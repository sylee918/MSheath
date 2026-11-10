"""
nc_writer.py
============
CF-1.8 Compliant NetCDF4 (.nc) Writer for Monthly GSE 2D Magnetosheath Distributions.
Stores both 5-minute time-resolved 2D distributions and monthly cell-level statistics
(Mean, Median, Std, Valid Count) with zlib compression.
"""

import os
from datetime import datetime, timezone
from typing import Dict, Any
import numpy as np
import pandas as pd
import netCDF4 as nc


VAR_META = {
    "np": ("Proton Number Density", "cm^-3"),
    "temp_k": ("Proton Temperature", "K"),
    "vx_gse": ("GSE X Flow Velocity Component", "km/s"),
    "vy_gse": ("GSE Y Flow Velocity Component", "km/s"),
    "vz_gse": ("GSE Z Flow Velocity Component", "km/s"),
    "vmag": ("Bulk Flow Speed", "km/s"),
    "rbs": ("Bow Shock Radial Distance (Lu et al. 2019)", "R_E"),
    "rmp": ("Magnetopause Radial Distance (Lin et al. 2010)", "R_E"),
}


def save_monthly_netcdf(
    year: int,
    month: int,
    df_month: pd.DataFrame,
    chunk_res: Dict[str, Any],
    stats: Dict[str, np.ndarray],
    out_dir: str = "output_nc",
    complevel: int = 4,
) -> str:
    """Write monthly GSE 2D distributions and aggregated statistics to a compressed NetCDF4 file."""
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"MSH_GSE_{year:04d}-{month:02d}.nc")

    x_axis = chunk_res["x_axis"]
    y_axis = chunk_res["y_axis"]
    z_axis = chunk_res["z_axis"]
    unix_time = chunk_res["unix_time"]

    nt, nx, ny, nz = len(unix_time), len(x_axis), len(y_axis), len(z_axis)

    with nc.Dataset(out_path, mode="w", format="NETCDF4") as ds:
        # 1. Global Attributes
        ds.title = (
            f"Tsyganenko (2024, 2025) Empirical Magnetosheath 2D Distributions in GSE "
            f"({year:04d}-{month:02d})"
        )
        ds.coordinate_system = "GSE (Geocentric Solar Ecliptic)"
        ds.model_references = (
            "Tsyganenko et al. (2024, JGR: Space Physics, 10.1029/2024JA033233); "
            "Tsyganenko et al. (2025, JGR: Space Physics, 10.1029/2025JA034343)"
        )
        ds.boundary_models = "Magnetopause: Lin et al. (2010); Bow Shock: Lu et al. (2019)"
        ds.time_resolution = "5 minutes"
        ds.time_coverage_start = pd.to_datetime(unix_time[0], unit="s", utc=True).isoformat()
        ds.time_coverage_end = pd.to_datetime(unix_time[-1], unit="s", utc=True).isoformat()
        ds.grid_x_range_Re = f"[{float(x_axis[0]):.2f}, {float(x_axis[-1]):.2f}]"
        ds.grid_y_range_Re = f"[{float(y_axis[0]):.2f}, {float(y_axis[-1]):.2f}]"
        ds.grid_z_range_Re = f"[{float(z_axis[0]):.2f}, {float(z_axis[-1]):.2f}]"
        ds.grid_bin_size_Re = float(x_axis[1] - x_axis[0]) if nx > 1 else 0.5
        ds.meridional_nightside_policy = "X_GSE < 0 skipped and masked (_FillValue=NaN, flag=-1)"
        ds.history = f"Created on {datetime.now(timezone.utc).isoformat()} by HPC GSE MSheath Pipeline"

        # 2. Dimensions
        ds.createDimension("time", nt)
        ds.createDimension("x_gse", nx)
        ds.createDimension("y_gse", ny)
        ds.createDimension("z_gse", nz)

        # 3. Coordinate Variables
        v_time = ds.createVariable("time", "i8", ("time",))
        v_time.long_name = "UTC Time"
        v_time.units = "seconds since 1970-01-01T00:00:00Z"
        v_time.calendar = "standard"
        v_time[:] = unix_time

        v_x = ds.createVariable("x_gse", "f4", ("x_gse",))
        v_x.long_name = "GSE X Coordinate"
        v_x.units = "R_E"
        v_x[:] = x_axis

        v_y = ds.createVariable("y_gse", "f4", ("y_gse",))
        v_y.long_name = "GSE Y Coordinate (Equatorial Plane Z_GSE = 0)"
        v_y.units = "R_E"
        v_y[:] = y_axis

        v_z = ds.createVariable("z_gse", "f4", ("z_gse",))
        v_z.long_name = "GSE Z Coordinate (Meridional Plane Y_GSE = 0)"
        v_z.units = "R_E"
        v_z[:] = z_axis

        # 4. 1D Solar Wind / IMF / Attitude Input Variables
        def _add_1d(name, dtype, data, long_name, units):
            var = ds.createVariable(name, dtype, ("time",), zlib=True, complevel=complevel)
            var.long_name = long_name
            var.units = units
            var[:] = data

        _add_1d("omni_quality_flag", "i1", chunk_res["quality_flag"],
                "OMNI Input Quality (2=observed, 1=interpolated_<=15m, 0=missing)", "1")
        _add_1d("dipole_tilt_deg", "f4", chunk_res["psi_deg"],
                "Geodipole Tilt Angle Psi", "degrees")
        _add_1d("gsm_to_gse_roll_deg", "f4", chunk_res["gsm_gse_angle_deg"],
                "Rotation Angle around X-axis between GSM and GSE", "degrees")
        _add_1d("sw_vsw", "f4", df_month["vsw"].to_numpy(dtype=np.float32),
                "Solar Wind Bulk Speed", "km/s")
        _add_1d("sw_np", "f4", df_month["np"].to_numpy(dtype=np.float32),
                "Solar Wind Proton Density", "cm^-3")
        _add_1d("sw_temp_k", "f4", df_month["temp_k"].to_numpy(dtype=np.float32),
                "Solar Wind Proton Temperature", "K")
        _add_1d("imf_bx_gsm", "f4", df_month["bx_gsm"].to_numpy(dtype=np.float32),
                "IMF Bx (GSM == GSE)", "nT")
        _add_1d("imf_by_gsm", "f4", df_month["by_gsm"].to_numpy(dtype=np.float32),
                "IMF By (GSM)", "nT")
        _add_1d("imf_bz_gsm", "f4", df_month["bz_gsm"].to_numpy(dtype=np.float32),
                "IMF Bz (GSM)", "nT")

        # 5. 3D Time-Resolved 2D Grids: Equatorial (time, x_gse, y_gse) & Meridional (time, x_gse, z_gse)
        for plane, dim2, plane_desc in [
            ("eq", "y_gse", "GSE Equatorial Plane (Z_GSE = 0)"),
            ("mer", "z_gse", "GSE Noon-Midnight Meridional Plane (Y_GSE = 0)"),
        ]:
            # Region Flag
            v_flg = ds.createVariable(
                f"{plane}_region_flag",
                "i1",
                ("time", "x_gse", dim2),
                zlib=True,
                complevel=complevel,
            )
            v_flg.long_name = f"Region Identification Flag on {plane_desc}"
            v_flg.flag_values = np.array([-2, -1, 0, 1, 2], dtype=np.int8)
            v_flg.flag_meanings = (
                "missing_omni_step masked_invalid_or_nightside inside_magnetopause "
                "magnetosheath upstream_solar_wind"
            )
            v_flg[:] = chunk_res[f"{plane}_flag"]

            for vkey, (desc, unit) in VAR_META.items():
                v_3d = ds.createVariable(
                    f"{plane}_{vkey}",
                    "f4",
                    ("time", "x_gse", dim2),
                    zlib=True,
                    complevel=complevel,
                    fill_value=np.nan,
                )
                v_3d.long_name = f"{desc} on {plane_desc}"
                v_3d.units = unit
                v_3d.coordinates = f"time x_gse {dim2}"
                v_3d[:] = chunk_res[f"{plane}_{vkey}"]

            # 6. Monthly 2D Summary Statistics (Mean, Median, Std, Counts)
            for c_type, c_desc in [
                ("valid_count", "Total Valid Evaluated Timesteps in Month"),
                ("msh_count", "Total Timesteps Located Inside Magnetosheath (flag==1)"),
            ]:
                vc = ds.createVariable(
                    f"{plane}_{c_type}",
                    "i4",
                    ("x_gse", dim2),
                    zlib=True,
                    complevel=complevel,
                )
                vc.long_name = f"{c_desc} on {plane_desc}"
                vc.units = "count"
                vc[:] = stats[f"{plane}_{c_type}"]

            for vkey in ["np", "temp_k", "vx_gse", "vy_gse", "vz_gse", "vmag"]:
                desc, unit = VAR_META[vkey]
                for stat_name in ["mean", "median", "std"]:
                    vs = ds.createVariable(
                        f"{plane}_{vkey}_{stat_name}",
                        "f4",
                        ("x_gse", dim2),
                        zlib=True,
                        complevel=complevel,
                        fill_value=np.nan,
                    )
                    vs.long_name = f"Monthly {stat_name.capitalize()} of {desc} on {plane_desc}"
                    vs.units = unit
                    vs[:] = stats[f"{plane}_{vkey}_{stat_name}"]

    return out_path
