"""
grid_engine.py
==============
In-Memory Fortran (`libmsh.so`) Grid Evaluation & Monthly Statistical Aggregation Engine.
Evaluates GSE Equatorial (X-Y, Z_GSE=0) and GSE Meridional (X-Z, Y_GSE=0, skipping X_GSE < 0)
2D distributions at 5-minute cadence and computes monthly cell statistics (mean, median, std, count).
"""

import os
import ctypes
from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

from coord_transform import compute_epoch_rotations, gse_to_gsm_coords, gsm_to_gse_vector


@dataclass
class GridConfig:
    xmin: float = -10.0
    xmax: float = 20.0
    dx: float = 0.5
    ymin: float = -30.0
    ymax: float = 30.0
    dy: float = 0.5
    zmin: float = -30.0
    zmax: float = 30.0
    dz: float = 0.5
    skip_meridional_nightside: bool = True


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
    Evaluate GSE Equatorial and Meridional 2D distributions for a chunk of 5-min OMNI records.
    For the Meridional plane, X_GSE < 0 points are completely skipped during Fortran evaluation.
    """
    lib = get_msh_lib(lib_path)
    p_f64 = ctypes.POINTER(ctypes.c_double)
    p_i32 = ctypes.POINTER(ctypes.c_int)

    x_axis = np.arange(cfg.xmin, cfg.xmax + 0.5 * cfg.dx, cfg.dx, dtype=np.float64)
    y_axis = np.arange(cfg.ymin, cfg.ymax + 0.5 * cfg.dy, cfg.dy, dtype=np.float64)
    z_axis = np.arange(cfg.zmin, cfg.zmax + 0.5 * cfg.dz, cfg.dz, dtype=np.float64)

    nx, ny, nz = len(x_axis), len(y_axis), len(z_axis)
    nt = len(df_chunk)

    # 1. Equatorial GSE grid (Z_GSE = 0): full X in [-10, 20], Y in [-30, 30]
    eq_X2d, eq_Y2d = np.meshgrid(x_axis, y_axis, indexing="ij")
    eq_x_flat = eq_X2d.ravel()
    eq_y_flat = eq_Y2d.ravel()
    eq_z_flat = np.zeros_like(eq_x_flat)
    n_eq = len(eq_x_flat)

    # 2. Meridional GSE grid (Y_GSE = 0): only evaluate X_GSE >= 0 if skip_meridional_nightside=True
    if cfg.skip_meridional_nightside:
        ix_pos = np.where(x_axis >= -1e-9)[0]
        x_mer_eval = x_axis[ix_pos]
        ix_start = int(ix_pos[0])
    else:
        x_mer_eval = x_axis
        ix_start = 0

    mer_X2d, mer_Z2d = np.meshgrid(x_mer_eval, z_axis, indexing="ij")
    mer_x_flat = mer_X2d.ravel()
    mer_y_flat = np.zeros_like(mer_x_flat)
    mer_z_flat = mer_Z2d.ravel()
    n_mer_eval = len(mer_x_flat)
    nx_mer_eval = len(x_mer_eval)

    # Preallocate output 3D arrays (float32 to save 50% RAM)
    shape_eq = (nt, nx, ny)
    shape_mer = (nt, nx, nz)

    out = {
        "x_axis": x_axis.astype(np.float32),
        "y_axis": y_axis.astype(np.float32),
        "z_axis": z_axis.astype(np.float32),
        "unix_time": df_chunk["unix_time"].to_numpy(dtype=np.int64),
        "quality_flag": df_chunk["quality_flag"].to_numpy(dtype=np.int8),
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
    }

    # Precompute dipole tilt and GSE<->GSM rotation angles for all timestamps in chunk
    psi_deg, cos_a, sin_a = compute_epoch_rotations(out["unix_time"])
    out["psi_deg"] = psi_deg.astype(np.float32)
    out["gsm_gse_angle_deg"] = np.degrees(np.arctan2(sin_a, cos_a)).astype(np.float32)

    # Reusable work buffers for Fortran call
    den_eq = np.empty(n_eq, dtype=np.float64)
    tk_eq = np.empty(n_eq, dtype=np.float64)
    vx_eq = np.empty(n_eq, dtype=np.float64)
    vy_eq = np.empty(n_eq, dtype=np.float64)
    vz_eq = np.empty(n_eq, dtype=np.float64)
    rbs_eq = np.empty(n_eq, dtype=np.float64)
    rmp_eq = np.empty(n_eq, dtype=np.float64)
    flg_eq = np.empty(n_eq, dtype=np.int32)

    den_mer = np.empty(n_mer_eval, dtype=np.float64)
    tk_mer = np.empty(n_mer_eval, dtype=np.float64)
    vx_mer = np.empty(n_mer_eval, dtype=np.float64)
    vy_mer = np.empty(n_mer_eval, dtype=np.float64)
    vz_mer = np.empty(n_mer_eval, dtype=np.float64)
    rbs_mer = np.empty(n_mer_eval, dtype=np.float64)
    rmp_mer = np.empty(n_mer_eval, dtype=np.float64)
    flg_mer = np.empty(n_mer_eval, dtype=np.int32)

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

        # --- (A) Equatorial Plane (Z_GSE = 0) ---
        xg, yg, zg = gse_to_gsm_coords(eq_x_flat, eq_y_flat, eq_z_flat, c_ang, s_ang)
        lib.msh_eval_batch(
            n_eq,
            xg.ctypes.data_as(p_f64),
            yg.ctypes.data_as(p_f64),
            zg.ctypes.data_as(p_f64),
            vsw, dsw, wsw, bx, by, bz, psid,
            den_eq.ctypes.data_as(p_f64),
            tk_eq.ctypes.data_as(p_f64),
            vx_eq.ctypes.data_as(p_f64),
            vy_eq.ctypes.data_as(p_f64),
            vz_eq.ctypes.data_as(p_f64),
            rbs_eq.ctypes.data_as(p_f64),
            rmp_eq.ctypes.data_as(p_f64),
            flg_eq.ctypes.data_as(p_i32),
        )
        vx_gse_eq, vy_gse_eq, vz_gse_eq = gsm_to_gse_vector(vx_eq, vy_eq, vz_eq, c_ang, s_ang)
        vmag_eq = np.sqrt(vx_gse_eq ** 2 + vy_gse_eq ** 2 + vz_gse_eq ** 2)

        # Mask magnetosphere (flg == 0) and any unphysical extrapolation spikes
        inv_eq = (flg_eq == 1) & ((vmag_eq > v_cap) | (den_eq < n_min_msh) | (tk_eq > 8.0e6))
        mask_eq = (flg_eq == 0) | inv_eq
        flg_eq_clean = np.where(inv_eq, -1, flg_eq)

        out["eq_np"][it] = np.where(mask_eq, np.nan, den_eq).reshape((nx, ny))
        out["eq_temp_k"][it] = np.where(mask_eq, np.nan, tk_eq).reshape((nx, ny))
        out["eq_vx_gse"][it] = np.where(mask_eq, np.nan, vx_gse_eq).reshape((nx, ny))
        out["eq_vy_gse"][it] = np.where(mask_eq, np.nan, vy_gse_eq).reshape((nx, ny))
        out["eq_vz_gse"][it] = np.where(mask_eq, np.nan, vz_gse_eq).reshape((nx, ny))
        out["eq_vmag"][it] = np.where(mask_eq, np.nan, vmag_eq).reshape((nx, ny))
        out["eq_rbs"][it] = rbs_eq.reshape((nx, ny))
        out["eq_rmp"][it] = rmp_eq.reshape((nx, ny))
        out["eq_flag"][it] = flg_eq_clean.reshape((nx, ny))

        # --- (B) Meridional Plane (Y_GSE = 0, skipping X_GSE < 0) ---
        xg_m, yg_m, zg_m = gse_to_gsm_coords(mer_x_flat, mer_y_flat, mer_z_flat, c_ang, s_ang)
        lib.msh_eval_batch(
            n_mer_eval,
            xg_m.ctypes.data_as(p_f64),
            yg_m.ctypes.data_as(p_f64),
            zg_m.ctypes.data_as(p_f64),
            vsw, dsw, wsw, bx, by, bz, psid,
            den_mer.ctypes.data_as(p_f64),
            tk_mer.ctypes.data_as(p_f64),
            vx_mer.ctypes.data_as(p_f64),
            vy_mer.ctypes.data_as(p_f64),
            vz_mer.ctypes.data_as(p_f64),
            rbs_mer.ctypes.data_as(p_f64),
            rmp_mer.ctypes.data_as(p_f64),
            flg_mer.ctypes.data_as(p_i32),
        )
        vx_gse_m, vy_gse_m, vz_gse_m = gsm_to_gse_vector(vx_mer, vy_mer, vz_mer, c_ang, s_ang)
        vmag_m = np.sqrt(vx_gse_m ** 2 + vy_gse_m ** 2 + vz_gse_m ** 2)

        inv_m = (flg_mer == 1) & ((vmag_m > v_cap) | (den_mer < n_min_msh) | (tk_mer > 8.0e6))
        mask_m = (flg_mer == 0) | inv_m
        flg_m_clean = np.where(inv_m, -1, flg_mer)

        out["mer_np"][it, ix_start:, :] = np.where(mask_m, np.nan, den_mer).reshape((nx_mer_eval, nz))
        out["mer_temp_k"][it, ix_start:, :] = np.where(mask_m, np.nan, tk_mer).reshape((nx_mer_eval, nz))
        out["mer_vx_gse"][it, ix_start:, :] = np.where(mask_m, np.nan, vx_gse_m).reshape((nx_mer_eval, nz))
        out["mer_vy_gse"][it, ix_start:, :] = np.where(mask_m, np.nan, vy_gse_m).reshape((nx_mer_eval, nz))
        out["mer_vz_gse"][it, ix_start:, :] = np.where(mask_m, np.nan, vz_gse_m).reshape((nx_mer_eval, nz))
        out["mer_vmag"][it, ix_start:, :] = np.where(mask_m, np.nan, vmag_m).reshape((nx_mer_eval, nz))
        out["mer_rbs"][it, ix_start:, :] = rbs_mer.reshape((nx_mer_eval, nz))
        out["mer_rmp"][it, ix_start:, :] = rmp_mer.reshape((nx_mer_eval, nz))
        out["mer_flag"][it, ix_start:, :] = flg_m_clean.reshape((nx_mer_eval, nz))

    return out


def compute_monthly_statistics(chunk_res: Dict[str, Any]) -> Dict[str, np.ndarray]:
    """
    Compute monthly cell-level summary statistics (Mean, Median, Std, Valid Count, MSH Count)
    across the time axis (axis=0) for both Equatorial and Meridional planes.
    """
    stats = {}
    var_prefixes = ["np", "temp_k", "vx_gse", "vy_gse", "vz_gse", "vmag"]

    import warnings
    for plane in ["eq", "mer"]:
        flg = chunk_res[f"{plane}_flag"]
        stats[f"{plane}_valid_count"] = np.sum(flg > 0, axis=0).astype(np.int32)
        stats[f"{plane}_msh_count"] = np.sum(flg == 1, axis=0).astype(np.int32)

        for v in var_prefixes:
            arr = chunk_res[f"{plane}_{v}"]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                stats[f"{plane}_{v}_mean"] = np.nanmean(arr, axis=0).astype(np.float32)
                stats[f"{plane}_{v}_median"] = np.nanmedian(arr, axis=0).astype(np.float32)
                stats[f"{plane}_{v}_std"] = np.nanstd(arr, axis=0).astype(np.float32)

    return stats
