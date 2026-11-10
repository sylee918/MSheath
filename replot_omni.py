import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm

def draw_earth(ax, psi_deg=0.0, is_meridian=False):
    night = Wedge((0, 0), 1.0, 90, 270, fc='black', ec='black', lw=1.0, zorder=10)
    day = Wedge((0, 0), 1.0, 270, 90, fc='white', ec='black', lw=1.0, zorder=10)
    ax.add_patch(night)
    ax.add_patch(day)
    
    if is_meridian and abs(psi_deg) > 0.1:
        psi_rad = np.radians(psi_deg)
        mx = 2.2 * np.sin(psi_rad)
        mz = 2.2 * np.cos(psi_rad)
        ax.annotate('', xy=(mx, mz), xytext=(-mx*0.4, -mz*0.4),
                    arrowprops=dict(arrowstyle="->", color="gold", lw=2.2, zorder=12))
        ax.text(mx*1.2, mz*1.2, r'$\mathbf{M}$', color='gold', fontsize=11, fontweight='bold',
                ha='center', va='center', zorder=12)

def plot_six_panels(dat_file, save_path, plane_name, coord_label, title_info, psi_deg, xmin, xmax, gmin, gmax):
    print(f"Plotting robust 6 panels for {plane_name} from {dat_file}...")
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
    
    # Clip extreme extrapolation values at distant high-latitude flanks (|G| > 20 Re)
    # Physical speed cap for solar wind / magnetosheath: ~500 km/s
    VMAG_clipped = np.clip(VMAG, 0.0, 500.0)
    VX_clipped = np.clip(VX, -500.0, 500.0)
    VY_clipped = np.clip(VY, -500.0, 500.0)
    VZ_clipped = np.clip(VZ, -500.0, 500.0)
    
    # Cap polynomial extrapolation spikes at deep distant flanks for density and temp
    DEN_clipped = np.clip(DEN, 0.0, 65.0)
    T_clipped = np.clip(T_MK, 0.0, 4.0)
    
    # Mask magnetosphere (IFLAG == 0)
    den_p = np.where(IFLAG == 0, np.nan, DEN_clipped)
    t_p = np.where(IFLAG == 0, np.nan, T_clipped)
    vmag_p = np.where(IFLAG == 0, np.nan, VMAG_clipped)
    vx_p = np.where(IFLAG == 0, np.nan, VX_clipped)
    vy_p = np.where(IFLAG == 0, np.nan, VY_clipped)
    vz_p = np.where(IFLAG == 0, np.nan, VZ_clipped)
    
    fig, axes = plt.subplots(2, 3, figsize=(22, 13), dpi=300)
    
    # Scale ranges
    den_max = 60.0
    t_max = 3.5
    vmag_max = 450.0
    
    # Symmetric limits for velocity components
    vx_lim = 450.0 # -450 to +450 km/s (symmetric)
    vy_lim = 250.0 # -250 to +250 km/s
    vz_lim = 250.0 # -250 to +250 km/s
    
    cmap_jet = plt.cm.jet.copy()
    cmap_jet.set_bad('midnightblue', 0.95)
    
    cmap_rdbu = plt.cm.RdBu_r.copy() # Blue negative, Red positive, White zero
    cmap_rdbu.set_bad('midnightblue', 0.95)
    
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
    
    # -------------------------------------------------------------
    # (1) Density Np (jet, 0 to 60)
    # -------------------------------------------------------------
    ax = axes[0, 0]
    cf = ax.contourf(X, G, den_p, levels=np.linspace(0, den_max, 61), cmap=cmap_jet, extend='max')
    c = ax.contour(X, G, den_p, levels=[10, 20, 30, 40, 50], colors='white', linewidths=0.5, alpha=0.6)
    ax.clabel(c, inline=True, fontsize=7.5, fmt='%.0f')
    format_ax(ax, r'(a) Proton Number Density $N_p$ [$\mathrm{cm^{-3}}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$N_p\ [\mathrm{cm^{-3}}]$', fontsize=11, fontweight='bold')
    
    # -------------------------------------------------------------
    # (2) Temperature T (jet, 0 to 3.5 MK)
    # -------------------------------------------------------------
    ax = axes[0, 1]
    cf = ax.contourf(X, G, t_p, levels=np.linspace(0, t_max, 71), cmap=cmap_jet, extend='max')
    c = ax.contour(X, G, t_p, levels=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0], colors='white', linewidths=0.5, alpha=0.6)
    ax.clabel(c, inline=True, fontsize=7.5, fmt='%.1f')
    format_ax(ax, r'(b) Proton Temperature $T$ [$10^6\ \mathrm{K}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$T\ [10^6\ \mathrm{K}]$', fontsize=11, fontweight='bold')
    
    # -------------------------------------------------------------
    # (3) Speed |V| (jet, 0 to 450 km/s) + Streamlines
    # -------------------------------------------------------------
    ax = axes[0, 2]
    cf = ax.contourf(X, G, vmag_p, levels=np.linspace(0, vmag_max, 91), cmap=cmap_jet, extend='max')
    vx_stream = np.where(IFLAG > 0, VX_clipped, 0.0)
    vg_stream = np.where(IFLAG > 0, (VZ_clipped if is_meridian else VY_clipped), 0.0)
    ax.streamplot(xs, gs, vx_stream.T, vg_stream.T, color='white', density=1.2, linewidth=0.7, arrowsize=0.9)
    format_ax(ax, r'(c) Flow Speed $|V|$ [$\mathrm{km/s}$] & Streamlines')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$|V|\ [\mathrm{km/s}]$', fontsize=11, fontweight='bold')
    
    # -------------------------------------------------------------
    # (4) Vx (RdBu_r, symmetric [-450, +450])
    # -------------------------------------------------------------
    ax = axes[1, 0]
    norm_vx = TwoSlopeNorm(vmin=-vx_lim, vcenter=0.0, vmax=vx_lim)
    cf = ax.contourf(X, G, vx_p, levels=np.linspace(-vx_lim, vx_lim, 91), cmap=cmap_rdbu, norm=norm_vx, extend='both')
    format_ax(ax, r'(d) Sun-Earth Flow Component $V_x$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_x\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=11, fontweight='bold')
    
    # -------------------------------------------------------------
    # (5) Vy (RdBu_r, symmetric [-250, +250])
    # -------------------------------------------------------------
    ax = axes[1, 1]
    norm_vy = TwoSlopeNorm(vmin=-vy_lim, vcenter=0.0, vmax=vy_lim)
    cf = ax.contourf(X, G, vy_p, levels=np.linspace(-vy_lim, vy_lim, 101), cmap=cmap_rdbu, norm=norm_vy, extend='both')
    format_ax(ax, r'(e) Dawn-Dusk Flow Component $V_y$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_y\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=11, fontweight='bold')
    
    # -------------------------------------------------------------
    # (6) Vz (RdBu_r, symmetric [-250, +250])
    # -------------------------------------------------------------
    ax = axes[1, 2]
    norm_vz = TwoSlopeNorm(vmin=-vz_lim, vcenter=0.0, vmax=vz_lim)
    cf = ax.contourf(X, G, vz_p, levels=np.linspace(-vz_lim, vz_lim, 101), cmap=cmap_rdbu, norm=norm_vz, extend='both')
    format_ax(ax, r'(f) North-South Flow Component $V_z$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_z\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=11, fontweight='bold')
    
    # Legend
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
    print(f"Saved: {save_path}")

if __name__ == '__main__':
    vsw = 370.0
    dsw = 13.46
    wsw = 6.50
    bx  = 1.54
    by  = -6.64
    bz  = -4.20
    psi = -25.40
    
    xmin = -10.0; xmax = 20.0; gmin = -30.0; gmax = 30.0
    
    title_common = (
        r"Tsyganenko MSheath Model Driven by OMNI Data [2018-01-01 00:00 UT (00:01 UT)]" + "\n" +
        rf"$V_{{\mathrm{{sw}}}}={vsw:.1f}\ \mathrm{{km/s}},\ N_{{\mathrm{{sw}}}}={dsw:.2f}\ \mathrm{{cm^{{-3}}}},\ T_{{\mathrm{{sw}}}}={wsw*11604.5/1e3:.1f}\ \mathrm{{kK}}\ ({wsw:.2f}\ \mathrm{{eV}}),\ \mathbf{{B}}_{{\mathrm{{IMF}}}}=({bx:+.2f}, {by:+.2f}, {bz:+.2f})\ \mathrm{{nT}}\ (\mathrm{{GSM}}),\ \Psi={psi:.1f}^\circ$"
    )
    
    # 1. Equatorial Plane
    plot_six_panels(
        dat_file="omni_20180101_equatorial.dat",
        save_path="omni_20180101_equatorial_distribution.png",
        plane_name="Equatorial Plane",
        coord_label="Y",
        title_info=title_common + r" — Equatorial Plane ($Z_{\mathrm{GSM}}=0$)",
        psi_deg=psi,
        xmin=xmin, xmax=xmax, gmin=gmin, gmax=gmax
    )
    
    # 2. Meridional Plane
    plot_six_panels(
        dat_file="omni_20180101_meridional.dat",
        save_path="omni_20180101_meridional_distribution.png",
        plane_name="Noon-Midnight Meridian Plane",
        coord_label="Z",
        title_info=title_common + r" — Noon-Midnight Meridian Plane ($Y_{\mathrm{GSM}}=0$)",
        psi_deg=psi,
        xmin=xmin, xmax=xmax, gmin=gmin, gmax=gmax
    )
    
    print("Re-rendered both 6-panel figures successfully!")
