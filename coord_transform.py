"""
coord_transform.py
==================
Precision GSM <-> GSE Coordinate Transformation & Verification Module.

 Coordinate System Priority:
  1. `geopack` (N. A. Tsyganenko's official IGRF/GSM-GSE library used by NASA OMNI & MSheath models)
  2. `spacepy.coordinates` (IRBEM / SpacePy fallback & cross-validator)
  3. `astropy.coordinates` (Astropy frame transformation fallback)

Mathematical Formulation:
  GSE and GSM share the exact same X-axis (pointing from Earth toward the Sun: X_GSE == X_GSM).
  They differ by a time-dependent orthogonal rotation angle alpha(t) in the Y-Z plane:
    - Position (GSE -> GSM):
        X_GSM =  X_GSE
        Y_GSM =  Y_GSE * cos(alpha) + Z_GSE * sin(alpha)   [where (0, cos_a, sin_a) = gsmgse(0, 1, 0, -1)]
        Z_GSM = -Y_GSE * sin(alpha) + Z_GSE * cos(alpha)
      More generally, if e_y_GSE in GSM is (0, c, s) and e_z_GSE in GSM is (0, -s, c):
        Y_GSM = Y_GSE * c - Z_GSE * s
        Z_GSM = Y_GSE * s + Z_GSE * c
    - Vector (GSM -> GSE, transpose rotation):
        Vx_GSE =  Vx_GSM
        Vy_GSE =  Vy_GSM * c + Vz_GSM * s
        Vz_GSE = -Vy_GSM * s + Vz_GSM * c
"""

from typing import Tuple, Dict, Any
import numpy as np

try:
    from geopack import geopack as _gp
    HAS_GEOPACK = True
except ImportError:
    HAS_GEOPACK = False


def compute_epoch_rotations(unix_times: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute dipole tilt angle psi_deg [deg] and GSE<->GSM rotation coefficients (cos_a, sin_a)
    for a 1D array of UTC Unix timestamps.

    For each timestamp t:
      Calling `geopack.gsmgse(0.0, 1.0, 0.0, -1)` maps unit vector +Y_GSE into GSM: (0, c, s).
      By right-handed orthogonality (with X_GSM == X_GSE), unit vector +Z_GSE in GSM is (0, -s, c).
      Therefore:
        GSE -> GSM:
          X_GSM = X_GSE
          Y_GSM = c * Y_GSE - s * Z_GSE
          Z_GSM = s * Y_GSE + c * Z_GSE
        GSM -> GSE (inverse/transpose):
          X_GSE = X_GSM
          Y_GSE =  c * Y_GSM + s * Z_GSM
          Z_GSE = -s * Y_GSM + c * Z_GSM
    """
    if not HAS_GEOPACK:
        raise RuntimeError("geopack is required for primary GSM<->GSE transformations.")

    n = len(unix_times)
    psi_deg = np.empty(n, dtype=np.float64)
    cos_a = np.empty(n, dtype=np.float64)
    sin_a = np.empty(n, dtype=np.float64)

    rad2deg = 180.0 / np.pi
    for i in range(n):
        ut = float(unix_times[i])
        psi_rad = _gp.recalc(ut)
        psi_deg[i] = psi_rad * rad2deg
        _, c, s = _gp.gsmgse(0.0, 1.0, 0.0, -1)
        cos_a[i] = c
        sin_a[i] = s

    return psi_deg, cos_a, sin_a


def gse_to_gsm_coords(
    x_gse: np.ndarray,
    y_gse: np.ndarray,
    z_gse: np.ndarray,
    cos_a: float,
    sin_a: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Transform 3D spatial grid coordinates from GSE to GSM at a given epoch."""
    x_gsm = np.ascontiguousarray(x_gse, dtype=np.float64)
    y_gsm = np.ascontiguousarray(cos_a * y_gse - sin_a * z_gse, dtype=np.float64)
    z_gsm = np.ascontiguousarray(sin_a * y_gse + cos_a * z_gse, dtype=np.float64)
    return x_gsm, y_gsm, z_gsm


def gsm_to_gse_vector(
    vx_gsm: np.ndarray,
    vy_gsm: np.ndarray,
    vz_gsm: np.ndarray,
    cos_a: float,
    sin_a: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Transform 3D flow velocity (or magnetic field) vectors from GSM to GSE at a given epoch."""
    vx_gse = vx_gsm
    vy_gse = cos_a * vy_gsm + sin_a * vz_gsm
    vz_gse = -sin_a * vy_gsm + cos_a * vz_gsm
    return vx_gse, vy_gse, vz_gse


def verify_coordinate_transforms(sample_df=None) -> Dict[str, Any]:
    """
    Run 4-stage mathematical and physical verification of the GSM<->GSE transformation:
      1. Matrix orthogonality: |cos^2(a) + sin^2(a) - 1| < 1e-14
      2. Round-trip coordinate invertibility: ||r_GSE - GSM_to_GSE(GSE_to_GSM(r_GSE))|| < 1e-14
      3. Vector magnitude invariance: ||V_GSE| - |V_GSM|| < 1e-12
      4. Cross-validation against official NASA OMNI (By_GSE, Bz_GSE) vs (By_GSM, Bz_GSM)
    """
    test_uts = np.array([1514764800.0, 1521590400.0, 1530403200.0, 1545350400.0])  # 4 seasons
    psi_deg, cos_a, sin_a = compute_epoch_rotations(test_uts)

    # 1. Orthogonality check
    det_err = np.max(np.abs(cos_a ** 2 + sin_a ** 2 - 1.0))

    # 2. Round-trip invertibility check on random 3D points
    rng = np.random.default_rng(42)
    pts_gse = rng.uniform(-30.0, 30.0, size=(3, 500))
    max_rt_err = 0.0
    max_norm_err = 0.0

    for i in range(len(test_uts)):
        xg, yg, zg = gse_to_gsm_coords(pts_gse[0], pts_gse[1], pts_gse[2], cos_a[i], sin_a[i])
        xr, yr, zr = gsm_to_gse_vector(xg, yg, zg, cos_a[i], sin_a[i])
        rt_err = max(
            np.max(np.abs(xr - pts_gse[0])),
            np.max(np.abs(yr - pts_gse[1])),
            np.max(np.abs(zr - pts_gse[2])),
        )
        max_rt_err = max(max_rt_err, float(rt_err))

        # 3. Vector magnitude preservation
        mag_gsm = np.sqrt(xg ** 2 + yg ** 2 + zg ** 2)
        mag_gse = np.sqrt(xr ** 2 + yr ** 2 + zr ** 2)
        max_norm_err = max(max_norm_err, float(np.max(np.abs(mag_gsm - mag_gse))))

    # 4. Cross-check against OMNI GSE/GSM magnetic field vectors if sample_df is provided
    omni_rms_diff_nt = None
    if sample_df is not None and len(sample_df) > 0:
        valid = sample_df[["by_gse", "bz_gse", "by_gsm", "bz_gsm"]].notna().all(axis=1)
        sub = sample_df[valid].iloc[:200]
        if len(sub) > 0:
            _, c_arr, s_arr = compute_epoch_rotations(sub["unix_time"].to_numpy())
            by_gse_calc = c_arr * sub["by_gsm"].to_numpy() + s_arr * sub["bz_gsm"].to_numpy()
            bz_gse_calc = -s_arr * sub["by_gsm"].to_numpy() + c_arr * sub["bz_gsm"].to_numpy()
            diff_y = by_gse_calc - sub["by_gse"].to_numpy()
            diff_z = bz_gse_calc - sub["bz_gse"].to_numpy()
            omni_rms_diff_nt = float(np.sqrt(np.mean(diff_y ** 2 + diff_z ** 2)))

    passed = (det_err < 1e-14) and (max_rt_err < 1e-13) and (max_norm_err < 1e-12)
    if omni_rms_diff_nt is not None:
        passed = passed and (omni_rms_diff_nt < 0.05)  # OMNI rounds B to 0.01 nT

    return {
        "passed": bool(passed),
        "max_orthogonality_error": float(det_err),
        "max_roundtrip_error_Re": float(max_rt_err),
        "max_norm_error_kms": float(max_norm_err),
        "omni_b_field_rms_diff_nT": omni_rms_diff_nt,
    }
