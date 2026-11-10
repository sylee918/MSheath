#!/usr/bin/env python3
"""
build_summary_stats.py
======================
Generates a lightweight, self-contained NetCDF4 summary dataset (`MSH_GSE_2018_Summary.nc`)
from the 12 monthly 5-minute HPC NetCDF4 files (e.g., on NASA Lou `/u/slee122/MSheath/Tsy2018/`).

What this script computes and packages into a single ~5-8 MB file for local plotting:
  1. Monthly 2D Statistics (12 months x 61 x 121) for Equatorial (XY) & Meridional (XZ) planes:
     - Pre-computed All-Valid (MSH + SW) Mean, Median, Std, Valid Count, MSH Count, MSH Probability.
     - Pure Magnetosheath-Only (`region_flag == 1`) Mean and Std for Np, T, Vx, Vy, Vz, Vmag.
     - Monthly Mean Bow Shock (`rbs`) and Magnetopause (`rmp`) 2D fields for exact boundary contours.
  2. Exact Full-Year (Annual) 2D Maps (61 x 121):
     - Pooled exact Mean, Std, MSH Probability, and Mean Boundaries for both All-Valid and MSH-Only.
  3. Conditional Physical Regime 2D Composites (8 Regimes x 61 x 121):
     - [0] Full Year Baseline
     - [1] Southward IMF (Bz_GSM < -2 nT)
     - [2] Northward IMF (Bz_GSM > +2 nT)
     - [3] High Dynamic Pressure (Pdyn > 2.5 nPa)
     - [4] Low Dynamic Pressure (Pdyn < 1.2 nPa)
     - [5] Positive Dipole Tilt (Psi > +15 deg, Northern Summer)
     - [6] Negative Dipole Tilt (Psi < -15 deg, Northern Winter)
     - [7] Near-Equinox Dipole Tilt (|Psi| <= 5 deg)
  4. Full-Year 5-Minute 1D Time Series (105,120 steps):
     - Solar wind & IMF inputs (Vsw, Np, Temp, Pdyn, Bx, By, Bz, Dipole Tilt, Quality Flag).
     - Subsolar Nose (Y_GSE=0, Z_GSE=0) Bow Shock standoff (R_BS0), Magnetopause standoff (R_MP0),
       Magnetosheath thickness (dR_MSH), and subsolar MSH mean Np, Vmag, and Temperature.

Usage on NASA Lou / Pleiades:
  python3 build_summary_stats.py --in-dir /u/slee122/MSheath/Tsy2018 --year 2018
"""

import os
import sys
import glob
import time
import warnings
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
import numpy as np
import netCDF4 as nc


VARS = ["np", "temp_k", "vx_gse", "vy_gse", "vz_gse", "vmag"]
VAR_META = {
    "np": ("Proton Number Density", "cm^-3"),
    "temp_k": ("Proton Temperature", "K"),
    "vx_gse": ("GSE X Flow Velocity Component", "km/s"),
    "vy_gse": ("GSE Y Flow Velocity Component", "km/s"),
    "vz_gse": ("GSE Z Flow Velocity Component", "km/s"),
    "vmag": ("Bulk Flow Speed", "km/s"),
}

REGIME_NAMES = [
    "all_year",
    "imf_south_bz_lt_m2",
    "imf_north_bz_gt_p2",
    "pdyn_high_gt_2p5",
    "pdyn_low_lt_1p2",
    "tilt_pos_gt_p15",
    "tilt_neg_lt_m15",
    "tilt_equinox_abs_le_5",
]

REGIME_DESCRIPTIONS = [
    "0: Full Year Baseline (All Valid Steps)",
    "1: Southward IMF (Bz_GSM < -2.0 nT)",
    "2: Northward IMF (Bz_GSM > +2.0 nT)",
    "3: High Solar Wind Dynamic Pressure (Pdyn > 2.5 nPa)",
    "4: Low Solar Wind Dynamic Pressure (Pdyn < 1.2 nPa)",
    "5: Positive Dipole Tilt (Psi > +15 deg, Northern Summer)",
    "6: Negative Dipole Tilt (Psi < -15 deg, Northern Winter)",
    "7: Near-Equinox Dipole Tilt (|Psi| <= 5 deg)",
]


class StreamingAccumulator2D:
    """Memory-efficient running accumulator for exact 2D mean and standard deviation."""

    def __init__(self, shape: Tuple[int, int]):
        self.shape = shape
        self.count = np.zeros(shape, dtype=np.int64)
        self.sum_val = {v: np.zeros(shape, dtype=np.float64) for v in VARS + ["rbs", "rmp"]}
        self.sum_sq = {v: np.zeros(shape, dtype=np.float64) for v in VARS}

    def update(self, mask: np.ndarray, data_dict: Dict[str, np.ndarray], rbs: np.ndarray, rmp: np.ndarray, valid_step_mask: np.ndarray):
        """
        mask: 3D boolean array (nt, nx, n2) indicating valid cells for this accumulator.
        valid_step_mask: 1D boolean array (nt,) for boundary averaging.
        """
        if not np.any(valid_step_mask):
            return
        c = np.sum(mask, axis=0)
        self.count += c

        for v in VARS:
            arr = data_dict[v]
            clean = np.where(mask, arr, 0.0)
            self.sum_val[v] += np.sum(clean, axis=0)
            self.sum_sq[v] += np.sum(clean * clean, axis=0)

        # For rbs and rmp, average over valid steps in the regime
        rbs_sub = rbs[valid_step_mask]
        rmp_sub = rmp[valid_step_mask]
        finite_rbs = np.isfinite(rbs_sub)
        finite_rmp = np.isfinite(rmp_sub)
        self.sum_val["rbs"] += np.sum(np.where(finite_rbs, rbs_sub, 0.0), axis=0)
        self.sum_val["rmp"] += np.sum(np.where(finite_rmp, rmp_sub, 0.0), axis=0)

    def finalize_var(self, v: str) -> Tuple[np.ndarray, np.ndarray]:
        denom = np.maximum(self.count, 1).astype(np.float64)
        mean = self.sum_val[v] / denom
        var = np.maximum(0.0, (self.sum_sq[v] / denom) - mean * mean)
        std = np.sqrt(var)
        invalid = self.count == 0
        mean[invalid] = np.nan
        std[invalid] = np.nan
        return mean.astype(np.float32), std.astype(np.float32)

    def finalize_boundary(self, bname: str, total_valid_steps: int) -> np.ndarray:
        if total_valid_steps <= 0:
            return np.full(self.shape, np.nan, dtype=np.float32)
        out = (self.sum_val[bname] / float(total_valid_steps)).astype(np.float32)
        out[out <= 0.0] = np.nan
        return out


def find_monthly_files(in_dir: str, year: int) -> Dict[int, str]:
    found = {}
    for m in range(1, 13):
        candidate = os.path.join(in_dir, f"MSH_GSE_{year:04d}-{m:02d}.nc")
        if os.path.isfile(candidate):
            found[m] = candidate
    return found


def build_summary(in_dir: str, out_path: str, year: int = 2018, bg_msp_density: Optional[float] = 0.1) -> str:
    t0 = time.perf_counter()
    monthly_files = find_monthly_files(in_dir, year)
    if not monthly_files:
        raise FileNotFoundError(f"No MSH_GSE_{year:04d}-MM.nc files found in '{in_dir}'.")

    months_present = sorted(monthly_files.keys())
    print("=" * 76)
    print(f"[Summary Builder] Found {len(months_present)} monthly file(s) in: {in_dir}")
    print(f"                  Months: {months_present}")
    print("=" * 76)

    # Inspect grid coordinates from first available file
    first_file = monthly_files[months_present[0]]
    with nc.Dataset(first_file, "r") as ds0:
        x_gse = np.array(ds0.variables["x_gse"][:], dtype=np.float32)
        y_gse = np.array(ds0.variables["y_gse"][:], dtype=np.float32)
        z_gse = np.array(ds0.variables["z_gse"][:], dtype=np.float32)

    nx, ny, nz = len(x_gse), len(y_gse), len(z_gse)
    eq_shape = (nx, ny)
    mer_shape = (nx, nz)
    n_regimes = len(REGIME_NAMES)

    # Find indices for Subsolar Nose line (Y_GSE == 0, X_GSE >= 0)
    iy0 = int(np.argmin(np.abs(y_gse - 0.0)))
    iz0 = int(np.argmin(np.abs(z_gse - 0.0)))
    ix_pos = np.where(x_gse >= 0.0)[0]
    ix_nose_ref = int(np.argmin(np.abs(x_gse - 10.0)))

    # Allocate Monthly 2D arrays (12, nx, ny/nz)
    m_data: Dict[str, np.ndarray] = {}
    for plane, n2 in [("eq", ny), ("mer", nz)]:
        m_data[f"{plane}_valid_count"] = np.zeros((12, nx, n2), dtype=np.int32)
        m_data[f"{plane}_msh_count"] = np.zeros((12, nx, n2), dtype=np.int32)
        m_data[f"{plane}_msh_fraction"] = np.full((12, nx, n2), np.nan, dtype=np.float32)
        m_data[f"{plane}_rbs_mean"] = np.full((12, nx, n2), np.nan, dtype=np.float32)
        m_data[f"{plane}_rmp_mean"] = np.full((12, nx, n2), np.nan, dtype=np.float32)
        for v in VARS:
            for st in ["mean", "median", "std", "msh_mean", "msh_std"]:
                m_data[f"{plane}_{v}_{st}"] = np.full((12, nx, n2), np.nan, dtype=np.float32)

    # Streaming accumulators for Annual (All-Valid & MSH-Only) and 8 Regimes (All-Valid & MSH-Only)
    acc_annual_all = {"eq": StreamingAccumulator2D(eq_shape), "mer": StreamingAccumulator2D(mer_shape)}
    acc_annual_msh = {"eq": StreamingAccumulator2D(eq_shape), "mer": StreamingAccumulator2D(mer_shape)}
    acc_regime_all = {
        "eq": [StreamingAccumulator2D(eq_shape) for _ in range(n_regimes)],
        "mer": [StreamingAccumulator2D(mer_shape) for _ in range(n_regimes)],
    }
    acc_regime_msh = {
        "eq": [StreamingAccumulator2D(eq_shape) for _ in range(n_regimes)],
        "mer": [StreamingAccumulator2D(mer_shape) for _ in range(n_regimes)],
    }
    regime_step_counts = np.zeros(n_regimes, dtype=np.int64)
    total_valid_steps_year = 0

    # Lists for 1D Full-Year Time Series
    ts_lists: Dict[str, List[np.ndarray]] = {
        "time": [],
        "month": [],
        "omni_quality_flag": [],
        "dipole_tilt_deg": [],
        "gsm_to_gse_roll_deg": [],
        "sw_vsw": [],
        "sw_np": [],
        "sw_temp_k": [],
        "sw_pdyn_npa": [],
        "imf_bx_gsm": [],
        "imf_by_gsm": [],
        "imf_bz_gsm": [],
        "subsolar_rbs_Re": [],
        "subsolar_rmp_Re": [],
        "subsolar_msh_thickness_Re": [],
        "subsolar_msh_np": [],
        "subsolar_msh_vmag": [],
        "subsolar_msh_temp_k": [],
    }

    # Process each month sequentially to keep memory footprint low (< 400 MB)
    for m in months_present:
        m_idx = m - 1
        fpath = monthly_files[m]
        tm0 = time.perf_counter()

        with nc.Dataset(fpath, "r") as ds:
            t_arr = np.array(ds.variables["time"][:], dtype=np.int64)
            nt = len(t_arr)
            q_flag = np.array(ds.variables["omni_quality_flag"][:], dtype=np.int8)
            psi_deg = np.array(ds.variables["dipole_tilt_deg"][:], dtype=np.float32)
            roll_deg = np.array(ds.variables["gsm_to_gse_roll_deg"][:], dtype=np.float32)
            vsw = np.array(ds.variables["sw_vsw"][:], dtype=np.float32)
            sw_np = np.array(ds.variables["sw_np"][:], dtype=np.float32)
            sw_tk = np.array(ds.variables["sw_temp_k"][:], dtype=np.float32)
            bx = np.array(ds.variables["imf_bx_gsm"][:], dtype=np.float32)
            by = np.array(ds.variables["imf_by_gsm"][:], dtype=np.float32)
            bz = np.array(ds.variables["imf_bz_gsm"][:], dtype=np.float32)

            # Dynamic pressure Pdyn [nPa] = 1.6726e-6 * Np [cm^-3] * Vsw^2 [km/s]^2
            pdyn = (1.6726e-6 * sw_np * (vsw ** 2)).astype(np.float32)
            valid_t = q_flag > 0
            n_valid_m = int(np.sum(valid_t))
            total_valid_steps_year += n_valid_m

            # Define 1D boolean masks for the 8 physical regimes
            r_masks_1d = [
                valid_t,                                          # 0: All year valid
                valid_t & (bz < -2.0),                            # 1: Southward IMF
                valid_t & (bz > 2.0),                             # 2: Northward IMF
                valid_t & (pdyn > 2.5),                           # 3: High Pdyn
                valid_t & (pdyn < 1.2),                           # 4: Low Pdyn
                valid_t & (psi_deg > 15.0),                       # 5: Positive dipole tilt
                valid_t & (psi_deg < -15.0),                      # 6: Negative dipole tilt
                valid_t & (np.abs(psi_deg) <= 5.0),               # 7: Equinox dipole tilt
            ]
            for ir, rm in enumerate(r_masks_1d):
                regime_step_counts[ir] += int(np.sum(rm))

            # Process Equatorial and Meridional planes
            for plane, shape_2d in [("eq", eq_shape), ("mer", mer_shape)]:
                # 1. Read pre-computed monthly summaries
                vc = np.array(ds.variables[f"{plane}_valid_count"][:], dtype=np.int32)
                mc = np.array(ds.variables[f"{plane}_msh_count"][:], dtype=np.int32)
                m_data[f"{plane}_valid_count"][m_idx] = vc
                m_data[f"{plane}_msh_count"][m_idx] = mc
                with np.errstate(divide="ignore", invalid="ignore"):
                    frac = np.where(vc > 0, mc.astype(np.float32) / vc.astype(np.float32), np.nan)
                m_data[f"{plane}_msh_fraction"][m_idx] = frac

                for v in VARS:
                    for st in ["mean", "median", "std"]:
                        m_data[f"{plane}_{v}_{st}"][m_idx] = np.array(
                            ds.variables[f"{plane}_{v}_{st}"][:], dtype=np.float32
                        )

                # 2. Load 3D arrays for MSH-only stats, boundary means, and regime composites
                flg_3d = np.array(ds.variables[f"{plane}_region_flag"][:], dtype=np.int8)
                rbs_3d = np.array(ds.variables[f"{plane}_rbs"][:], dtype=np.float32)
                rmp_3d = np.array(ds.variables[f"{plane}_rmp"][:], dtype=np.float32)

                vars_3d = {}
                for v in VARS:
                    vars_3d[v] = np.array(ds.variables[f"{plane}_{v}"][:], dtype=np.float32)

                # Mask definitions
                # flg_3d: 1=MSH, 2=SW, 0=MSP, -1=Nightside/Invalid, -2=Missing OMNI
                # When bg_msp_density is set, fill magnetosphere (flg_3d == 0) with background value (e.g. 0.1 cm^-3)
                if bg_msp_density is not None:
                    is_msp = (flg_3d == 0)
                    vars_3d["np"] = np.where(is_msp, np.float32(bg_msp_density), vars_3d["np"])
                    vars_3d["temp_k"] = np.where(is_msp, np.float32(1.0e5), vars_3d["temp_k"]) # 0.1 MK background
                    vars_3d["vx_gse"] = np.where(is_msp, np.float32(0.0), vars_3d["vx_gse"])
                    vars_3d["vy_gse"] = np.where(is_msp, np.float32(0.0), vars_3d["vy_gse"])
                    vars_3d["vz_gse"] = np.where(is_msp, np.float32(0.0), vars_3d["vz_gse"])
                    vars_3d["vmag"] = np.where(is_msp, np.float32(0.0), vars_3d["vmag"])
                    mask_all_valid = (flg_3d >= 0) & np.isfinite(vars_3d["np"])
                else:
                    mask_all_valid = (flg_3d > 0) & np.isfinite(vars_3d["np"])

                mask_msh_only = (flg_3d == 1) & np.isfinite(vars_3d["np"])

                # Monthly MSH-only stats and boundary means
                acc_m_msh = StreamingAccumulator2D(shape_2d)
                acc_m_msh.update(mask_msh_only, vars_3d, rbs_3d, rmp_3d, valid_t)
                for v in VARS:
                    m_mean, m_std = acc_m_msh.finalize_var(v)
                    m_data[f"{plane}_{v}_msh_mean"][m_idx] = m_mean
                    m_data[f"{plane}_{v}_msh_std"][m_idx] = m_std

                m_data[f"{plane}_rbs_mean"][m_idx] = acc_m_msh.finalize_boundary("rbs", n_valid_m)
                m_data[f"{plane}_rmp_mean"][m_idx] = acc_m_msh.finalize_boundary("rmp", n_valid_m)

                # Update Annual Accumulators
                acc_annual_all[plane].update(mask_all_valid, vars_3d, rbs_3d, rmp_3d, valid_t)
                acc_annual_msh[plane].update(mask_msh_only, vars_3d, rbs_3d, rmp_3d, valid_t)

                # Update Regime Accumulators
                for ir, rm_1d in enumerate(r_masks_1d):
                    if not np.any(rm_1d):
                        continue
                    rm_3d = rm_1d[:, None, None]
                    acc_regime_all[plane][ir].update(mask_all_valid & rm_3d, vars_3d, rbs_3d, rmp_3d, rm_1d)
                    acc_regime_msh[plane][ir].update(mask_msh_only & rm_3d, vars_3d, rbs_3d, rmp_3d, rm_1d)

                # Extract Subsolar 1D time series from Equatorial plane (Y_GSE == 0)
                if plane == "eq":
                    rbs_nose = rbs_3d[:, ix_nose_ref, iy0].copy()
                    rmp_nose = rmp_3d[:, ix_nose_ref, iy0].copy()
                    rbs_nose[~valid_t] = np.nan
                    rmp_nose[~valid_t] = np.nan
                    dr_nose = rbs_nose - rmp_nose

                    # Subsolar line MSH average (X >= 0, Y = 0, flag == 1)
                    sub_msh_mask = mask_msh_only[:, ix_pos, iy0]
                    sub_cnt = np.maximum(np.sum(sub_msh_mask, axis=1), 1)
                    has_sub = np.sum(sub_msh_mask, axis=1) > 0

                    sub_np = np.sum(np.where(sub_msh_mask, vars_3d["np"][:, ix_pos, iy0], 0.0), axis=1) / sub_cnt
                    sub_vm = np.sum(np.where(sub_msh_mask, vars_3d["vmag"][:, ix_pos, iy0], 0.0), axis=1) / sub_cnt
                    sub_tk = np.sum(np.where(sub_msh_mask, vars_3d["temp_k"][:, ix_pos, iy0], 0.0), axis=1) / sub_cnt

                    sub_np = np.where(has_sub, sub_np, np.nan).astype(np.float32)
                    sub_vm = np.where(has_sub, sub_vm, np.nan).astype(np.float32)
                    sub_tk = np.where(has_sub, sub_tk, np.nan).astype(np.float32)

                    ts_lists["time"].append(t_arr)
                    ts_lists["month"].append(np.full(nt, m, dtype=np.int8))
                    ts_lists["omni_quality_flag"].append(q_flag)
                    ts_lists["dipole_tilt_deg"].append(psi_deg)
                    ts_lists["gsm_to_gse_roll_deg"].append(roll_deg)
                    ts_lists["sw_vsw"].append(vsw)
                    ts_lists["sw_np"].append(sw_np)
                    ts_lists["sw_temp_k"].append(sw_tk)
                    ts_lists["sw_pdyn_npa"].append(pdyn)
                    ts_lists["imf_bx_gsm"].append(bx)
                    ts_lists["imf_by_gsm"].append(by)
                    ts_lists["imf_bz_gsm"].append(bz)
                    ts_lists["subsolar_rbs_Re"].append(rbs_nose)
                    ts_lists["subsolar_rmp_Re"].append(rmp_nose)
                    ts_lists["subsolar_msh_thickness_Re"].append(dr_nose)
                    ts_lists["subsolar_msh_np"].append(sub_np)
                    ts_lists["subsolar_msh_vmag"].append(sub_vm)
                    ts_lists["subsolar_msh_temp_k"].append(sub_tk)

        print(f"  [Month {year:04d}-{m:02d}] Processed {nt:,} steps (valid={n_valid_m:,}) in {time.perf_counter()-tm0:.2f}s")

    # Concatenate 1D time series
    ts_concat = {k: np.concatenate(v_list, axis=0) for k, v_list in ts_lists.items()}
    nt_total = len(ts_concat["time"])

    # Write output summary NetCDF4
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    complevel = 5
    with nc.Dataset(out_path, "w", format="NETCDF4") as ds_out:
        ds_out.title = f"Tsyganenko (2024, 2025) GSE Magnetosheath Annual & Monthly Statistical Summary ({year})"
        ds_out.coordinate_system = "GSE (Geocentric Solar Ecliptic)"
        ds_out.source_directory = os.path.abspath(in_dir)
        ds_out.months_included = ",".join(str(m) for m in months_present)
        ds_out.total_timesteps = int(nt_total)
        ds_out.total_valid_timesteps = int(total_valid_steps_year)
        ds_out.regime_definitions = " | ".join(REGIME_DESCRIPTIONS)
        ds_out.history = f"Generated on {datetime.now(timezone.utc).isoformat()} by build_summary_stats.py"

        # Dimensions
        ds_out.createDimension("month", 12)
        ds_out.createDimension("regime", n_regimes)
        ds_out.createDimension("x_gse", nx)
        ds_out.createDimension("y_gse", ny)
        ds_out.createDimension("z_gse", nz)
        ds_out.createDimension("time", nt_total)

        # Coordinate Variables
        v_m = ds_out.createVariable("month", "i4", ("month",))
        v_m.long_name = "Calendar Month (1=Jan .. 12=Dec)"
        v_m[:] = np.arange(1, 13, dtype=np.int32)

        v_r = ds_out.createVariable("regime", "i4", ("regime",))
        v_r.long_name = "Physical Regime Index"
        v_r.flag_values = np.arange(n_regimes, dtype=np.int32)
        v_r.flag_meanings = " ".join(REGIME_NAMES)
        v_r.descriptions = " ; ".join(REGIME_DESCRIPTIONS)
        v_r[:] = np.arange(n_regimes, dtype=np.int32)

        v_rc = ds_out.createVariable("regime_step_count", "i8", ("regime",))
        v_rc.long_name = "Number of Valid 5-min Timesteps in Regime"
        v_rc[:] = regime_step_counts

        for cname, cdata, desc in [
            ("x_gse", x_gse, "GSE X Coordinate [R_E]"),
            ("y_gse", y_gse, "GSE Y Coordinate (Equatorial Plane Z_GSE=0) [R_E]"),
            ("z_gse", z_gse, "GSE Z Coordinate (Meridional Plane Y_GSE=0) [R_E]"),
        ]:
            vc = ds_out.createVariable(cname, "f4", (cname,))
            vc.long_name = desc
            vc.units = "R_E"
            vc[:] = cdata

        # 1. Write Monthly 2D Statistics (month, x_gse, y_gse/z_gse)
        for plane, dim2 in [("eq", "y_gse"), ("mer", "z_gse")]:
            for k_suffix, dtype in [
                ("valid_count", "i4"),
                ("msh_count", "i4"),
                ("msh_fraction", "f4"),
                ("rbs_mean", "f4"),
                ("rmp_mean", "f4"),
            ]:
                k = f"{plane}_{k_suffix}"
                kwargs = {"zlib": True, "complevel": complevel}
                if dtype == "f4":
                    kwargs["fill_value"] = np.nan
                var = ds_out.createVariable(f"monthly_{k}", dtype, ("month", "x_gse", dim2), **kwargs)
                var[:] = m_data[k]

            for v in VARS:
                for st in ["mean", "median", "std", "msh_mean", "msh_std"]:
                    k = f"{plane}_{v}_{st}"
                    var = ds_out.createVariable(
                        f"monthly_{k}", "f4", ("month", "x_gse", dim2), zlib=True, complevel=complevel, fill_value=np.nan
                    )
                    var.units = VAR_META[v][1]
                    var[:] = m_data[k]

            # 2. Write Annual 2D Maps (x_gse, y_gse/z_gse)
            acc_a = acc_annual_all[plane]
            acc_m = acc_annual_msh[plane]

            v_avc = ds_out.createVariable(f"annual_{plane}_valid_count", "i4", ("x_gse", dim2), zlib=True, complevel=complevel)
            v_avc[:] = acc_a.count.astype(np.int32)

            v_amc = ds_out.createVariable(f"annual_{plane}_msh_count", "i4", ("x_gse", dim2), zlib=True, complevel=complevel)
            v_amc[:] = acc_m.count.astype(np.int32)

            v_afr = ds_out.createVariable(f"annual_{plane}_msh_fraction", "f4", ("x_gse", dim2), zlib=True, complevel=complevel, fill_value=np.nan)
            with np.errstate(divide="ignore", invalid="ignore"):
                v_afr[:] = np.where(acc_a.count > 0, acc_m.count / acc_a.count, np.nan).astype(np.float32)

            v_arbs = ds_out.createVariable(f"annual_{plane}_rbs_mean", "f4", ("x_gse", dim2), zlib=True, complevel=complevel, fill_value=np.nan)
            v_arbs[:] = acc_a.finalize_boundary("rbs", total_valid_steps_year)

            v_armp = ds_out.createVariable(f"annual_{plane}_rmp_mean", "f4", ("x_gse", dim2), zlib=True, complevel=complevel, fill_value=np.nan)
            v_armp[:] = acc_a.finalize_boundary("rmp", total_valid_steps_year)

            for v in VARS:
                a_mean, a_std = acc_a.finalize_var(v)
                m_mean, m_std = acc_m.finalize_var(v)
                # Approximate annual median from monthly medians
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    a_med = np.nanmedian(m_data[f"{plane}_{v}_median"], axis=0).astype(np.float32)

                for st_name, arr_2d in [
                    ("mean", a_mean),
                    ("median", a_med),
                    ("std", a_std),
                    ("msh_mean", m_mean),
                    ("msh_std", m_std),
                ]:
                    vv = ds_out.createVariable(
                        f"annual_{plane}_{v}_{st_name}", "f4", ("x_gse", dim2),
                        zlib=True, complevel=complevel, fill_value=np.nan
                    )
                    vv.units = VAR_META[v][1]
                    vv[:] = arr_2d

            # 3. Write Conditional Physical Regime 2D Composites (regime, x_gse, y_gse/z_gse)
            n2_len = ny if plane == "eq" else nz
            reg_msh_frac = np.full((n_regimes, nx, n2_len), np.nan, dtype=np.float32)
            reg_rbs = np.full((n_regimes, nx, n2_len), np.nan, dtype=np.float32)
            reg_rmp = np.full((n_regimes, nx, n2_len), np.nan, dtype=np.float32)

            for ir in range(n_regimes):
                ca = acc_regime_all[plane][ir].count
                cm = acc_regime_msh[plane][ir].count
                with np.errstate(divide="ignore", invalid="ignore"):
                    reg_msh_frac[ir] = np.where(ca > 0, cm / ca, np.nan).astype(np.float32)
                reg_rbs[ir] = acc_regime_all[plane][ir].finalize_boundary("rbs", int(regime_step_counts[ir]))
                reg_rmp[ir] = acc_regime_all[plane][ir].finalize_boundary("rmp", int(regime_step_counts[ir]))

            for r_suf, r_arr in [("msh_fraction", reg_msh_frac), ("rbs_mean", reg_rbs), ("rmp_mean", reg_rmp)]:
                vr = ds_out.createVariable(
                    f"regime_{plane}_{r_suf}", "f4", ("regime", "x_gse", dim2),
                    zlib=True, complevel=complevel, fill_value=np.nan
                )
                vr[:] = r_arr

            for v in VARS:
                r_all_mean = np.full((n_regimes, nx, n2_len), np.nan, dtype=np.float32)
                r_msh_mean = np.full((n_regimes, nx, n2_len), np.nan, dtype=np.float32)
                r_msh_std = np.full((n_regimes, nx, n2_len), np.nan, dtype=np.float32)
                for ir in range(n_regimes):
                    r_all_mean[ir], _ = acc_regime_all[plane][ir].finalize_var(v)
                    r_msh_mean[ir], r_msh_std[ir] = acc_regime_msh[plane][ir].finalize_var(v)

                for st_s, r_arr in [("mean", r_all_mean), ("msh_mean", r_msh_mean), ("msh_std", r_msh_std)]:
                    vr = ds_out.createVariable(
                        f"regime_{plane}_{v}_{st_s}", "f4", ("regime", "x_gse", dim2),
                        zlib=True, complevel=complevel, fill_value=np.nan
                    )
                    vr.units = VAR_META[v][1]
                    vr[:] = r_arr

        # 4. Write 1D Full-Year Time Series (time,)
        v_t = ds_out.createVariable("time", "i8", ("time",), zlib=True, complevel=complevel)
        v_t.long_name = "UTC Time"
        v_t.units = "seconds since 1970-01-01T00:00:00Z"
        v_t[:] = ts_concat["time"]

        for ts_name, ts_dtype in [
            ("month", "i1"),
            ("omni_quality_flag", "i1"),
            ("dipole_tilt_deg", "f4"),
            ("gsm_to_gse_roll_deg", "f4"),
            ("sw_vsw", "f4"),
            ("sw_np", "f4"),
            ("sw_temp_k", "f4"),
            ("sw_pdyn_npa", "f4"),
            ("imf_bx_gsm", "f4"),
            ("imf_by_gsm", "f4"),
            ("imf_bz_gsm", "f4"),
            ("subsolar_rbs_Re", "f4"),
            ("subsolar_rmp_Re", "f4"),
            ("subsolar_msh_thickness_Re", "f4"),
            ("subsolar_msh_np", "f4"),
            ("subsolar_msh_vmag", "f4"),
            ("subsolar_msh_temp_k", "f4"),
        ]:
            v_key = "ts_month" if ts_name == "month" else ts_name
            kwargs = {"zlib": True, "complevel": complevel}
            if ts_dtype == "f4":
                kwargs["fill_value"] = np.nan
            vt = ds_out.createVariable(v_key, ts_dtype, ("time",), **kwargs)
            vt[:] = ts_concat[ts_name]

    sz_mb = os.path.getsize(out_path) / (1024 * 1024)
    dt_total = time.perf_counter() - t0
    print("=" * 76)
    print(f"[Summary Complete] Saved: {out_path} ({sz_mb:.2f} MB) in {dt_total:.2f} s")
    print("=" * 76)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Build compact NetCDF4 summary stats from monthly MSheath files.")
    parser.add_argument(
        "--in-dir",
        type=str,
        default="/u/slee122/MSheath/Tsy2018",
        help="Directory containing MSH_GSE_YYYY-MM.nc files (default: /u/slee122/MSheath/Tsy2018)",
    )
    parser.add_argument("--year", type=int, default=2018, help="Target year (default: 2018)")
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output NetCDF4 summary path (default: summary_stats/MSH_GSE_<YEAR>_Summary.nc)",
    )
    parser.add_argument(
        "--bg-msp-np",
        type=float,
        default=0.1,
        help="Background proton density [cm^-3] inside magnetopause (flg==0) (default: 0.1, set to negative to disable)",
    )
    args = parser.parse_args()

    bg_msp = args.bg_msp_np if args.bg_msp_np >= 0.0 else None
    out_path = args.out or os.path.join("summary_stats", f"MSH_GSE_{args.year:04d}_Summary.nc")
    build_summary(in_dir=args.in_dir, out_path=out_path, year=args.year, bg_msp_density=bg_msp)


if __name__ == "__main__":
    main()
