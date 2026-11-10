"""
test_hpc_pipeline.py
====================
Automated Verification Suite for the 40-Core GSE Magnetosheath HPC Pipeline.
"""

import time
import numpy as np
import netCDF4 as nc

from grid_engine import get_msh_lib
from omni_loader import load_and_preprocess_omni
from coord_transform import verify_coordinate_transforms
from hpc_pipeline import run_annual_pipeline
import ctypes


def test_1_fortran_lib_consistency():
    print("\n--- [Test 1] Fortran Shared Library (libmsh.so) Consistency & Speed ---")
    lib = get_msh_lib("./libmsh.so")
    d = np.genfromtxt("omni_20180101_equatorial.dat", names=True)
    n = len(d)

    x = np.ascontiguousarray(d["X"], dtype=np.float64)
    y = np.ascontiguousarray(d["Y"], dtype=np.float64)
    z = np.ascontiguousarray(d["Z"], dtype=np.float64)

    den = np.empty(n, dtype=np.float64)
    tk = np.empty(n, dtype=np.float64)
    vx = np.empty(n, dtype=np.float64)
    vy = np.empty(n, dtype=np.float64)
    vz = np.empty(n, dtype=np.float64)
    rbs = np.empty(n, dtype=np.float64)
    rmp = np.empty(n, dtype=np.float64)
    flg = np.empty(n, dtype=np.int32)

    p_f64 = ctypes.POINTER(ctypes.c_double)
    p_i32 = ctypes.POINTER(ctypes.c_int)

    t0 = time.perf_counter()
    lib.msh_eval_batch(
        n,
        x.ctypes.data_as(p_f64),
        y.ctypes.data_as(p_f64),
        z.ctypes.data_as(p_f64),
        370.0, 13.46, 6.50, 1.54, -6.64, -4.20, -25.40,
        den.ctypes.data_as(p_f64),
        tk.ctypes.data_as(p_f64),
        vx.ctypes.data_as(p_f64),
        vy.ctypes.data_as(p_f64),
        vz.ctypes.data_as(p_f64),
        rbs.ctypes.data_as(p_f64),
        rmp.ctypes.data_as(p_f64),
        flg.ctypes.data_as(p_i32),
    )
    dt_ms = (time.perf_counter() - t0) * 1000.0

    max_diff_den = np.max(np.abs(den - d["DEN"]))
    max_diff_vx = np.max(np.abs(vx - d["VX"]))
    max_diff_vy = np.max(np.abs(vy - d["VY"]))
    flag_match = np.all(flg == d["IFLAG"].astype(np.int32))

    print(f"  29,161 grid points evaluated in: {dt_ms:.2f} ms (vs ~650 ms subprocess+ASCII I/O)")
    print(f"  Max diff vs ASCII .dat (4-decimal format): DEN={max_diff_den:.2e}, VX={max_diff_vx:.2e}, VY={max_diff_vy:.2e}")
    print(f"  Region flag 100% match: {flag_match}")
    assert max_diff_den < 1e-3 and max_diff_vx < 1e-3 and flag_match, "Mismatch with reference!"


def test_2_omni_and_coords():
    print("\n--- [Test 2] NASA SPDF 5-min OMNI Loader & GSM<->GSE Verification ---")
    df = load_and_preprocess_omni(year=2018, month_filter=1)
    print(f"  2018-01 5-min records: {len(df)} (Expected: 8928)")
    assert len(df) == 8928, f"Expected 8928 5-min records in Jan 2018, got {len(df)}"

    rep = verify_coordinate_transforms(sample_df=df)
    for k, v in rep.items():
        print(f"  {k}: {v}")
    assert rep["passed"], "Coordinate transform verification failed!"


def test_3_end_to_end_pipeline():
    print("\n--- [Test 3] End-to-End Multi-Worker Pipeline & NetCDF4 Verification ---")
    summary = run_annual_pipeline(
        year=2018,
        months=[1],
        total_cores=12,
        workers_per_month=12,
        concurrent_months=1,
        dx=0.5,
        out_dir="output_nc",
        max_steps_per_month=288,  # 24 hours (288 x 5-min steps) benchmark
    )
    nc_path = summary[0]["nc_path"]
    elapsed = summary[0]["elapsed_sec"]

    with nc.Dataset(nc_path, "r") as ds:
        print(f"  NetCDF4 file verified: {nc_path}")
        print(f"  Coordinate system attr: {ds.coordinate_system}")
        print(f"  Dimensions: {{k: len(v) for k, v in ds.dimensions.items()}} -> "
              f"{ {k: len(v) for k, v in ds.dimensions.items()} }")

        x_gse = np.ma.filled(ds.variables["x_gse"][:], np.nan)
        mer_np = np.ma.filled(ds.variables["mer_np"][:], np.nan)
        mer_flg = np.ma.filled(ds.variables["mer_region_flag"][:], -99)
        eq_np_mean = np.ma.filled(ds.variables["eq_np_mean"][:], np.nan)
        eq_np_med = np.ma.filled(ds.variables["eq_np_median"][:], np.nan)
        eq_cnt = np.ma.filled(ds.variables["eq_valid_count"][:], 0)

        # Verify X_GSE < 0 in Meridional plane is 100% masked (NaN and flag == -1)
        ix_neg = np.where(x_gse < 0)[0]
        assert np.all(np.isnan(mer_np[:, ix_neg, :])), "Meridional X<0 must be NaN!"
        assert np.all(mer_flg[:, ix_neg, :] == -1), "Meridional X<0 flag must be -1!"
        print(f"  Meridional X_GSE < 0 skip/mask verified (all {len(ix_neg)} X<0 slices are NaN & flag=-1)")
        print(f"  Equatorial peak monthly mean Np: {np.nanmax(eq_np_mean):.2f} cm^-3, "
              f"median Np: {np.nanmax(eq_np_med):.2f} cm^-3, max valid count: {np.max(eq_cnt)}")

    steps_per_sec = 288.0 / elapsed
    est_year_40core_min = (105120.0 / (steps_per_sec * (40.0 / 12.0))) / 60.0
    print(f"  Throughput (12 workers): {steps_per_sec:.1f} steps/sec "
          f"-> Projected 1-year (105,120 steps) on 40 cores: ~{est_year_40core_min:.1f} minutes!")


if __name__ == "__main__":
    test_1_fortran_lib_consistency()
    test_2_omni_and_coords()
    test_3_end_to_end_pipeline()
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
