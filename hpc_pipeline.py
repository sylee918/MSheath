"""
hpc_pipeline.py
===============
40-Core HPC Parallel Orchestrator for Monthly GSE 2D Magnetosheath Distributions.

Features:
  - Splits annual 5-minute OMNI datasets into 12 Monthly Chunks (YYYY-MM).
  - Assigns `workers_per_month` (default: 3 CPU workers per month, or up to 40 total cores)
    using `concurrent.futures.ProcessPoolExecutor` to parallelize CPU-bound coordinate
    transformations and Fortran (`libmsh.so`) 2D grid evaluations.
  - Explicitly releases memory (`del` + `gc.collect()`) after each monthly NetCDF4 write
    to prevent Out-Of-Memory (OOM) during multi-year HPC batch runs.
"""

import os
import gc
import time
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Optional, Tuple, Dict, Any
import numpy as np
import pandas as pd

from omni_loader import load_and_preprocess_omni, split_by_month
from coord_transform import verify_coordinate_transforms
from grid_engine import GridConfig, evaluate_time_chunk, compute_monthly_statistics
from nc_writer import save_monthly_netcdf


def _worker_eval_subchunk(args: Tuple[int, pd.DataFrame, GridConfig, str]) -> Tuple[int, Dict[str, Any]]:
    """Worker entrypoint for evaluating a temporal sub-chunk of a month."""
    sub_idx, df_sub, cfg, lib_path = args
    res = evaluate_time_chunk(df_sub, cfg, lib_path=lib_path)
    return sub_idx, res


def _merge_subchunks(sub_results: List[Tuple[int, Dict[str, Any]]]) -> Dict[str, Any]:
    """Concatenate ordered temporal sub-chunk results into a single monthly dictionary."""
    sub_results.sort(key=lambda x: x[0])
    if len(sub_results) == 1:
        return sub_results[0][1]

    first = sub_results[0][1]
    merged = {
        "x_axis": first["x_axis"],
        "y_axis": first["y_axis"],
        "z_axis": first["z_axis"],
    }

    time_keys = [
        "unix_time", "quality_flag", "psi_deg", "gsm_gse_angle_deg",
        "eq_np", "eq_temp_k", "eq_vx_gse", "eq_vy_gse", "eq_vz_gse", "eq_vmag", "eq_rbs", "eq_rmp", "eq_flag",
        "mer_np", "mer_temp_k", "mer_vx_gse", "mer_vy_gse", "mer_vz_gse", "mer_vmag", "mer_rbs", "mer_rmp", "mer_flag",
    ]
    for k in time_keys:
        merged[k] = np.concatenate([r[k] for _, r in sub_results], axis=0)

    return merged


def process_single_month(
    year: int,
    month: int,
    df_month: pd.DataFrame,
    cfg: GridConfig,
    out_dir: str,
    workers_for_month: int = 3,
    executor: Optional[ProcessPoolExecutor] = None,
    lib_path: str = "./libmsh.so",
) -> Dict[str, Any]:
    """
    Process one monthly chunk (YYYY-MM) using `workers_for_month` CPU workers,
    compute cell-level statistics, write `MSH_GSE_YYYY-MM.nc`, and free RAM.
    """
    t0 = time.perf_counter()
    n_steps = len(df_month)
    valid_steps = int(np.sum(df_month["quality_flag"] > 0))

    # Split monthly dataframe into `workers_for_month` contiguous sub-chunks
    n_splits = max(1, min(workers_for_month, n_steps))
    indices = np.array_split(np.arange(n_steps), n_splits)
    tasks = [
        (idx, df_month.iloc[idxs].copy().reset_index(drop=True), cfg, lib_path)
        for idx, idxs in enumerate(indices)
        if len(idxs) > 0
    ]

    if executor is not None and len(tasks) > 1:
        futures = [executor.submit(_worker_eval_subchunk, t) for t in tasks]
        sub_results = [f.result() for f in futures]
    elif len(tasks) > 1:
        with ProcessPoolExecutor(max_workers=len(tasks)) as local_pool:
            futures = [local_pool.submit(_worker_eval_subchunk, t) for t in tasks]
            sub_results = [f.result() for f in futures]
    else:
        sub_results = [_worker_eval_subchunk(tasks[0])]

    chunk_res = _merge_subchunks(sub_results)
    del sub_results

    # Compute monthly cell statistics (Mean, Median, Std, Counts)
    stats = compute_monthly_statistics(chunk_res)

    # Write compressed NetCDF4 output
    nc_path = save_monthly_netcdf(
        year=year,
        month=month,
        df_month=df_month,
        chunk_res=chunk_res,
        stats=stats,
        out_dir=out_dir,
    )
    file_mb = os.path.getsize(nc_path) / (1024 * 1024)
    dt = time.perf_counter() - t0

    # Explicit memory cleanup to prevent OOM over multi-month runs
    del chunk_res
    del stats
    gc.collect()

    return {
        "year": year,
        "month": month,
        "total_steps": n_steps,
        "valid_steps": valid_steps,
        "elapsed_sec": dt,
        "nc_path": nc_path,
        "size_mb": file_mb,
    }


def run_annual_pipeline(
    year: int,
    months: Optional[List[int]] = None,
    total_cores: int = 40,
    workers_per_month: int = 3,
    concurrent_months: int = 4,
    dx: float = 0.5,
    out_dir: str = "output_nc",
    omni_file: Optional[str] = None,
    max_steps_per_month: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Execute the full HPC pipeline for a given year (or selected months).
    """
    t_start = time.perf_counter()
    print("=" * 78)
    print(f"[HPC GSE MSheath Pipeline] Year={year} | Total Cores={total_cores} | "
          f"Workers/Month={workers_per_month} | Concurrent Months={concurrent_months} | Bin={dx} Re")
    print("=" * 78)

    # Step 1: Load and preprocess 5-minute OMNI data
    df_year = load_and_preprocess_omni(year=year, filepath=omni_file)
    print(f"[Stage 1] Loaded {len(df_year):,} 5-min OMNI records for {year}: "
          f"Observed={(df_year['quality_flag']==2).sum():,}, "
          f"Interpolated(<=15m)={(df_year['quality_flag']==1).sum():,}, "
          f"Missing={(df_year['quality_flag']==0).sum():,}")

    # Step 2: Verify GSM <-> GSE coordinate transformations
    v_rep = verify_coordinate_transforms(sample_df=df_year)
    print(f"[Stage 2] Coordinate Transform Verification: passed={v_rep['passed']} | "
          f"det_err={v_rep['max_orthogonality_error']:.2e} | "
          f"roundtrip_err={v_rep['max_roundtrip_error_Re']:.2e} Re | "
          f"OMNI B-field RMS diff={v_rep['omni_b_field_rms_diff_nT']:.4f} nT")
    if not v_rep["passed"]:
        raise RuntimeError(f"Coordinate transformation verification failed: {v_rep}")

    monthly_dfs = split_by_month(df_year)
    del df_year
    gc.collect()

    target_months = sorted(months) if months else sorted(monthly_dfs.keys())
    cfg = GridConfig(dx=dx, dy=dx, dz=dx, skip_meridional_nightside=True)

    # Step 3 & 4: Execute monthly chunks in parallel waves across the shared ProcessPool
    results_summary = []
    pool_size = min(total_cores, max(1, len(target_months) * workers_per_month))

    with ProcessPoolExecutor(max_workers=pool_size) as pool:
        # Process in waves of `concurrent_months` to bound peak RAM while saturating CPU cores
        for wave_start in range(0, len(target_months), concurrent_months):
            wave_months = target_months[wave_start : wave_start + concurrent_months]
            # Distribute available pool workers evenly across active months in this wave
            eff_workers = max(workers_per_month, pool_size // len(wave_months))

            wave_futures = {}
            for m in wave_months:
                df_m = monthly_dfs[m]
                if max_steps_per_month is not None:
                    df_m = df_m.iloc[:max_steps_per_month].copy().reset_index(drop=True)

                # Submit sub-chunks of month `m` to the shared process pool
                n_steps = len(df_m)
                n_splits = max(1, min(eff_workers, n_steps))
                indices = np.array_split(np.arange(n_steps), n_splits)
                sub_futs = [
                    pool.submit(
                        _worker_eval_subchunk,
                        (idx, df_m.iloc[idxs].copy().reset_index(drop=True), cfg, "./libmsh.so"),
                    )
                    for idx, idxs in enumerate(indices)
                    if len(idxs) > 0
                ]
                wave_futures[m] = ( time.perf_counter(), df_m, sub_futs )

            # Collect each month in the wave, compute stats, write NetCDF, and release RAM
            for m, (t_m0, df_m, sub_futs) in wave_futures.items():
                sub_res = [f.result() for f in sub_futs]
                chunk_res = _merge_subchunks(sub_res)
                del sub_res

                stats = compute_monthly_statistics(chunk_res)
                nc_path = save_monthly_netcdf(
                    year=year,
                    month=m,
                    df_month=df_m,
                    chunk_res=chunk_res,
                    stats=stats,
                    out_dir=out_dir,
                )
                sz_mb = os.path.getsize(nc_path) / (1024 * 1024)
                dt_m = time.perf_counter() - t_m0

                info = {
                    "year": year,
                    "month": m,
                    "total_steps": len(df_m),
                    "valid_steps": int(np.sum(df_m["quality_flag"] > 0)),
                    "elapsed_sec": dt_m,
                    "nc_path": nc_path,
                    "size_mb": sz_mb,
                }
                results_summary.append(info)
                print(f"  -> [Month {year:04d}-{m:02d}] Steps={info['valid_steps']}/{info['total_steps']} | "
                      f"Time={dt_m:.2f}s | Output={nc_path} ({sz_mb:.2f} MB)")

                del chunk_res, stats, df_m
                monthly_dfs.pop(m, None)
                gc.collect()

    total_dt = time.perf_counter() - t_start
    print("=" * 78)
    print(f"[HPC Pipeline Complete] Processed {len(results_summary)} month(s) in {total_dt:.2f} s.")
    print("=" * 78)
    return results_summary


def main():
    parser = argparse.ArgumentParser(
        description="40-Core HPC GSE Magnetosheath 2D Distribution Pipeline"
    )
    parser.add_argument("--year", type=int, default=2018, help="Target OMNI year (e.g., 2018)")
    parser.add_argument(
        "--months",
        type=int,
        nargs="+",
        default=None,
        help="Specific months to run (1..12). Default: all 12 months.",
    )
    parser.add_argument(
        "--total-cores", type=int, default=40, help="Total CPU cores on node (default: 40)"
    )
    parser.add_argument(
        "--workers-per-month",
        type=int,
        default=3,
        help="Workers allocated per monthly task (default: 3)",
    )
    parser.add_argument(
        "--concurrent-months",
        type=int,
        default=4,
        help="Number of months evaluated simultaneously per wave (default: 4)",
    )
    parser.add_argument(
        "--dx", type=float, default=0.5, help="Spatial grid resolution in R_E (default: 0.5)"
    )
    parser.add_argument(
        "--out-dir", type=str, default="output_nc", help="Output directory for NetCDF4 files"
    )
    parser.add_argument(
        "--omni-file", type=str, default=None, help="Optional path to local OMNI 5-min ASCII file"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="Optional cap on steps per month (for quick verification/benchmarking)",
    )
    args = parser.parse_args()

    run_annual_pipeline(
        year=args.year,
        months=args.months,
        total_cores=args.total_cores,
        workers_per_month=args.workers_per_month,
        concurrent_months=args.concurrent_months,
        dx=args.dx,
        out_dir=args.out_dir,
        omni_file=args.omni_file,
        max_steps_per_month=args.max_steps,
    )


if __name__ == "__main__":
    main()
