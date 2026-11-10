import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm

def run_fortran_grid(plane_type, vsw, dsw, wsw, bx, by, bz, psi, xmin, xmax, dx, gmin, gmax, dg, outfile):
    print(f"Running simulation: plane={plane_type}, Vsw={vsw}, Dsw={dsw}, Wsw={wsw}, B=({bx},{by},{bz}), Psi={psi}")
    input_str = f"{plane_type}\n{vsw} {dsw} {wsw} {bx} {by} {bz} {psi}\n{xmin} {xmax} {dx} {gmin} {gmax} {dg}\n{outfile}\n"
    if os.name == 'posix':
        res = subprocess.run("./msh_calc_grid", input=input_str, shell=True, capture_output=True, text=True)
    else:
        cmd = f"cd '/mnt/c/Users/slee122/OneDrive - NASA/Desktop/Work/JSokol/MSheath' && printf '{input_str}' | ./msh_calc_grid"
        res = subprocess.run(["wsl", "-d", "Ubuntu-22.04", "--", "bash", "-c", cmd], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Fortran run error: {res.stderr}")
    print(f"Generated {outfile}")

def draw_earth(ax, psi_deg=0.0, is_meridian=False):
    night = Wedge((0, 0), 1.0, 90, 270, fc='black', ec='black', lw=1.0, zorder=10)
    day = Wedge((0, 0), 1.0, 270, 90, fc='white', ec='black', lw=1.0, zorder=10)
    ax.add_patch(night)
    ax.add_patch(day)
    
    if is_meridian and abs(psi_deg) > 0.1:
        psi_rad = np.radians(psi_deg)
        mx = 2.4 * np.sin(psi_rad)
        mz = 2.4 * np.cos(psi_rad)
        ax.annotate('', xy=(mx, mz), xytext=(-mx*0.35, -mz*0.35),
                    arrowprops=dict(arrowstyle="->", color="gold", lw=2.2, zorder=12))
        ax.text(mx*1.2, mz*1.2, r'$\mathbf{M}$', color='gold', fontsize=11, fontweight='bold',
                ha='center', va='center', zorder=12)

def plot_six_panels_nosat(dat_file, save_path, plane_name, coord_label, title_info, psi_deg, xmin, xmax, gmin, gmax, vsw_val):
    print(f"Plotting saturation-free 6 panels for {plane_name} from {dat_file}...")
    data = np.genfromtxt(dat_file, names=True)
    
    xs = np.unique(data['X'])
    gs = np.unique(data['Z'] if coord_label == 'Z' else data['Y'])
    nx, ng = len(xs), len(gs)
    
    X = data['X'].reshape((nx, ng))
    G = (data['Z'] if coord_label == 'Z' else data['Y']).reshape((nx, ng))
    
    DEN = data['DEN'].reshape((nx, ng))
    T_MK = (data['T_K'] / 1e6).reshape((nx, ng))
    VMAG = data['VMAG'].reshape((nx, ng))
    VX = data['VX'].reshape((nx, ng))
    VY = data['VY'].reshape((nx, ng))
    VZ = data['VZ'].reshape((nx, ng))
    RBS = data['RBS'].reshape((nx, ng))
    RMP = data['RMP'].reshape((nx, ng))
    IFLAG = data['IFLAG'].reshape((nx, ng))
    
    R = np.sqrt(X**2 + G**2)
    is_meridian = (coord_label == 'Z')
    
    # Physical cap to prevent division-by-zero singularities at cusp boundaries
    # Maximum physical bulk speed in magnetosheath: ~1.35 * Vsw
    v_cap = max(vsw_val * 1.35, 480.0)
    
    # Clean speed values from rare division spikes
    vmag_clean = np.where(IFLAG == 1, np.clip(VMAG, 0.0, v_cap), VMAG)
    vx_clean = np.where(IFLAG == 1, np.clip(VX, -v_cap, v_cap), VX)
    vy_clean = np.where(IFLAG == 1, np.clip(VY, -v_cap, v_cap), VY)
    vz_clean = np.where(IFLAG == 1, np.clip(VZ, -v_cap, v_cap), VZ)
    
    # Mask magnetosphere (IFLAG == 0)
    den_p = np.where(IFLAG == 0, np.nan, DEN)
    t_p = np.where(IFLAG == 0, np.nan, T_MK)
    vmag_p = np.where(IFLAG == 0, np.nan, vmag_clean)
    vx_p = np.where(IFLAG == 0, np.nan, vx_clean)
    vy_p = np.where(IFLAG == 0, np.nan, vy_clean)
    vz_p = np.where(IFLAG == 0, np.nan, vz_clean)
    
    # Dynamic non-saturating range calculation based on 99.8th percentile + margin
    msh_mask = (IFLAG == 1)
    
    # 1. Density max: ensure all pixels are within range without saturation
    p998_den = np.nanpercentile(den_p[msh_mask], 99.5) if np.any(msh_mask) else 30.0
    den_max = np.ceil(p998_den / 10.0) * 10.0 + 10.0 # add 10 margin
    den_max = max(den_max, 40.0)
    
    # 2. Temperature max
    p998_t = np.nanpercentile(t_p[msh_mask], 99.5) if np.any(msh_mask) else 2.5
    t_max = np.ceil(p998_t * 2.0) / 2.0 + 0.5 # add 0.5 MK margin
    t_max = max(t_max, 2.5)
    
    # 3. Speed max: [0, v_cap]
    vmag_max = np.ceil(v_cap / 50.0) * 50.0
    
    # 4. Symmetric velocity limits: [-v_lim, +v_lim]
    # For Vx
    vx_max_abs = max(abs(np.nanmin(vx_p[msh_mask])), abs(np.nanmax(vx_p[msh_mask])), vsw_val)
    vx_lim = np.ceil(vx_max_abs / 50.0) * 50.0
    
    # For Vy
    vy_max_abs = max(abs(np.nanmin(vy_p[msh_mask])), abs(np.nanmax(vy_p[msh_mask]))) if np.any(msh_mask) else 100.0
    vy_lim = max(np.ceil(vy_max_abs / 25.0) * 25.0 + 25.0, 100.0)
    
    # For Vz
    vz_max_abs = max(abs(np.nanmin(vz_p[msh_mask])), abs(np.nanmax(vz_p[msh_mask]))) if np.any(msh_mask) else 100.0
    vz_lim = max(np.ceil(vz_max_abs / 25.0) * 25.0 + 25.0, 100.0)
    
    cmap_jet = plt.cm.jet.copy()
    cmap_jet.set_bad('midnightblue', 0.95)
    
    cmap_rdbu = plt.cm.RdBu_r.copy() # Blue negative, Red positive, White zero
    cmap_rdbu.set_bad('midnightblue', 0.95)
    
    fig, axes = plt.subplots(2, 3, figsize=(22, 13), dpi=300)
    
    def format_ax(ax, title, xlabel=True, ylabel=True):
        ax.contour(X, G, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
        ax.contour(X, G, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
        draw_earth(ax, psi_deg, is_meridian)
        ax.set_title(title, fontsize=12, fontweight='bold', pad=7)
        if xlabel:
            ax.set_xlabel(r'$X_{\mathrm{GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
        if ylabel:
            ax.set_ylabel(rf'${coord_label}_{{\mathrm{{GSM}}}}\ [R_E]$', fontsize=11, fontweight='bold')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(gmin, gmax)
        ax.set_aspect('equal')
        ax.grid(True, linestyle=':', alpha=0.35, color='gray')
    
    # (1) Density Np (jet, 0 to den_max)
    ax = axes[0, 0]
    n_levels = int(den_max / 2) + 1
    cf = ax.contourf(X, G, den_p, levels=np.linspace(0, den_max, 91), cmap=cmap_jet, extend='max')
    c_step = 10 if den_max <= 70 else 20
    c = ax.contour(X, G, den_p, levels=np.arange(c_step, den_max, c_step), colors='white', linewidths=0.5, alpha=0.6)
    ax.clabel(c, inline=True, fontsize=7.5, fmt='%.0f')
    format_ax(ax, r'(a) Proton Number Density $N_p$ [$\mathrm{cm^{-3}}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$N_p\ [\mathrm{cm^{-3}}]$', fontsize=11, fontweight='bold')
    
    # (2) Temperature T (jet, 0 to t_max)
    ax = axes[0, 1]
    cf = ax.contourf(X, G, t_p, levels=np.linspace(0, t_max, 91), cmap=cmap_jet, extend='max')
    t_step = 0.5 if t_max <= 4.0 else 1.0
    c = ax.contour(X, G, t_p, levels=np.arange(t_step, t_max, t_step), colors='white', linewidths=0.5, alpha=0.6)
    ax.clabel(c, inline=True, fontsize=7.5, fmt='%.1f')
    format_ax(ax, r'(b) Proton Temperature $T$ [$10^6\ \mathrm{K}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$T\ [10^6\ \mathrm{K}]$', fontsize=11, fontweight='bold')
    
    # (3) Speed |V| (jet, 0 to vmag_max) + Streamlines
    ax = axes[0, 2]
    cf = ax.contourf(X, G, vmag_p, levels=np.linspace(0, vmag_max, 91), cmap=cmap_jet, extend='max')
    vx_stream = np.where(IFLAG > 0, vx_clean, 0.0)
    vg_stream = np.where(IFLAG > 0, (vz_clean if is_meridian else vy_clean), 0.0)
    ax.streamplot(xs, gs, vx_stream.T, vg_stream.T, color='white', density=1.2, linewidth=0.7, arrowsize=0.9)
    format_ax(ax, r'(c) Flow Speed $|V|$ [$\mathrm{km/s}$] & Streamlines')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$|V|\ [\mathrm{km/s}]$', fontsize=11, fontweight='bold')
    
    # (4) Vx (RdBu_r, symmetric [-vx_lim, +vx_lim])
    ax = axes[1, 0]
    norm_vx = TwoSlopeNorm(vmin=-vx_lim, vcenter=0.0, vmax=vx_lim)
    cf = ax.contourf(X, G, vx_p, levels=np.linspace(-vx_lim, vx_lim, 91), cmap=cmap_rdbu, norm=norm_vx, extend='both')
    format_ax(ax, r'(d) Sun-Earth Flow Component $V_x$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_x\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=11, fontweight='bold')
    
    # (5) Vy (RdBu_r, symmetric [-vy_lim, +vy_lim])
    ax = axes[1, 1]
    norm_vy = TwoSlopeNorm(vmin=-vy_lim, vcenter=0.0, vmax=vy_lim)
    cf = ax.contourf(X, G, vy_p, levels=np.linspace(-vy_lim, vy_lim, 91), cmap=cmap_rdbu, norm=norm_vy, extend='both')
    format_ax(ax, r'(e) Dawn-Dusk Flow Component $V_y$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_y\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=11, fontweight='bold')
    
    # (6) Vz (RdBu_r, symmetric [-vz_lim, +vz_lim])
    ax = axes[1, 2]
    norm_vz = TwoSlopeNorm(vmin=-vz_lim, vcenter=0.0, vmax=vz_lim)
    cf = ax.contourf(X, G, vz_p, levels=np.linspace(-vz_lim, vz_lim, 91), cmap=cmap_rdbu, norm=norm_vz, extend='both')
    format_ax(ax, r'(f) North-South Flow Component $V_z$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_z\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=11, fontweight='bold')
    
    legend_elements = [
        Line2D([0], [0], color='cyan', lw=2.0, linestyle='-', label='Magnetopause (Lin et al. 2010)'),
        Line2D([0], [0], color='magenta', lw=2.0, linestyle='--', label='Bow Shock (Lu et al. 2019)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markeredgecolor='k', markersize=8, label='Earth')
    ]
    axes[0, 0].legend(handles=legend_elements, loc='upper left', fontsize=8.5, framealpha=0.9, facecolor='white')
    
    plt.suptitle(title_info, fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved figure: {save_path}")

if __name__ == '__main__':
    xmin = -10.0; xmax = 20.0; dx = 0.25
    gmin = -30.0; gmax = 30.0; dg = 0.25
    
    # =============================================================
    # 1. Re-plot 2018-01-01 00:00 UT with No Saturation
    # =============================================================
    vsw_2018 = 370.0; dsw_2018 = 13.46; wsw_2018 = 6.50
    bx_2018 = 1.54; by_2018 = -6.64; bz_2018 = -4.20
    psi_2018 = -25.40
    
    title_2018 = (
        r"Tsyganenko MSheath Model [2018-01-01 00:00 UT (00:01 UT)] — No Saturation" + "\n" +
        rf"$V_{{\mathrm{{sw}}}}={vsw_2018:.1f}\ \mathrm{{km/s}},\ N_{{\mathrm{{sw}}}}={dsw_2018:.2f}\ \mathrm{{cm^{{-3}}}},\ T_{{\mathrm{{sw}}}}={wsw_2018*11604.5/1e3:.1f}\ \mathrm{{kK}},\ \mathbf{{B}}_{{\mathrm{{IMF}}}}=({bx_2018:+.2f}, {by_2018:+.2f}, {bz_2018:+.2f})\ \mathrm{{nT}},\ \Psi={psi_2018:.1f}^\circ$"
    )
    
    plot_six_panels_nosat(
        dat_file="omni_20180101_equatorial.dat",
        save_path="omni_20180101_equatorial_nosat.png",
        plane_name="Equatorial Plane (2018)",
        coord_label="Y",
        title_info=title_2018 + r" — Equatorial Plane ($Z=0$)",
        psi_deg=psi_2018,
        xmin=xmin, xmax=xmax, gmin=gmin, gmax=gmax, vsw_val=vsw_2018
    )
    
    plot_six_panels_nosat(
        dat_file="omni_20180101_meridional.dat",
        save_path="omni_20180101_meridional_nosat.png",
        plane_name="Meridian Plane (2018)",
        coord_label="Z",
        title_info=title_2018 + r" — Noon-Midnight Meridian ($Y=0$)",
        psi_deg=psi_2018,
        xmin=xmin, xmax=xmax, gmin=gmin, gmax=gmax, vsw_val=vsw_2018
    )
    
    # =============================================================
    # 2. Simulate & Plot 2008-06-12 06:00 UT
    # =============================================================
    # OMNI observed parameters for 2008-06-12 06:00 UT:
    # Vsw = 319.0 km/s (measured at 06:00 UT)
    # Nsw = 6.90 cm^-3 (05:00 UT measurement; stable solar min stream)
    # Tsw = 17,726 K -> Wsw = 1.53 eV
    # IMF (GSM): Bx = +0.60 nT, By = +0.60 nT, Bz = +1.60 nT
    # Dipole tilt Psi = +13.57 deg (IGRF calculated)
    vsw_2008 = 319.0; dsw_2008 = 6.90; wsw_2008 = 1.53
    bx_2008 = 0.60; by_2008 = 0.60; bz_2008 = 1.60
    psi_2008 = 13.57
    
    title_2008 = (
        r"Tsyganenko MSheath Model [2008-06-12 06:00 UT (Solar Minimum)]" + "\n" +
        rf"$V_{{\mathrm{{sw}}}}={vsw_2008:.1f}\ \mathrm{{km/s}},\ N_{{\mathrm{{sw}}}}={dsw_2008:.2f}\ \mathrm{{cm^{{-3}}}},\ T_{{\mathrm{{sw}}}}={wsw_2008*11604.5/1e3:.1f}\ \mathrm{{kK}}\ ({wsw_2008:.2f}\ \mathrm{{eV}}),\ \mathbf{{B}}_{{\mathrm{{IMF}}}}=({bx_2008:+.2f}, {by_2008:+.2f}, {bz_2008:+.2f})\ \mathrm{{nT}},\ \Psi=+{psi_2008:.1f}^\circ$"
    )
    
    # 2.1 Equatorial Plane (Z=0, X-Y)
    run_fortran_grid(
        plane_type=2, vsw=vsw_2008, dsw=dsw_2008, wsw=wsw_2008,
        bx=bx_2008, by=by_2008, bz=bz_2008, psi=psi_2008,
        xmin=xmin, xmax=xmax, dx=dx, gmin=gmin, gmax=gmax, dg=dg,
        outfile="omni_20080612_equatorial.dat"
    )
    plot_six_panels_nosat(
        dat_file="omni_20080612_equatorial.dat",
        save_path="omni_20080612_equatorial_distribution.png",
        plane_name="Equatorial Plane (2008)",
        coord_label="Y",
        title_info=title_2008 + r" — Equatorial Plane ($Z=0$)",
        psi_deg=psi_2008,
        xmin=xmin, xmax=xmax, gmin=gmin, gmax=gmax, vsw_val=vsw_2008
    )
    
    # 2.2 Meridian Plane (Y=0, X-Z)
    run_fortran_grid(
        plane_type=1, vsw=vsw_2008, dsw=dsw_2008, wsw=wsw_2008,
        bx=bx_2008, by=by_2008, bz=bz_2008, psi=psi_2008,
        xmin=xmin, xmax=xmax, dx=dx, gmin=gmin, gmax=gmax, dg=dg,
        outfile="omni_20080612_meridional.dat"
    )
    plot_six_panels_nosat(
        dat_file="omni_20080612_meridional.dat",
        save_path="omni_20080612_meridional_distribution.png",
        plane_name="Meridian Plane (2008)",
        coord_label="Z",
        title_info=title_2008 + r" — Noon-Midnight Meridian ($Y=0$)",
        psi_deg=psi_2008,
        xmin=xmin, xmax=xmax, gmin=gmin, gmax=gmax, vsw_val=vsw_2008
    )
    
    print("All tasks completed successfully!")
