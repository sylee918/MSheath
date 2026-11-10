#!/usr/bin/env python3
"""
plot_subsolar_radial_profiles.py
================================
Plots 1D Radial Profiles along the Sun-Earth line (Subsolar axis, GSE X, with Y=0, Z=0)
for Proton Number Density (Np) and Temperature (Tp), comparing Annual Mean and Standard Deviation (Mean ± 1-Sigma).

Also overlays:
  - Mean Bow Shock standoff (R_BS,0) and Magnetopause standoff (R_MP,0)
  - 10th-90th percentile boundary motion range
  - 4 Seasonal/Equinox profiles or IMF Bz polarity comparison
"""

import os
import argparse
import numpy as np
import netCDF4 as nc
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_profiles(summary_path: str, out_dir: str = "figures", year: int = 2018):
    os.makedirs(out_dir, exist_ok=True)
    with nc.Dataset(summary_path, "r") as ds:
        x = np.array(ds.variables["x_gse"][:], dtype=np.float64)
        y = np.array(ds.variables["y_gse"][:], dtype=np.float64)
        iy0 = int(np.argmin(np.abs(y - 0.0)))

        # 1. Annual Profiles along Y=0 (Equatorial plane)
        np_mean = np.array(ds.variables["annual_eq_np_mean"][:, iy0], dtype=np.float64)
        np_std = np.array(ds.variables["annual_eq_np_std"][:, iy0], dtype=np.float64)
        np_med = np.array(ds.variables["annual_eq_np_median"][:, iy0], dtype=np.float64)

        tk_mean = np.array(ds.variables["annual_eq_temp_k_mean"][:, iy0], dtype=np.float64) / 1e6
        tk_std = np.array(ds.variables["annual_eq_temp_k_std"][:, iy0], dtype=np.float64) / 1e6
        tk_med = np.array(ds.variables["annual_eq_temp_k_median"][:, iy0], dtype=np.float64) / 1e6

        # Flow velocity components along X
        vx_mean = np.array(ds.variables["annual_eq_vx_gse_mean"][:, iy0], dtype=np.float64)
        vx_std = np.array(ds.variables["annual_eq_vx_gse_std"][:, iy0], dtype=np.float64)

        # MSH probability profile
        msh_frac = np.array(ds.variables["annual_eq_msh_fraction"][:, iy0], dtype=np.float64) * 100.0

        # Subsolar boundary locations from 1D time series
        rbs_ts = np.array(ds.variables["subsolar_rbs_Re"][:], dtype=np.float64)
        rmp_ts = np.array(ds.variables["subsolar_rmp_Re"][:], dtype=np.float64)
        rbs_valid = rbs_ts[np.isfinite(rbs_ts)]
        rmp_valid = rmp_ts[np.isfinite(rmp_ts)]

        rbs_mean = float(np.mean(rbs_valid))
        rbs_p10, rbs_p90 = float(np.percentile(rbs_valid, 10)), float(np.percentile(rbs_valid, 90))
        rmp_mean = float(np.mean(rmp_valid))
        rmp_p10, rmp_p90 = float(np.percentile(rmp_valid, 10)), float(np.percentile(rmp_valid, 90))

        # Regime profiles (Southward vs Northward IMF)
        reg_np_msh = np.array(ds.variables["regime_eq_np_msh_mean"][:, :, iy0], dtype=np.float64)
        reg_tk_msh = np.array(ds.variables["regime_eq_temp_k_msh_mean"][:, :, iy0], dtype=np.float64) / 1e6

    # -------------------------------------------------------------
    # Figure 1: 3-Panel Profile (Density, Temperature, Flow Speed)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(11, 12), sharex=True, constrained_layout=True)
    fig.suptitle(
        f"Subsolar ($Y_{{\\mathrm{{GSE}}}}=0, Z_{{\\mathrm{{GSE}}}}=0$) Radial Profiles along Earth-Sun Line — {year}\n"
        f"Tsyganenko (2024, 2025) Empirical Model (Annual Mean $\\pm$ 1$\\sigma$ Fluctuation)",
        fontsize=13, fontweight="bold"
    )

    x_mask = x >= 0.0
    x_plot = x[x_mask]

    def add_boundary_overlays(ax):
        # Magnetopause
        ax.axvspan(rmp_p10, rmp_p90, color="#d95f02", alpha=0.15, label=f"$R_{{\\mathrm{{MP}},0}}$ Range (10-90%): [{rmp_p10:.1f}, {rmp_p90:.1f}] $R_E$")
        ax.axvline(rmp_mean, color="#d95f02", ls="--", lw=1.8, label=f"Mean $R_{{\\mathrm{{MP}},0}} = {rmp_mean:.2f}\ R_E$")
        # Bow Shock
        ax.axvspan(rbs_p10, rbs_p90, color="#1b9e77", alpha=0.15, label=f"$R_{{\\mathrm{{BS}},0}}$ Range (10-90%): [{rbs_p10:.1f}, {rbs_p90:.1f}] $R_E$")
        ax.axvline(rbs_mean, color="#1b9e77", ls="--", lw=1.8, label=f"Mean $R_{{\\mathrm{{BS}},0}} = {rbs_mean:.2f}\ R_E$")
        ax.grid(True, ls=":", alpha=0.5, color="black")

    # Panel 1: Proton Number Density (Np)
    ax1 = axes[0]
    add_boundary_overlays(ax1)
    np_p = np_mean[x_mask]
    np_s = np_std[x_mask]
    np_m = np_med[x_mask]

    ax1.plot(x_plot, np_p, color="#08519c", lw=2.5, label="Annual Mean $N_p$")
    ax1.fill_between(x_plot, np.maximum(0, np_p - np_s), np_p + np_s, color="#4292c6", alpha=0.35, label="$\\pm 1\\sigma$ Standard Deviation")
    ax1.plot(x_plot, np_m, color="#08306b", ls=":", lw=1.6, label="Annual Median $N_p$")

    # Secondary axis for MSH probability
    ax1_r = ax1.twinx()
    ax1_r.plot(x_plot, msh_frac[x_mask], color="#756bb1", ls="-.", lw=1.5, alpha=0.85, label="MSH Probability (%)")
    ax1_r.set_ylabel("MSH Residence Prob. [%]", color="#756bb1", fontsize=11)
    ax1_r.tick_params(axis="y", labelcolor="#756bb1")
    ax1_r.set_ylim(0, 105)

    ax1.set_ylabel("Proton Number Density $N_p$ [$\\mathrm{cm}^{-3}$]", fontsize=11)
    ax1.set_title("(a) Proton Density Compression & Stagnation across Subsolar Shock & Sheath", fontsize=11.5, loc="left")
    ax1.set_ylim(0, max(80, np.nanmax(np_p + np_s) * 1.05))
    ax1.legend(loc="upper right", framealpha=0.9, fontsize=9.5)

    # Panel 2: Proton Temperature (Tp)
    ax2 = axes[1]
    add_boundary_overlays(ax2)
    tk_p = tk_mean[x_mask]
    tk_s = tk_std[x_mask]
    tk_m = tk_med[x_mask]

    ax2.plot(x_plot, tk_p, color="#bd0026", lw=2.5, label="Annual Mean $T_p$")
    ax2.fill_between(x_plot, np.maximum(0, tk_p - tk_s), tk_p + tk_s, color="#fb6a4a", alpha=0.35, label="$\\pm 1\\sigma$ Standard Deviation")
    ax2.plot(x_plot, tk_m, color="#800026", ls=":", lw=1.6, label="Annual Median $T_p$")
    ax2.set_ylabel("Proton Temperature $T_p$ [MK]", fontsize=11)
    ax2.set_title("(b) Shock Heating & Temperature Dissipation Profile", fontsize=11.5, loc="left")
    ax2.set_ylim(0, max(5.0, np.nanmax(tk_p + tk_s) * 1.05))
    ax2.legend(loc="upper right", framealpha=0.9, fontsize=9.5)

    # Panel 3: Inflow Velocity (Vx) Deceleration
    ax3 = axes[2]
    add_boundary_overlays(ax3)
    vx_p = vx_mean[x_mask]
    vx_s = vx_std[x_mask]

    ax3.plot(x_plot, vx_p, color="#238b45", lw=2.5, label="Annual Mean $V_x$ (Inflow)")
    ax3.fill_between(x_plot, vx_p - vx_s, vx_p + vx_s, color="#74c476", alpha=0.35, label="$\\pm 1\\sigma$ Standard Deviation")
    ax3.axhline(0, color="gray", lw=1.0, ls="-")
    ax3.set_ylabel("Flow Velocity $V_x$ [km/s]", fontsize=11)
    ax3.set_xlabel("Radial Distance from Earth Center along GSE X-Axis $X_{\\mathrm{GSE}}$ [$R_E$] (Sun $\\leftarrow$)", fontsize=11.5)
    ax3.set_title("(c) Solar Wind Deceleration across Bow Shock into Magnetopause Stagnation", fontsize=11.5, loc="left")
    ax3.set_xlim(5, 20)
    ax3.legend(loc="lower right", framealpha=0.9, fontsize=9.5)

    out_file1 = os.path.join(out_dir, f"fig6_{year}_subsolar_radial_profiles_np_temp_vx.png")
    fig.savefig(out_file1, dpi=220)
    plt.close(fig)
    print(f"  -> Saved: {out_file1}")

    # -------------------------------------------------------------
    # Figure 2: Physical Regimes Comparison along Nose Line
    # (Southward IMF vs Northward IMF vs High/Low Pdyn)
    # -------------------------------------------------------------
    fig2, (ax_a, ax_b) = plt.subplots(2, 1, figsize=(11, 8.5), sharex=True, constrained_layout=True)
    fig2.suptitle(f"Subsolar Profile Dependence on IMF $B_z$ and Solar Wind Dynamic Pressure — {year}", fontsize=13, fontweight="bold")

    reg_indices = [
        (0, "All-Year Mean", "black", "-"),
        (1, "Southward IMF ($B_z < -2$ nT)", "#e41a1c", "-"),
        (2, "Northward IMF ($B_z > +2$ nT)", "#377eb8", "--"),
        (3, "High $P_{\\mathrm{dyn}} > 2.5$ nPa", "#ff7f00", "-."),
        (4, "Low $P_{\\mathrm{dyn}} < 1.2$ nPa", "#4daf4a", ":"),
    ]

    add_boundary_overlays(ax_a)
    add_boundary_overlays(ax_b)

    for r_idx, label, color, ls in reg_indices:
        np_r = reg_np_msh[r_idx, x_mask]
        tk_r = reg_tk_msh[r_idx, x_mask]
        ax_a.plot(x_plot, np_r, color=color, ls=ls, lw=2.0, label=label)
        ax_b.plot(x_plot, tk_r, color=color, ls=ls, lw=2.0, label=label)

    ax_a.set_ylabel("MSH Density $N_p$ [$\\mathrm{cm}^{-3}$]", fontsize=11)
    ax_a.set_title("Proton Density Profiles by Upstream Driving Regime", fontsize=11.5, loc="left")
    ax_a.set_ylim(0, 60)
    ax_a.legend(loc="upper right", framealpha=0.9, fontsize=9.5)

    ax_b.set_ylabel("MSH Temperature $T_p$ [MK]", fontsize=11)
    ax_b.set_title("Proton Temperature Profiles by Upstream Driving Regime", fontsize=11.5, loc="left")
    ax_b.set_xlabel("GSE X-Axis Distance $X_{\\mathrm{GSE}}$ [$R_E$]", fontsize=11.5)
    ax_b.set_xlim(7, 18)
    ax_b.set_ylim(0, 4.5)
    ax_b.legend(loc="upper right", framealpha=0.9, fontsize=9.5)

    out_file2 = os.path.join(out_dir, f"fig7_{year}_subsolar_profiles_by_regime.png")
    fig2.savefig(out_file2, dpi=220)
    plt.close(fig2)
    print(f"  -> Saved: {out_file2}")


def main():
    parser = argparse.ArgumentParser(description="Plot Subsolar Radial Profiles of Np and Tp along X-axis.")
    parser.add_argument("--summary", type=str, default="summary_stats/MSH_GSE_2018_Summary.nc")
    parser.add_argument("--out-dir", type=str, default="figures")
    parser.add_argument("--year", type=int, default=None)
    args = parser.parse_args()

    year = args.year
    if year is None:
        import re
        m = re.search(r"(\d{4})", os.path.basename(args.summary))
        year = int(m.group(1)) if m else 2018

    plot_profiles(summary_path=args.summary, out_dir=args.out_dir, year=year)


if __name__ == "__main__":
    main()
