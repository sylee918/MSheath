"""
omni_loader.py
==============
High-Resolution (5-minute) NASA SPDF OMNI Data Loader & Preprocessor.
Supports automatic download/caching from NASA SPDF and local offline files,
strict fill-value filtering, and short-gap (<=15 min) linear interpolation.
"""

import os
import urllib.request
from typing import Dict, Optional
import numpy as np
import pandas as pd


SPDF_5MIN_URL_TEMPLATE = (
    "https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/omni_5min{year}.asc"
)

# 0-based column indices from official NASA SPDF HRO_format.txt
OMNI_5MIN_COL_MAP = {
    0: "year",
    1: "doy",
    2: "hour",
    3: "minute",
    13: "b_mag",
    14: "bx_gsm",     # Bx (GSE, GSM are identical)
    15: "by_gse",
    16: "bz_gse",
    17: "by_gsm",
    18: "bz_gsm",
    21: "vsw",        # Flow speed [km/s]
    22: "vx_gse",     # Vx [km/s] in GSE
    23: "vy_gse",     # Vy [km/s] in GSE
    24: "vz_gse",     # Vz [km/s] in GSE
    25: "np",         # Proton number density [cm^-3]
    26: "temp_k",     # Proton temperature [K]
    27: "pdyn",       # Flow dynamic pressure [nPa]
}


def download_omni_5min(year: int, cache_dir: str = "data/omni_5min") -> str:
    """Download annual 5-minute OMNI ASCII file from NASA SPDF if not cached."""
    os.makedirs(cache_dir, exist_ok=True)
    local_path = os.path.join(cache_dir, f"omni_5min{year}.asc")
    if os.path.exists(local_path) and os.path.getsize(local_path) > 1024:
        return local_path

    url = SPDF_5MIN_URL_TEMPLATE.format(year=year)
    print(f"[omni_loader] Downloading {url} -> {local_path} ...")
    urllib.request.urlretrieve(url, local_path)
    print(f"[omni_loader] Download complete ({os.path.getsize(local_path) / (1024*1024):.2f} MB)")
    return local_path


def load_and_preprocess_omni(
    year: int,
    filepath: Optional[str] = None,
    cache_dir: str = "data/omni_5min",
    max_interp_steps: int = 3,
    month_filter: Optional[int] = None,
) -> pd.DataFrame:
    """
    Load 5-minute OMNI data for a given year (or specific month), filter fill values,
    and interpolate short gaps (<= max_interp_steps * 5 minutes).

    Quality Flag Definition:
      2 = Valid observed record (all required model inputs present)
      1 = Short gap (<= 15 min) filled via linear interpolation
      0 = Missing / long gap (> 15 min), model evaluation skipped
    """
    if filepath is None:
        filepath = download_omni_5min(year, cache_dir=cache_dir)

    usecols = sorted(OMNI_5MIN_COL_MAP.keys())
    col_names = [OMNI_5MIN_COL_MAP[i] for i in usecols]

    df = pd.read_csv(
        filepath,
        sep=r"\s+",
        header=None,
        usecols=usecols,
        names=col_names,
        dtype={
            "year": np.int32,
            "doy": np.int32,
            "hour": np.int32,
            "minute": np.int32,
            "b_mag": np.float64,
            "bx_gsm": np.float64,
            "by_gse": np.float64,
            "bz_gse": np.float64,
            "by_gsm": np.float64,
            "bz_gsm": np.float64,
            "vsw": np.float64,
            "vx_gse": np.float64,
            "vy_gse": np.float64,
            "vz_gse": np.float64,
            "np": np.float64,
            "temp_k": np.float64,
            "pdyn": np.float64,
        },
    )

    # Construct UTC timestamp
    base_year = pd.to_datetime(df["year"].astype(str) + "-01-01T00:00:00Z")
    df["timestamp"] = (
        base_year
        + pd.to_timedelta(df["doy"] - 1, unit="D")
        + pd.to_timedelta(df["hour"], unit="h")
        + pd.to_timedelta(df["minute"], unit="m")
    )
    df["unix_time"] = df["timestamp"].astype("int64") // 10**9
    df["month"] = df["timestamp"].dt.month

    if month_filter is not None:
        df = df[df["month"] == month_filter].copy().reset_index(drop=True)

    # 1. Replace official NASA SPDF Fill Values and out-of-bounds values with NaN
    b_cols = ["b_mag", "bx_gsm", "by_gse", "bz_gse", "by_gsm", "bz_gsm"]
    for c in b_cols:
        df.loc[(df[c] >= 999.0) | (df[c].abs() > 500.0), c] = np.nan

    v_cols = ["vsw", "vx_gse", "vy_gse", "vz_gse"]
    for c in v_cols:
        df.loc[(df[c] >= 9999.0) | (df[c].abs() > 3000.0), c] = np.nan
    df.loc[df["vsw"] < 150.0, "vsw"] = np.nan

    df.loc[(df["np"] >= 999.0) | (df["np"] <= 0.05) | (df["np"] > 500.0), "np"] = np.nan
    df.loc[(df["temp_k"] >= 9999990.0) | (df["temp_k"] <= 500.0) | (df["temp_k"] > 5.0e7), "temp_k"] = np.nan
    df.loc[(df["pdyn"] >= 99.0) | (df["pdyn"] <= 0.01), "pdyn"] = np.nan

    # Fallback: if vsw is missing but (vx_gse, vy_gse, vz_gse) are valid, compute vsw
    v_vec_mag = np.sqrt(df["vx_gse"] ** 2 + df["vy_gse"] ** 2 + df["vz_gse"] ** 2)
    df["vsw"] = df["vsw"].fillna(v_vec_mag)

    # Required model inputs for Tsyganenko (2024, 2025)
    req_cols = ["bx_gsm", "by_gsm", "bz_gsm", "vsw", "np", "temp_k"]
    obs_valid = df[req_cols].notna().all(axis=1)

    # 2. Interpolate short gaps (<= max_interp_steps consecutive 5-min bins)
    if max_interp_steps > 0:
        df[req_cols] = df[req_cols].interpolate(
            method="linear", limit=max_interp_steps, limit_direction="both"
        )
        for c in ["vx_gse", "vy_gse", "vz_gse"]:
            df[c] = df[c].interpolate(
                method="linear", limit=max_interp_steps, limit_direction="both"
            )

    after_valid = df[req_cols].notna().all(axis=1)

    # Assign quality_flag: 2=observed, 1=interpolated, 0=missing
    df["quality_flag"] = np.where(obs_valid, 2, np.where(after_valid, 1, 0)).astype(np.int8)

    # Derived solar wind thermal energy W_sw [eV] and dynamic pressure P_dyn [nPa]
    df["wsw_ev"] = df["temp_k"] / 11604.525
    df["pdyn"] = df["pdyn"].fillna(1.937e-6 * df["np"] * (df["vsw"] ** 2))

    return df


def split_by_month(df: pd.DataFrame) -> Dict[int, pd.DataFrame]:
    """Split a preprocessed OMNI DataFrame into monthly chunks (1..12)."""
    chunks = {}
    for m, grp in df.groupby("month", sort=True):
        chunks[int(m)] = grp.copy().reset_index(drop=True)
    return chunks
