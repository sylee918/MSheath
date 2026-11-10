import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D

def draw_earth(ax):
    night = Wedge((0, 0), 1.0, 90, 270, fc='black', ec='black', lw=1.0, zorder=10)
    day = Wedge((0, 0), 1.0, 270, 90, fc='white', ec='black', lw=1.0, zorder=10)
    ax.add_patch(night)
    ax.add_patch(day)

def plot_components_equatorial(dat_file, save_path):
    print(f"Plotting equatorial velocity components from {dat_file}...")
    data = np.genfromtxt(dat_file, names=True)
    xs = np.unique(data['X'])
    ys = np.unique(data['Y'])
    nx, ny = len(xs), len(ys)
    
    X = data['X'].reshape((nx, ny))
    Y = data['Y'].reshape((nx, ny))
    VX = data['VX'].reshape((nx, ny))
    VY = data['VY'].reshape((nx, ny))
    VZ = data['VZ'].reshape((nx, ny))
    VMAG = data['VMAG'].reshape((nx, ny))
    RBS = data['RBS'].reshape((nx, ny))
    RMP = data['RMP'].reshape((nx, ny))
    IFLAG = data['IFLAG'].reshape((nx, ny))
    R = np.sqrt(X**2 + Y**2)
    
    # Mask magnetosphere
    vx_plot = np.where(IFLAG == 0, np.nan, VX)
    vy_plot = np.where(IFLAG == 0, np.nan, VY)
    vz_plot = np.where(IFLAG == 0, np.nan, VZ)
    vmag_plot = np.where(IFLAG == 0, np.nan, VMAG)
    
    # 2x2 Subplots for Vx, Vy, Vz, and |V| with streamlines
    fig, axes = plt.subplots(2, 2, figsize=(16, 14), dpi=300)
    
    # (a) Vx component
    ax_vx = axes[0, 0]
    cmap_vx = plt.cm.RdBu_r.copy()
    cmap_vx.set_bad('midnightblue', 0.9)
    # Vx ranges from -450 km/s to 0
    cf_vx = ax_vx.contourf(X, Y, vx_plot, levels=np.linspace(-420, 0, 85), cmap=cmap_vx, extend='both')
    c_vx = ax_vx.contour(X, Y, vx_plot, levels=[-400, -300, -200, -100, -50], colors='k', linewidths=0.5, alpha=0.5)
    ax_vx.clabel(c_vx, inline=True, fontsize=8, fmt='%.0f')
    ax_vx.contour(X, Y, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_vx.contour(X, Y, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_vx)
    cb_vx = fig.colorbar(cf_vx, ax=ax_vx, fraction=0.046, pad=0.04)
    cb_vx.set_label(r'$V_x\ [\mathrm{km/s}]$ (Sunward $>0$, Tailward $<0$)', fontsize=11, fontweight='bold')
    ax_vx.set_title(r'(a) Sun-Earth Flow Component $V_x$', fontsize=13, fontweight='bold', pad=8)
    ax_vx.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vx.set_ylabel(r'$Y_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vx.set_xlim(-12, 18); ax_vx.set_ylim(-16, 16); ax_vx.set_aspect('equal')
    ax_vx.grid(True, linestyle=':', alpha=0.4)
    
    # (b) Vy component
    ax_vy = axes[0, 1]
    cmap_vy = plt.cm.PuOr.copy() # symmetric diverging colormap around 0
    cmap_vy.set_bad('midnightblue', 0.9)
    cf_vy = ax_vy.contourf(X, Y, vy_plot, levels=np.linspace(-250, 250, 101), cmap=cmap_vy, extend='both')
    c_vy = ax_vy.contour(X, Y, vy_plot, levels=[-200, -150, -100, -50, 0, 50, 100, 150, 200], colors='k', linewidths=0.5, alpha=0.5)
    ax_vy.clabel(c_vy, inline=True, fontsize=8, fmt='%.0f')
    ax_vy.contour(X, Y, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_vy.contour(X, Y, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_vy)
    cb_vy = fig.colorbar(cf_vy, ax=ax_vy, fraction=0.046, pad=0.04)
    cb_vy.set_label(r'$V_y\ [\mathrm{km/s}]$ (Duskward $>0$, Dawnward $<0$)', fontsize=11, fontweight='bold')
    ax_vy.set_title(r'(b) Dawn-Dusk Deflection Component $V_y$', fontsize=13, fontweight='bold', pad=8)
    ax_vy.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vy.set_ylabel(r'$Y_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vy.set_xlim(-12, 18); ax_vy.set_ylim(-16, 16); ax_vy.set_aspect('equal')
    ax_vy.grid(True, linestyle=':', alpha=0.4)
    
    # (c) Vz component
    ax_vz = axes[1, 0]
    cmap_vz = plt.cm.coolwarm.copy()
    cmap_vz.set_bad('midnightblue', 0.9)
    cf_vz = ax_vz.contourf(X, Y, vz_plot, levels=np.linspace(-60, 60, 61), cmap=cmap_vz, extend='both')
    ax_vz.contour(X, Y, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_vz.contour(X, Y, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_vz)
    cb_vz = fig.colorbar(cf_vz, ax=ax_vz, fraction=0.046, pad=0.04)
    cb_vz.set_label(r'$V_z\ [\mathrm{km/s}]$ (Northward $>0$, Southward $<0$)', fontsize=11, fontweight='bold')
    ax_vz.set_title(r'(c) Out-of-Plane Component $V_z$ (Equator, $Z=0$)', fontsize=13, fontweight='bold', pad=8)
    ax_vz.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vz.set_ylabel(r'$Y_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vz.set_xlim(-12, 18); ax_vz.set_ylim(-16, 16); ax_vz.set_aspect('equal')
    ax_vz.grid(True, linestyle=':', alpha=0.4)
    
    # (d) Magnitude |V| + Streamlines
    ax_mag = axes[1, 1]
    cmap_mag = plt.cm.turbo.copy()
    cmap_mag.set_bad('midnightblue', 0.9)
    cf_mag = ax_mag.contourf(X, Y, vmag_plot, levels=np.linspace(0, 450, 61), cmap=cmap_mag, extend='max')
    
    vx_stream = np.where(IFLAG > 0, VX, 0.0)
    vy_stream = np.where(IFLAG > 0, VY, 0.0)
    ax_mag.streamplot(xs, ys, vx_stream.T, vy_stream.T, color='white', density=1.2, linewidth=0.8, arrowsize=1.0)
    ax_mag.contour(X, Y, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_mag.contour(X, Y, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_mag)
    cb_mag = fig.colorbar(cf_mag, ax=ax_mag, fraction=0.046, pad=0.04)
    cb_mag.set_label(r'Total Speed $|V| = \sqrt{V_x^2+V_y^2+V_z^2}\ [\mathrm{km/s}]$', fontsize=11, fontweight='bold')
    ax_mag.set_title(r'(d) Total Speed $|V|$ & Velocity Streamlines', fontsize=13, fontweight='bold', pad=8)
    ax_mag.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_mag.set_ylabel(r'$Y_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_mag.set_xlim(-12, 18); ax_mag.set_ylim(-16, 16); ax_mag.set_aspect('equal')
    ax_mag.grid(True, linestyle=':', alpha=0.4)
    
    legend_elements = [
        Line2D([0], [0], color='cyan', lw=2.0, linestyle='-', label='Magnetopause (Lin et al.)'),
        Line2D([0], [0], color='magenta', lw=2.0, linestyle='--', label='Bow Shock (Lu et al.)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markeredgecolor='k', markersize=8, label='Earth')
    ]
    ax_vx.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.9, facecolor='white')
    
    plt.suptitle(r"Magnetosheath Plasma Bulk Velocity Vector Decomposition $(V_x, V_y, V_z, |V|)$ in Equatorial Plane ($Z=0$)" + "\n" +
                 r"$V_{\mathrm{sw}}=400\ \mathrm{km/s},\ N_{\mathrm{sw}}=5\ \mathrm{cm^{-3}},\ \mathbf{B}_{\mathrm{IMF}}=(-4, +5, 0)\ \mathrm{nT}\ (\mathrm{Parker\ Spiral}),\ \Psi=0^\circ$",
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")

def plot_components_meridional(dat_file, save_path):
    print(f"Plotting meridional velocity components from {dat_file}...")
    data = np.genfromtxt(dat_file, names=True)
    xs = np.unique(data['X'])
    zs = np.unique(data['Z'])
    nx, nz = len(xs), len(zs)
    
    X = data['X'].reshape((nx, nz))
    Z = data['Z'].reshape((nx, nz))
    VX = data['VX'].reshape((nx, nz))
    VY = data['VY'].reshape((nx, nz))
    VZ = data['VZ'].reshape((nx, nz))
    VMAG = data['VMAG'].reshape((nx, nz))
    RBS = data['RBS'].reshape((nx, nz))
    RMP = data['RMP'].reshape((nx, nz))
    IFLAG = data['IFLAG'].reshape((nx, nz))
    R = np.sqrt(X**2 + Z**2)
    
    vx_plot = np.where(IFLAG == 0, np.nan, VX)
    vy_plot = np.where(IFLAG == 0, np.nan, VY)
    vz_plot = np.where(IFLAG == 0, np.nan, VZ)
    vmag_plot = np.where(IFLAG == 0, np.nan, VMAG)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14), dpi=300)
    
    # (a) Vx component
    ax_vx = axes[0, 0]
    cmap_vx = plt.cm.RdBu_r.copy()
    cmap_vx.set_bad('midnightblue', 0.9)
    cf_vx = ax_vx.contourf(X, Z, vx_plot, levels=np.linspace(-420, 0, 85), cmap=cmap_vx, extend='both')
    c_vx = ax_vx.contour(X, Z, vx_plot, levels=[-400, -300, -200, -100, -50], colors='k', linewidths=0.5, alpha=0.5)
    ax_vx.clabel(c_vx, inline=True, fontsize=8, fmt='%.0f')
    ax_vx.contour(X, Z, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_vx.contour(X, Z, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_vx)
    cb_vx = fig.colorbar(cf_vx, ax=ax_vx, fraction=0.046, pad=0.04)
    cb_vx.set_label(r'$V_x\ [\mathrm{km/s}]$ (Sunward $>0$, Tailward $<0$)', fontsize=11, fontweight='bold')
    ax_vx.set_title(r'(a) Sun-Earth Flow Component $V_x$', fontsize=13, fontweight='bold', pad=8)
    ax_vx.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vx.set_ylabel(r'$Z_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vx.set_xlim(-12, 18); ax_vx.set_ylim(-16, 16); ax_vx.set_aspect('equal')
    ax_vx.grid(True, linestyle=':', alpha=0.4)
    
    # (b) Vz component (North-South deflection)
    ax_vz = axes[0, 1]
    cmap_vz = plt.cm.PuOr.copy()
    cmap_vz.set_bad('midnightblue', 0.9)
    cf_vz = ax_vz.contourf(X, Z, vz_plot, levels=np.linspace(-250, 250, 101), cmap=cmap_vz, extend='both')
    c_vz = ax_vz.contour(X, Z, vz_plot, levels=[-200, -150, -100, -50, 0, 50, 100, 150, 200], colors='k', linewidths=0.5, alpha=0.5)
    ax_vz.clabel(c_vz, inline=True, fontsize=8, fmt='%.0f')
    ax_vz.contour(X, Z, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_vz.contour(X, Z, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_vz)
    cb_vz = fig.colorbar(cf_vz, ax=ax_vz, fraction=0.046, pad=0.04)
    cb_vz.set_label(r'$V_z\ [\mathrm{km/s}]$ (Northward $>0$, Southward $<0$)', fontsize=11, fontweight='bold')
    ax_vz.set_title(r'(b) North-South Deflection Component $V_z$', fontsize=13, fontweight='bold', pad=8)
    ax_vz.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vz.set_ylabel(r'$Z_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vz.set_xlim(-12, 18); ax_vz.set_ylim(-16, 16); ax_vz.set_aspect('equal')
    ax_vz.grid(True, linestyle=':', alpha=0.4)
    
    # (c) Vy component (Out-of-plane)
    ax_vy = axes[1, 0]
    cmap_vy = plt.cm.coolwarm.copy()
    cmap_vy.set_bad('midnightblue', 0.9)
    cf_vy = ax_vy.contourf(X, Z, vy_plot, levels=np.linspace(-60, 60, 61), cmap=cmap_vy, extend='both')
    ax_vy.contour(X, Z, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_vy.contour(X, Z, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_vy)
    cb_vy = fig.colorbar(cf_vy, ax=ax_vy, fraction=0.046, pad=0.04)
    cb_vy.set_label(r'$V_y\ [\mathrm{km/s}]$ (Duskward $>0$, Dawnward $<0$)', fontsize=11, fontweight='bold')
    ax_vy.set_title(r'(c) Out-of-Plane Component $V_y$ (Meridian, $Y=0$)', fontsize=13, fontweight='bold', pad=8)
    ax_vy.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vy.set_ylabel(r'$Z_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_vy.set_xlim(-12, 18); ax_vy.set_ylim(-16, 16); ax_vy.set_aspect('equal')
    ax_vy.grid(True, linestyle=':', alpha=0.4)
    
    # (d) Magnitude |V| + Streamlines
    ax_mag = axes[1, 1]
    cmap_mag = plt.cm.turbo.copy()
    cmap_mag.set_bad('midnightblue', 0.9)
    cf_mag = ax_mag.contourf(X, Z, vmag_plot, levels=np.linspace(0, 450, 61), cmap=cmap_mag, extend='max')
    
    vx_stream = np.where(IFLAG > 0, VX, 0.0)
    vz_stream = np.where(IFLAG > 0, VZ, 0.0)
    ax_mag.streamplot(xs, zs, vx_stream.T, vz_stream.T, color='white', density=1.2, linewidth=0.8, arrowsize=1.0)
    ax_mag.contour(X, Z, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
    ax_mag.contour(X, Z, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
    draw_earth(ax_mag)
    cb_mag = fig.colorbar(cf_mag, ax=ax_mag, fraction=0.046, pad=0.04)
    cb_mag.set_label(r'Total Speed $|V| = \sqrt{V_x^2+V_y^2+V_z^2}\ [\mathrm{km/s}]$', fontsize=11, fontweight='bold')
    ax_mag.set_title(r'(d) Total Speed $|V|$ & Velocity Streamlines', fontsize=13, fontweight='bold', pad=8)
    ax_mag.set_xlabel(r'$X_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_mag.set_ylabel(r'$Z_{\mathrm{GSE/GSM}}\ [R_E]$', fontsize=11, fontweight='bold')
    ax_mag.set_xlim(-12, 18); ax_mag.set_ylim(-16, 16); ax_mag.set_aspect('equal')
    ax_mag.grid(True, linestyle=':', alpha=0.4)
    
    legend_elements = [
        Line2D([0], [0], color='cyan', lw=2.0, linestyle='-', label='Magnetopause (Lin et al.)'),
        Line2D([0], [0], color='magenta', lw=2.0, linestyle='--', label='Bow Shock (Lu et al.)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markeredgecolor='k', markersize=8, label='Earth')
    ]
    ax_vx.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.9, facecolor='white')
    
    plt.suptitle(r"Magnetosheath Plasma Bulk Velocity Vector Decomposition $(V_x, V_y, V_z, |V|)$ in Noon-Midnight Meridian ($Y=0$)" + "\n" +
                 r"$V_{\mathrm{sw}}=400\ \mathrm{km/s},\ N_{\mathrm{sw}}=5\ \mathrm{cm^{-3}},\ \mathbf{B}_{\mathrm{IMF}}=(0, 0, +5)\ \mathrm{nT},\ \Psi=0^\circ$",
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")

if __name__ == '__main__':
    # 1. Equatorial Plane (X-Y) - shows Vx, Vy, Vz, |V|
    plot_components_equatorial("msh_equatorial_data.dat", "msh_velocity_components_equatorial.png")
    
    # 2. Meridional Plane (X-Z) - shows Vx, Vz, Vy, |V|
    plot_components_meridional("msh_meridional_data.dat", "msh_velocity_components_meridional.png")
