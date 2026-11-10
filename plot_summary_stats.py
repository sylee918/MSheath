#!/usr/bin/env python3
"""
plot_summary_stats.py
=====================
Generates publication-quality scientific figures from the compact summary file
(`summary_stats/MSH_GSE_2018_Summary.nc`) produced by `build_summary_stats.py`.

Generated Figures (saved to `figures/`):
  1. `fig1_annual_2d_overview.png`      : 2x4 panel Annual Mean MSH Np, Vmag (+ streamlines), Temp, and MSH Probability (EQ & MER)
  2. `fig2_dipole_tilt_asymmetry.png`   : Meridional (XZ_GSE) Np & Vmag for Positive Tilt (Summer), Equinox, Negative Tilt (Winter)
  3. `fig3_imf_bz_and_pdyn_regimes.png` : Equatorial (XY_GSE) response to Southward vs Northward IMF and High vs Low Pdyn
  4. `fig4_monthly_np_climatology.png`  : 12-month (3x4) Equatorial MSH Density climatology with monthly BS & MP boundaries
  5. `fig5_subsolar_standoff_stats.png` : Full-year Subsolar R_BS, R_MP, MSH thickness distributions & monthly variations
"""

import os
import argparse
import numpy as np
import netCDF4 as nc
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle


def draw_earth(ax, radius: float = 1.0):
    """Draw Earth with dayside (+X) white and nightside (-X) black."""
    earth_bg = Circle((0, 0), radius, facecolor="white", edgecolor="black", lw=1.0, zorder=10)
    night = Wedge((0, 0), radius, 90, 270, facecolor="black", edgecolor="black", lw=0.8, zorder=11)
    ax.add_patch(earth_bg)
    ax.add_patch(night)


def overlay_mean_boundaries(ax, x_1d, y_1d, rbs_2d, rmp_2d, color_bs="cyan", color_mp="magenta"):
    """Plot mean Bow Shock (r == rbs) and Magnetopause (r == rmp) contours on a 2D plane."""
    X, Y = np.meshgrid(x_1d, y_1d, indexing="ij")
    R = np.sqrt(X ** 2 + Y ** 2)
    diff_bs = R - rbs_2d
    diff_mp = R - rmp_2d
    if np.any(np.isfinite(diff_bs)):
        try:
            ax.contour(X, Y, diff_bs, levels=[0.0], colors=[color_bs], linewidths=1.5, linestyles="--", zorder=8)
        except Exception:
            pass
    if np.any(np.isfinite(diff_mp)):
        try:
            ax.contour(X, Y, diff_mp, levels=[0.0], colors=[color_mp], linewidths=1.6, linestyles="-", zorder=8)
        except Exception:
            pass


def plot_fig1_annual_overview(ds: nc.Dataset, out_dir: str, year: int):
    x = np.array(ds.variables["x_gse"][:])
    y = np.array(ds.variables["y_gse"][:])
    z = np.array(ds.variables["z_gse"][:])

    fig, axes = plt.subplots(2, 4, figsize=(20, 10), constrained_layout=True)
    fig.suptitle(f"Tsyganenko Empirical Magnetosheath Model — {year} Annual GSE Distributions", fontsize=15, fontweight="bold")

    for row, (plane, coord2, plane_label, v2_name) in enumerate([
        ("eq", y, "Equatorial Plane ($Z_{\\mathrm{GSE}}=0$)", "vy_gse"),
        ("mer", z, "Meridional Plane ($Y_{\\mathrm{GSE}}=0$)", "vz_gse"),
    ]):
        X, C2 = np.meshgrid(x, coord2, indexing="ij")
        rbs = np.array(ds.variables[f"annual_{plane}_rbs_mean"][:])
        rmp = np.array(ds.variables[f"annual_{plane}_rmp_mean"][:])
        msh_frac = np.array(ds.variables[f"annual_{plane}_msh_fraction"][:])

        # Mask cells with < 5% MSH presence for clean MSH-only plots
        msh_mask = msh_frac >= 0.05
        np_map = np.where(msh_mask, np.array(ds.variables[f"annual_{plane}_np_msh_mean"][:]), np.nan)
        vm_map = np.where(msh_mask, np.array(ds.variables[f"annual_{plane}_vmag_msh_mean"][:]), np.nan)
        tk_map = np.where(msh_mask, np.array(ds.variables[f"annual_{plane}_temp_k_msh_mean"][:]) / 1e6, np.nan)
        vx_map = np.where(msh_mask, np.array(ds.variables[f"annual_{plane}_vx_gse_msh_mean"][:]), np.nan)
        vy_map = np.where(msh_mask, np.array(ds.variables[f"annual_{plane}_{v2_name}_msh_mean"][:]), np.nan)

        panels = [
            (np_map, "viridis", 0, 35, "$N_p$ [$\\mathrm{cm}^{-3}$]", "Proton Density (MSH)"),
            (vm_map, "plasma", 50, 450, "$|V|$ [km/s]", "Flow Speed & Streamlines"),
            (tk_map, "inferno", 0.2, 5.0, "$T_p$ [MK]", "Proton Temperature (MSH)"),
            (msh_frac * 100.0, "YlGnBu", 0, 100, "MSH Occurrence [%]", "MSH Residence Probability"),
        ]

        for col, (data_2d, cmap, vmin, vmax, cbar_label, title_str) in enumerate(panels):
            ax = axes[row, col]
            ax.set_facecolor("#e8e8e8")
            pcm = ax.pcolormesh(X, C2, data_2d, cmap=cmap, vmin=vmin, vmax=vmax, shading="auto")
            overlay_mean_boundaries(ax, x, coord2, rbs, rmp, color_bs="#00ffff", color_mp="#ff00ff")
            draw_earth(ax, radius=1.0)

            # Quiver vectors on velocity panel
            if col == 1:
                step = 4
                ax.quiver(
                    X[::step, ::step], C2[::step, ::step],
                    vx_map[::step, ::step], vy_map[::step, ::step],
                    color="white", alpha=0.75, scale=4500, width=0.004, zorder=9
                )

            if plane == "mer":
                ax.axvspan(x[0], 0.0, color="#c0c0c0", alpha=0.5, zorder=2, label="$X_{\\mathrm{GSE}}<0$ Skipped")

            ax.set_xlim(x[-1], x[0])  # Sun (+X) to the left
            ax.set_ylim(-25, 25)
            ax.set_aspect("equal")
            ax.grid(True, ls=":", alpha=0.4, color="black")
            ax.set_xlabel("$X_{\\mathrm{GSE}}$ [$R_E$] (Sun $\\leftarrow$)")
            ax.set_ylabel("$Y_{\\mathrm{GSE}}$ [$R_E$]" if plane == "eq" else "$Z_{\\mathrm{GSE}}$ [$R_E$]")
            ax.set_title(f"{plane_label}\n{title_str}", fontsize=11)
            fig.colorbar(pcm, ax=ax, shrink=0.82, label=cbar_label)

    out_path = os.path.join(out_dir, f"fig1_{year}_annual_2d_overview.png")
    fig.savefig(out_path, dpi=220)
    plt.close(fig)
    print(f"  -> Saved: {out_path}")


def plot_fig2_dipole_tilt(ds: nc.Dataset, out_dir: str, year: int):
    x = np.array(ds.variables["x_gse"][:])
    z = np.array(ds.variables["z_gse"][:])
    X, Z = np.meshgrid(x, z, indexing="ij")

    reg_counts = np.array(ds.variables["regime_step_count"][:])
    reg_np = np.array(ds.variables["regime_mer_np_msh_mean"][:])
    reg_vm = np.array(ds.variables["regime_mer_vmag_msh_mean"][:])
    reg_frac = np.array(ds.variables["regime_mer_msh_fraction"][:])
    reg_rbs = np.array(ds.variables["regime_mer_rbs_mean"][:])
    reg_rmp = np.array(ds.variables["regime_mer_rmp_mean"][:])

    tilt_indices = [
        (5, "Northern Summer ($\\psi > +15^\\circ$)"),
        (7, "Near Equinox ($|\\psi| \\leq 5^\\circ$)"),
        (6, "Northern Winter ($\\psi < -15^\\circ$)"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(15, 9.5), constrained_layout=True)
    fig.suptitle(f"Dipole Tilt Seasonal Asymmetry in GSE Meridional Plane ($Y_{{\\mathrm{{GSE}}}}=0$) — {year}", fontsize=14, fontweight="bold")

    for col, (r_idx, label) in enumerate(tilt_indices):
        n_steps = int(reg_counts[r_idx])
        mask = reg_frac[r_idx] >= 0.05
        d_np = np.where(mask, reg_np[r_idx], np.nan)
        d_vm = np.where(mask, reg_vm[r_idx], np.nan)

        for row, (arr, cmap, vmin, vmax, unit_lbl, var_title) in enumerate([
            (d_np, "viridis", 0, 35, "$N_p$ [$\\mathrm{cm}^{-3}$]", "Proton Density"),
            (d_vm, "plasma", 50, 450, "$|V|$ [km/s]", "Bulk Speed"),
        ]):
            ax = axes[row, col]
            ax.set_facecolor("#e8e8e8")
            pcm = ax.pcolormesh(X, Z, arr, cmap=cmap, vmin=vmin, vmax=vmax, shading="auto")
            overlay_mean_boundaries(ax, x, z, reg_rbs[r_idx], reg_rmp[r_idx])
            draw_earth(ax)
            ax.axvspan(x[0], 0.0, color="#c0c0c0", alpha=0.5, zorder=2)
            ax.set_xlim(10, -15)
            ax.set_ylim(-22, 22)
            ax.set_aspect("equal")
            ax.grid(True, ls=":", alpha=0.4, color="black")
            ax.set_xlabel("$X_{\\mathrm{GSE}}$ [$R_E$]")
            ax.set_ylabel("$Z_{\\mathrm{GSE}}$ [$R_E$]")
            ax.set_title(f"{label}\n{var_title} ($N={n_steps:,}$ steps)", fontsize=10.5)
            fig.colorbar(pcm, ax=ax, shrink=0.82, label=unit_lbl)

    out_path = os.path.join(out_dir, f"fig2_{year}_dipole_tilt_asymmetry.png")
    fig.savefig(out_path, dpi=220)
    plt.close(fig)
    print(f"  -> Saved: {out_path}")


def plot_fig3_imf_and_pdyn(ds: nc.Dataset, out_dir: str, year: int):
    x = np.array(ds.variables["x_gse"][:])
    y = np.array(ds.variables["y_gse"][:])
    X, Y = np.meshgrid(x, y, indexing="ij")

    reg_counts = np.array(ds.variables["regime_step_count"][:])
    reg_np = np.array(ds.variables["regime_eq_np_msh_mean"][:])
    reg_frac = np.array(ds.variables["regime_eq_msh_fraction"][:])
    reg_rbs = np.array(ds.variables["regime_eq_rbs_mean"][:])
    reg_rmp = np.array(ds.variables["regime_eq_rmp_mean"][:])

    configs = [
        (1, "Southward IMF ($B_z < -2$ nT)"),
        (2, "Northward IMF ($B_z > +2$ nT)"),
        (3, "High $P_{\\mathrm{dyn}}$ ($> 2.5$ nPa)"),
        (4, "Low $P_{\\mathrm{dyn}}$ ($< 1.2$ nPa)"),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(19, 5.2), constrained_layout=True)
    fig.suptitle(f"Equatorial Magnetosheath Response to IMF $B_z$ and Solar Wind $P_{{\\mathrm{{dyn}}}}$ — {year}", fontsize=14, fontweight="bold")

    for col, (r_idx, label) in enumerate(configs):
        ax = axes[col]
        ax.set_facecolor("#e8e8e8")
        n_steps = int(reg_counts[r_idx])
        mask = reg_frac[r_idx] >= 0.05
        d_np = np.where(mask, reg_np[r_idx], np.nan)

        pcm = ax.pcolormesh(X, Y, d_np, cmap="viridis", vmin=0, vmax=40, shading="auto")
        overlay_mean_boundaries(ax, x, y, reg_rbs[r_idx], reg_rmp[r_idx])
        draw_earth(ax)
        ax.set_xlim(10, -20)
        ax.set_ylim(-25, 25)
        ax.set_aspect("equal")
        ax.grid(True, ls=":", alpha=0.4, color="black")
        ax.set_xlabel("$X_{\\mathrm{GSE}}$ [$R_E$]")
        ax.set_ylabel("$Y_{\\mathrm{GSE}}$ [$R_E$]")
        ax.set_title(f"{label}\n$N_p$ ($N={n_steps:,}$ steps)", fontsize=11)
        fig.colorbar(pcm, ax=ax, shrink=0.82, label="$N_p$ [$\\mathrm{cm}^{-3}$]")

    out_path = os.path.join(out_dir, f"fig3_{year}_imf_bz_and_pdyn_regimes.png")
    fig.savefig(out_path, dpi=220)
    plt.close(fig)
    print(f"  -> Saved: {out_path}")


def plot_fig4_monthly_climatology(ds: nc.Dataset, out_dir: str, year: int):
    x = np.array(ds.variables["x_gse"][:])
    y = np.array(ds.variables["y_gse"][:])
    X, Y = np.meshgrid(x, y, indexing="ij")

    m_np = np.array(ds.variables["monthly_eq_np_msh_mean"][:])
    m_frac = np.array(ds.variables["monthly_eq_msh_fraction"][:])
    m_rbs = np.array(ds.variables["monthly_eq_rbs_mean"][:])
    m_rmp = np.array(ds.variables["monthly_eq_rmp_mean"][:])
    m_vc = np.array(ds.variables["monthly_eq_valid_count"][:])

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig, axes = plt.subplots(3, 4, figsize=(18, 13.5), constrained_layout=True)
    fig.suptitle(f"Monthly GSE Equatorial Magnetosheath Proton Density Climatology — {year}", fontsize=15, fontweight="bold")

    pcm = None
    for idx in range(12):
        ax = axes[idx // 4, idx % 4]
        ax.set_facecolor("#e8e8e8")
        n_valid = int(np.max(m_vc[idx]))
        mask = m_frac[idx] >= 0.05
        arr = np.where(mask, m_np[idx], np.nan)
        pcm = ax.pcolormesh(X, Y, arr, cmap="viridis", vmin=0, vmax=35, shading="auto")
        overlay_mean_boundaries(ax, x, y, m_rbs[idx], m_rmp[idx])
        draw_earth(ax)
        ax.set_xlim(10, -20)
        ax.set_ylim(-25, 25)
        ax.set_aspect("equal")
        ax.grid(True, ls=":", alpha=0.35, color="black")
        ax.set_title(f"{year}-{idx+1:02d} ({month_names[idx]}) | Valid={n_valid:,}", fontsize=10.5)
        if idx // 4 == 2:
            ax.set_xlabel("$X_{\\mathrm{GSE}}$ [$R_E$]")
        if idx % 4 == 0:
            ax.set_ylabel("$Y_{\\mathrm{GSE}}$ [$R_E$]")

    if pcm is not None:
        fig.colorbar(pcm, ax=axes.ravel().tolist(), shrink=0.6, pad=0.015, label="Mean MSH $N_p$ [$\\mathrm{cm}^{-3}$]")

    out_path = os.path.join(out_dir, f"fig4_{year}_monthly_np_climatology.png")
    fig.savefig(out_path, dpi=220)
    plt.close(fig)
    print(f"  -> Saved: {out_path}")


def plot_fig5_subsolar_timeseries(ds: nc.Dataset, out_dir: str, year: int):
    ts_month = np.array(ds.variables["ts_month"][:])
    rbs = np.array(ds.variables["subsolar_rbs_Re"][:])
    rmp = np.array(ds.variables["subsolar_rmp_Re"][:])
    dr = np.array(ds.variables["subsolar_msh_thickness_Re"][:])
    sub_np = np.array(ds.variables["subsolar_msh_np"][:])
    pdyn = np.array(ds.variables["sw_pdyn_npa"][:])

    fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
    fig.suptitle(f"Subsolar Magnetosheath Boundaries ($R_{{\\mathrm{{BS}},0}}$, $R_{{\\mathrm{{MP}},0}}$) & Plasma Statistics — {year}", fontsize=14, fontweight="bold")

    # Panel 1: Histograms of R_MP0, R_BS0, and Thickness dR
    ax = axes[0, 0]
    v_rmp = rmp[np.isfinite(rmp)]
    v_rbs = rbs[np.isfinite(rbs)]
    v_dr = dr[np.isfinite(dr)]
    if len(v_rmp) > 0:
        ax.hist(v_rmp, bins=60, alpha=0.7, color="#d95f02", label=f"$R_{{\\mathrm{{MP}},0}}$ (mean={np.mean(v_rmp):.2f} $R_E$)")
    if len(v_rbs) > 0:
        ax.hist(v_rbs, bins=60, alpha=0.7, color="#1b9e77", label=f"$R_{{\\mathrm{{BS}},0}}$ (mean={np.mean(v_rbs):.2f} $R_E$)")
    if len(v_dr) > 0:
        ax.hist(v_dr, bins=50, alpha=0.7, color="#7570b3", label=f"$\\Delta R_{{\\mathrm{{MSH}}}}$ (mean={np.mean(v_dr):.2f} $R_E$)")
    ax.set_xlabel("Radial Distance / Thickness [$R_E$]")
    ax.set_ylabel("5-min Timestep Count")
    ax.set_title("Subsolar Boundary Standoff & MSH Thickness Distributions")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 2: Monthly Medians and IQR (25%-75%) of R_BS0 and R_MP0
    ax = axes[0, 1]
    months = np.arange(1, 13)
    rbs_med, rbs_p25, rbs_p75 = [], [], []
    rmp_med, rmp_p25, rmp_p75 = [], [], []
    for m in months:
        sel_bs = rbs[(ts_month == m) & np.isfinite(rbs)]
        sel_mp = rmp[(ts_month == m) & np.isfinite(rmp)]
        if len(sel_bs) > 0:
            rbs_med.append(np.median(sel_bs))
            rbs_p25.append(np.percentile(sel_bs, 25))
            rbs_p75.append(np.percentile(sel_bs, 75))
        else:
            rbs_med.append(np.nan); rbs_p25.append(np.nan); rbs_p75.append(np.nan)
        if len(sel_mp) > 0:
            rmp_med.append(np.median(sel_mp))
            rmp_p25.append(np.percentile(sel_mp, 25))
            rmp_p75.append(np.percentile(sel_mp, 75))
        else:
            rmp_med.append(np.nan); rmp_p25.append(np.nan); rmp_p75.append(np.nan)

    ax.plot(months, rbs_med, "o-", color="#1b9e77", lw=2, label="Bow Shock $R_{\\mathrm{BS},0}$ (Median & IQR)")
    ax.fill_between(months, rbs_p25, rbs_p75, color="#1b9e77", alpha=0.25)
    ax.plot(months, rmp_med, "s-", color="#d95f02", lw=2, label="Magnetopause $R_{\\mathrm{MP},0}$ (Median & IQR)")
    ax.fill_between(months, rmp_p25, rmp_p75, color="#d95f02", alpha=0.25)
    ax.set_xticks(months)
    ax.set_xlabel("Month of Year")
    ax.set_ylabel("Subsolar Standoff Distance [$R_E$]")
    ax.set_title("Monthly Subsolar Bow Shock & Magnetopause Variations")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 3: Subsolar MSH Np vs Solar Wind Pdyn
    ax = axes[1, 0]
    ok = np.isfinite(pdyn) & np.isfinite(sub_np) & (pdyn > 0) & (pdyn < 15)
    if np.any(ok):
        hb = ax.hexbin(pdyn[ok], sub_np[ok], gridsize=45, cmap="YlOrRd", mincnt=1, bins="log")
        fig.colorbar(hb, ax=ax, label="$\\log_{10}(\\mathrm{Count})$")
    ax.set_xlabel("Solar Wind Dynamic Pressure $P_{\\mathrm{dyn}}$ [nPa]")
    ax.set_ylabel("Subsolar Magnetosheath Mean $N_p$ [$\\mathrm{cm}^{-3}$]")
    ax.set_title("Subsolar MSH Density vs. Solar Wind $P_{\\mathrm{dyn}}$")
    ax.grid(True, alpha=0.3)

    # Panel 4: Subsolar Standoff Distance vs Pdyn
    ax = axes[1, 1]
    ok2 = np.isfinite(pdyn) & np.isfinite(rmp) & np.isfinite(rbs) & (pdyn > 0.2) & (pdyn < 12)
    if np.any(ok2):
        ax.scatter(pdyn[ok2][::5], rbs[ok2][::5], s=3, alpha=0.25, color="#1b9e77", label="$R_{\\mathrm{BS},0}$")
        ax.scatter(pdyn[ok2][::5], rmp[ok2][::5], s=3, alpha=0.25, color="#d95f02", label="$R_{\\mathrm{MP},0}$")
    ax.set_xlabel("Solar Wind Dynamic Pressure $P_{\\mathrm{dyn}}$ [nPa]")
    ax.set_ylabel("Subsolar Standoff Distance [$R_E$]")
    ax.set_title("Boundary Compression vs. Dynamic Pressure")
    ax.legend(markerscale=4)
    ax.grid(True, alpha=0.3)

    out_path = os.path.join(out_dir, f"fig5_{year}_subsolar_standoff_stats.png")
    fig.savefig(out_path, dpi=220)
    plt.close(fig)
    print(f"  -> Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot GSE Magnetosheath Summary Statistics.")
    parser.add_argument(
        "--summary",
        type=str,
        default="summary_stats/MSH_GSE_2018_Summary.nc",
        help="Path to summary NetCDF file (default: summary_stats/MSH_GSE_2018_Summary.nc)",
    )
    parser.add_argument("--out-dir", type=str, default="figures", help="Directory to save generated plots")
    parser.add_argument("--year", type=int, default=2018, help="Target year")
    args = parser.parse_args()

    if not os.path.isfile(args.summary):
        raise FileNotFoundError(f"Summary file not found: {args.summary}")

    os.makedirs(args.out_dir, exist_ok=True)
    print(f"[Plotter] Reading summary file: {args.summary}")
    with nc.Dataset(args.summary, "r") as ds:
        plot_fig1_annual_overview(ds, args.out_dir, args.year)
        plot_fig2_dipole_tilt(ds, args.out_dir, args.year)
        plot_fig3_imf_and_pdyn(ds, args.out_dir, args.year)
        plot_fig4_monthly_climatology(ds, args.out_dir, args.year)
        plot_fig5_subsolar_timeseries(ds, args.out_dir, args.year)
    print("[Plotter] All 5 figures generated successfully!")


if __name__ == "__main__":
    main()
