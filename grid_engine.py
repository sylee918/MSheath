"""
grid_engine.py
==============
In-Memory Fortran (`libmsh.so`) 3D Volume Grid Evaluation & Monthly Statistical Aggregation Engine.
Evaluates the full 3D GSE magnetosheath volume (x_gse, y_gse, z_gse) at 5-minute cadence using
streaming 3D statistical accumulators, while extracting GSE Equatorial (X-Y, Z_GSE=0) and
GSE Meridional (X-Z, Y_GSE=0, skipping X_GSE < 0) 2D time-series slices at zero extra Fortran cost.
"""

import os
import ctypes
from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

from coord_transform import compute_epoch_rotations, gse_to_gsm_coords, gsm_to_gse_vector

VAR_PREFIXES = ["np", "temp_k", "vx_gse", "vy_gse", "vz_gse", "vmag"]


@dataclass
class GridConfig:
    xmin: float = -10.0
    xmax: float = 20.0
    dx: float = 1.0
    ymin: float = -25.0
    ymax: float = 25.0
    dy: float = 1.0
    zmin: float = -15.0
    zmax: float = 15.0
    dz: float = 1.0
    skip_meridional_nightside: bool = True
    save_2d_timeseries: bool = False


_LIB_INSTANCE: Optional[ctypes.CDLL] = None


def get_msh_lib(lib_path: str = "./libmsh.so") -> ctypes.CDLL:
    """Load and initialize `libmsh.so` once per worker process."""
    global _LIB_INSTANCE
    if _LIB_INSTANCE is None:
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Shared library not found: {lib_path}")
        lib = ctypes.CDLL(os.path.abspath(lib_path))
        lib.msh_init.argtypes = []
        lib.msh_init.restype = None

        p_f64 = ctypes.POINTER(ctypes.c_double)
        p_i32 = ctypes.POINTER(ctypes.c_int)
        lib.msh_eval_batch.argtypes = [
            ctypes.c_int,
            p_f64, p_f64, p_f64,
            ctypes.c_double, ctypes.c_double, ctypes.c_double,
            ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            p_f64, p_f64, p_f64, p_f64, p_f64, p_f64, p_f64, p_i32,
        ]
        lib.msh_eval_batch.restype = None
        lib.msh_init()
        _LIB_INSTANCE = lib
    return _LIB_INSTANCE


def evaluate_time_chunk(
    df_chunk: pd.DataFrame,
    cfg: GridConfig,
    lib_path: str = "./libmsh.so",
) -> Dict[str, Any]:
    """
    Evaluate the full 3D GSE grid for a chunk of 5-min OMNI records, accumulating
    exact 3D streaming statistics in RAM while extracting Equatorial (Z_GSE=0) and
    Meridional (Y_GSE=0, skipping X_GSE < 0 if configured) 2D time-series slices.
    """
    lib = get_msh_lib(lib_path)
    p_f64 = ctypes.POINTER(ctypes.c_double)
    p_i32 = ctypes.POINTER(ctypes.c_int)

    x_axis = np.arange(cfg.xmin, cfg.xmax + 0.5 * cfg.dx, cfg.dx, dtype=np.float64)
    y_axis = np.arange(cfg.ymin, cfg.ymax + 0.5 * cfg.dy, cfg.dy, dtype=np.float64)
    z_axis = np.arange(cfg.zmin, cfg.zmax + 0.5 * cfg.dz, cfg.dz, dtype=np.float64)

    nx, ny, nz = len(x_axis), len(y_axis), len(z_axis)
    nt = len(df_chunk)
    shape_3d = (nx, ny, nz)

    # Full 3D GSE grid
    X3d, Y3d, Z3d = np.meshgrid(x_axis, y_axis, z_axis, indexing="ij")
    x_flat = np.ascontiguousarray(X3d.ravel(), dtype=np.float64)
    y_flat = np.ascontiguousarray(Y3d.ravel(), dtype=np.float64)
    z_flat = np.ascontiguousarray(Z3d.ravel(), dtype=np.float64)
    n_3d = len(x_flat)

    # 2D slice indices (Equatorial Z_GSE=0, Meridional Y_GSE=0)
    iz0 = int(np.argmin(np.abs(z_axis - 0.0)))
    iy0 = int(np.argmin(np.abs(y_axis - 0.0)))

    if cfg.skip_meridional_nightside:
        ix_pos = np.where(x_axis >= -1e-9)[0]
        ix_start = int(ix_pos[0]) if len(ix_pos) > 0 else nx
    else:
        ix_start = 0

    out: Dict[str, Any] = {
        "x_axis": x_axis.astype(np.float32),
        "y_axis": y_axis.astype(np.float32),
        "z_axis": z_axis.astype(np.float32),
        "ix_start": ix_start,
        "unix_time": df_chunk["unix_time"].to_numpy(dtype=np.int64),
        "quality_flag": df_chunk["quality_flag"].to_numpy(dtype=np.int8),
        # 3D streaming accumulators (kept in float64/int32 without storing 4D time arrays)
        "vol_valid_count": np.zeros(shape_3d, dtype=np.int32),
        "vol_msh_count": np.zeros(shape_3d, dtype=np.int32),
        "vol_bndry_count": np.zeros(shape_3d, dtype=np.int32),
        "vol_rbs_sum": np.zeros(shape_3d, dtype=np.float64),
        "vol_rmp_sum": np.zeros(shape_3d, dtype=np.float64),
    }
    if cfg.save_2d_timeseries:
        shape_eq = (nt, nx, ny)
        shape_mer = (nt, nx, nz)
        out.update({
            "eq_np": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_temp_k": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_vx_gse": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_vy_gse": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_vz_gse": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_vmag": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_rbs": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_rmp": np.full(shape_eq, np.nan, dtype=np.float32),
            "eq_flag": np.full(shape_eq, -2, dtype=np.int8),
            "mer_np": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_temp_k": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_vx_gse": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_vy_gse": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_vz_gse": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_vmag": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_rbs": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_rmp": np.full(shape_mer, np.nan, dtype=np.float32),
            "mer_flag": np.full(shape_mer, -1, dtype=np.int8),  # -1 = masked nightside X < 0
        })
    for v in VAR_PREFIXES:
        out[f"vol_{v}_sum"] = np.zeros(shape_3d, dtype=np.float64)
        out[f"vol_{v}_sum_sq"] = np.zeros(shape_3d, dtype=np.float64)
        out[f"vol_{v}_msh_sum"] = np.zeros(shape_3d, dtype=np.float64)
        out[f"vol_{v}_msh_sum_sq"] = np.zeros(shape_3d, dtype=np.float64)

    # Precompute dipole tilt and GSE<->GSM rotation angles for all timestamps in chunk
    psi_deg, cos_a, sin_a = compute_epoch_rotations(out["unix_time"])
    out["psi_deg"] = psi_deg.astype(np.float32)
    out["gsm_gse_angle_deg"] = np.degrees(np.arctan2(sin_a, cos_a)).astype(np.float32)

    # Reusable work buffers for single 3D Fortran call per timestep
    den_3d = np.empty(n_3d, dtype=np.float64)
    tk_3d = np.empty(n_3d, dtype=np.float64)
    vx_3d = np.empty(n_3d, dtype=np.float64)
    vy_3d = np.empty(n_3d, dtype=np.float64)
    vz_3d = np.empty(n_3d, dtype=np.float64)
    rbs_3d = np.empty(n_3d, dtype=np.float64)
    rmp_3d = np.empty(n_3d, dtype=np.float64)
    flg_3d = np.empty(n_3d, dtype=np.int32)

    vsw_arr = df_chunk["vsw"].to_numpy(dtype=np.float64)
    dsw_arr = df_chunk["np"].to_numpy(dtype=np.float64)
    wsw_arr = df_chunk["wsw_ev"].to_numpy(dtype=np.float64)
    bx_arr = df_chunk["bx_gsm"].to_numpy(dtype=np.float64)
    by_arr = df_chunk["by_gsm"].to_numpy(dtype=np.float64)
    bz_arr = df_chunk["bz_gsm"].to_numpy(dtype=np.float64)
    qflag_arr = out["quality_flag"]

    for it in range(nt):
        if qflag_arr[it] == 0:
            continue

        vsw = float(vsw_arr[it])
        dsw = float(dsw_arr[it])
        wsw = float(wsw_arr[it])
        bx = float(bx_arr[it])
        by = float(by_arr[it])
        bz = float(bz_arr[it])
        psid = float(psi_deg[it])
        c_ang = float(cos_a[it])
        s_ang = float(sin_a[it])

        v_cap = max(vsw * 1.35, 480.0)
        n_min_msh = 0.25 * dsw

        # --- Full 3D Volume Evaluation ---
        xg, yg, zg = gse_to_gsm_coords(x_flat, y_flat, z_flat, c_ang, s_ang)
        lib.msh_eval_batch(
            n_3d,
            xg.ctypes.data_as(p_f64),
            yg.ctypes.data_as(p_f64),
            zg.ctypes.data_as(p_f64),
            vsw, dsw, wsw, bx, by, bz, psid,
            den_3d.ctypes.data_as(p_f64),
            tk_3d.ctypes.data_as(p_f64),
            vx_3d.ctypes.data_as(p_f64),
            vy_3d.ctypes.data_as(p_f64),
            vz_3d.ctypes.data_as(p_f64),
            rbs_3d.ctypes.data_as(p_f64),
            rmp_3d.ctypes.data_as(p_f64),
            flg_3d.ctypes.data_as(p_i32),
        )
        vx_gse_3d, vy_gse_3d, vz_gse_3d = gsm_to_gse_vector(vx_3d, vy_3d, vz_3d, c_ang, s_ang)
        vmag_3d = np.sqrt(vx_gse_3d ** 2 + vy_gse_3d ** 2 + vz_gse_3d ** 2)

        # Mask magnetosphere (flg == 0) and any unphysical extrapolation spikes
        inv_3d = (flg_3d == 1) & ((vmag_3d > v_cap) | (den_3d < n_min_msh) | (tk_3d > 8.0e6))
        mask_3d = (flg_3d == 0) | inv_3d
        flg_3d_clean = np.where(inv_3d, -1, flg_3d)

        flg_3d_grid = flg_3d_clean.reshape(shape_3d)
        mask_3d_grid = mask_3d.reshape(shape_3d)
        rbs_3d_grid = rbs_3d.reshape(shape_3d)
        rmp_3d_grid = rmp_3d.reshape(shape_3d)

        vars_3d_map = {
            "np": den_3d.reshape(shape_3d),
            "temp_k": tk_3d.reshape(shape_3d),
            "vx_gse": vx_gse_3d.reshape(shape_3d),
            "vy_gse": vy_gse_3d.reshape(shape_3d),
            "vz_gse": vz_gse_3d.reshape(shape_3d),
            "vmag": vmag_3d.reshape(shape_3d),
        }

        # Update 3D streaming accumulators
        all_finite = np.isfinite(vars_3d_map["np"]) & np.isfinite(vars_3d_map["temp_k"]) & np.isfinite(vars_3d_map["vmag"])
        valid_3d = (flg_3d_grid > 0) & all_finite
        msh_3d = (flg_3d_grid == 1) & all_finite
        finite_bndry = np.isfinite(rbs_3d_grid) & np.isfinite(rmp_3d_grid) & (rbs_3d_grid > 0.0) & (rmp_3d_grid > 0.0)

        out["vol_valid_count"] += valid_3d
        out["vol_msh_count"] += msh_3d
        out["vol_bndry_count"] += finite_bndry
        out["vol_rbs_sum"] += np.where(finite_bndry, rbs_3d_grid, 0.0)
        out["vol_rmp_sum"] += np.where(finite_bndry, rmp_3d_grid, 0.0)

        for vname, vgrid in vars_3d_map.items():
            c_all = np.where(valid_3d, vgrid, 0.0)
            out[f"vol_{vname}_sum"] += c_all
            out[f"vol_{vname}_sum_sq"] += c_all * c_all
            c_msh = np.where(msh_3d, vgrid, 0.0)
            out[f"vol_{vname}_msh_sum"] += c_msh
            out[f"vol_{vname}_msh_sum_sq"] += c_msh * c_msh

        # --- Extract 2D Slices (optional, zero extra Fortran calls) ---
        if cfg.save_2d_timeseries:
            # (A) Equatorial Plane (Z_GSE = 0)
            mask_eq_slice = mask_3d_grid[:, :, iz0]
            out["eq_flag"][it] = flg_3d_grid[:, :, iz0]
            out["eq_rbs"][it] = rbs_3d_grid[:, :, iz0]
            out["eq_rmp"][it] = rmp_3d_grid[:, :, iz0]
            for vname, vgrid in vars_3d_map.items():
                out[f"eq_{vname}"][it] = np.where(mask_eq_slice, np.nan, vgrid[:, :, iz0])

            # (B) Meridional Plane (Y_GSE = 0, skipping X_GSE < 0 when configured)
            if ix_start < nx:
                mask_mer_slice = mask_3d_grid[ix_start:, iy0, :]
                out["mer_flag"][it, ix_start:, :] = flg_3d_grid[ix_start:, iy0, :]
                out["mer_rbs"][it, ix_start:, :] = rbs_3d_grid[ix_start:, iy0, :]
                out["mer_rmp"][it, ix_start:, :] = rmp_3d_grid[ix_start:, iy0, :]
                for vname, vgrid in vars_3d_map.items():
                    out[f"mer_{vname}"][it, ix_start:, :] = np.where(mask_mer_slice, np.nan, vgrid[ix_start:, iy0, :])

    return out


def compute_monthly_statistics(chunk_res: Dict[str, Any]) -> Dict[str, np.ndarray]:
    """
    Compute monthly cell-level summary statistics (Mean, Std, Valid Count, MSH Count,
    plus Median when 2D time-series is present) for 3D volume and 2D slices.
    """
    stats: Dict[str, np.ndarray] = {}

    if "vol_valid_count" in chunk_res:
        vol_vc = chunk_res["vol_valid_count"].astype(np.int32)
        vol_mc = chunk_res["vol_msh_count"].astype(np.int32)
        vol_bc = chunk_res["vol_bndry_count"]

        stats["vol_valid_count"] = vol_vc
        stats["vol_msh_count"] = vol_mc

        denom_vc = np.maximum(vol_vc, 1).astype(np.float64)
        denom_mc = np.maximum(vol_mc, 1).astype(np.float64)
        denom_bc = np.maximum(vol_bc, 1).astype(np.float64)

        stats["vol_msh_fraction"] = np.where(
            vol_vc > 0, vol_mc.astype(np.float64) / denom_vc, np.nan
        ).astype(np.float32)
        stats["vol_rbs_mean"] = np.where(
            vol_bc > 0, chunk_res["vol_rbs_sum"] / denom_bc, np.nan
        ).astype(np.float32)
        stats["vol_rmp_mean"] = np.where(
            vol_bc > 0, chunk_res["vol_rmp_sum"] / denom_bc, np.nan
        ).astype(np.float32)

        inv_all = vol_vc == 0
        inv_msh = vol_mc == 0

        for v in VAR_PREFIXES:
            mean_all = chunk_res[f"vol_{v}_sum"] / denom_vc
            var_all = np.maximum(0.0, (chunk_res[f"vol_{v}_sum_sq"] / denom_vc) - mean_all * mean_all)
            std_all = np.sqrt(var_all)
            mean_all[inv_all] = np.nan
            std_all[inv_all] = np.nan
            stats[f"vol_{v}_mean"] = mean_all.astype(np.float32)
            stats[f"vol_{v}_std"] = std_all.astype(np.float32)

            mean_msh = chunk_res[f"vol_{v}_msh_sum"] / denom_mc
            var_msh = np.maximum(0.0, (chunk_res[f"vol_{v}_msh_sum_sq"] / denom_mc) - mean_msh * mean_msh)
            std_msh = np.sqrt(var_msh)
            mean_msh[inv_msh] = np.nan
            std_msh[inv_msh] = np.nan
            stats[f"vol_{v}_msh_mean"] = mean_msh.astype(np.float32)
            stats[f"vol_{v}_msh_std"] = std_msh.astype(np.float32)

    if "eq_flag" in chunk_res:
        import warnings
        for plane in ["eq", "mer"]:
            flg = chunk_res[f"{plane}_flag"]
            stats[f"{plane}_valid_count"] = np.sum(flg > 0, axis=0).astype(np.int32)
            stats[f"{plane}_msh_count"] = np.sum(flg == 1, axis=0).astype(np.int32)

            for v in VAR_PREFIXES:
                arr = chunk_res[f"{plane}_{v}"]
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    stats[f"{plane}_{v}_mean"] = np.nanmean(arr, axis=0).astype(np.float32)
                    stats[f"{plane}_{v}_median"] = np.nanmedian(arr, axis=0).astype(np.float32)
                    stats[f"{plane}_{v}_std"] = np.nanstd(arr, axis=0).astype(np.float32)
    elif "vol_valid_count" in stats:
        # Derive 2D Equatorial (Z=0) and Meridional (Y=0) monthly stats directly from 3D volume stats
        x_axis = chunk_res["x_axis"]
        y_axis = chunk_res["y_axis"]
        z_axis = chunk_res["z_axis"]
        iz0 = int(np.argmin(np.abs(z_axis - 0.0)))
        iy0 = int(np.argmin(np.abs(y_axis - 0.0)))
        ix_start = int(chunk_res.get("ix_start", 0))
        nx, nz = len(x_axis), len(z_axis)

        stats["eq_valid_count"] = stats["vol_valid_count"][:, :, iz0].copy()
        stats["eq_msh_count"] = stats["vol_msh_count"][:, :, iz0].copy()

        mer_vc = np.zeros((nx, nz), dtype=np.int32)
        mer_mc = np.zeros((nx, nz), dtype=np.int32)
        if ix_start < nx:
            mer_vc[ix_start:, :] = stats["vol_valid_count"][ix_start:, iy0, :]
            mer_mc[ix_start:, :] = stats["vol_msh_count"][ix_start:, iy0, :]
        stats["mer_valid_count"] = mer_vc
        stats["mer_msh_count"] = mer_mc

        for v in VAR_PREFIXES:
            for st in ["mean", "std"]:
                stats[f"eq_{v}_{st}"] = stats[f"vol_{v}_{st}"][:, :, iz0].copy()
                mer_arr = np.full((nx, nz), np.nan, dtype=np.float32)
                if ix_start < nx:
                    mer_arr[ix_start:, :] = stats[f"vol_{v}_{st}"][ix_start:, iy0, :]
                stats[f"mer_{v}_{st}"] = mer_arr

    return stats
