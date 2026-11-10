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
    print("\n--- [Test 1] Fortran Shared Library (libmsh.so) Sanity & Speed ---")
    lib = get_msh_lib("./libmsh.so")

    import os
    if os.path.exists("omni_20180101_equatorial.dat"):
        d = np.genfromtxt("omni_20180101_equatorial.dat", names=True)
        x = np.ascontiguousarray(d["X"], dtype=np.float64)
        y = np.ascontiguousarray(d["Y"], dtype=np.float64)
        z = np.ascontiguousarray(d["Z"], dtype=np.float64)
        ref_den = d["DEN"]
        ref_vx = d["VX"]
        has_ref = True
    else:
        # Self-contained test grid on supercomputer
        xs = np.linspace(-10.0, 20.0, 61)
        ys = np.linspace(-30.0, 30.0, 121)
        X2d, Y2d = np.meshgrid(xs, ys, indexing="ij")
        x = np.ascontiguousarray(X2d.ravel(), dtype=np.float64)
        y = np.ascontiguousarray(Y2d.ravel(), dtype=np.float64)
        z = np.zeros_like(x)
        has_ref = False

    n = len(x)
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

    print(f"  {n:,} grid points evaluated in: {dt_ms:.2f} ms")
    if has_ref:
        max_diff_den = np.max(np.abs(den - ref_den))
        max_diff_vx = np.max(np.abs(vx - ref_vx))
        print(f"  Max diff vs reference .dat: DEN={max_diff_den:.2e}, VX={max_diff_vx:.2e}")
        assert max_diff_den < 1e-3 and max_diff_vx < 1e-3
    else:
        assert np.any(flg == 1), "Must have magnetosheath points (flag==1)"
        assert np.any(flg == 2), "Must have solar wind points (flag==2)"
        print(f"  Self-contained sanity check passed (MSH points: {np.sum(flg==1):,}, Solar wind: {np.sum(flg==2):,})")


def test_2_omni_and_coords():
    print("\n--- [Test 2] NASA SPDF 5-min OMNI Loader & GSM<->GSE Verification ---")
    import os
    from omni_loader import generate_synthetic_omni
    local_omni = "data/omni_5min/omni_5min2018.asc"
    if os.path.exists(local_omni):
        df = load_and_preprocess_omni(year=2018, filepath=local_omni, month_filter=1)
        print(f"  2018-01 5-min records: {len(df)} (Expected: 8928)")
        assert len(df) == 8928, f"Expected 8928 5-min records in Jan 2018, got {len(df)}"
    else:
        # Offline mode on supercomputer compute nodes without internet access
        print("  Local OMNI file not found. Using offline synthetic 5-min OMNI data for verification...")
        df = generate_synthetic_omni(year=2018, n_days=3)

    rep = verify_coordinate_transforms(sample_df=df)
    for k, v in rep.items():
        print(f"  {k}: {v}")
    assert rep["passed"], "Coordinate transform verification failed!"


def test_3_end_to_end_pipeline():
    print("\n--- [Test 3] End-to-End Multi-Worker Pipeline & NetCDF4 Verification ---")
    import os
    local_omni = "data/omni_5min/omni_5min2018.asc"
    omni_src = local_omni if os.path.exists(local_omni) else "SYNTHETIC"

    summary = run_annual_pipeline(
        year=2018,
        months=[1],
        total_cores=8,
        workers_per_month=8,
        concurrent_months=1,
        dx=0.5,
        out_dir="test_nc",
        omni_file=omni_src,
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
