import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Circle, Wedge
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

def draw_earth(ax):
    # Earth centered at (0, 0), radius 1 Re
    # Dayside (X > 0) is white, nightside (X < 0) is black
    night = Wedge((0, 0), 1.0, 90, 270, fc='black', ec='black', lw=1.0, zorder=10)
    day = Wedge((0, 0), 1.0, 270, 90, fc='white', ec='black', lw=1.0, zorder=10)
    ax.add_patch(night)
    ax.add_patch(day)

def plot_case(dat_file, title_text, coord_label, save_path, xmin, xmax, gmin, gmax):
    print(f"Plotting results from {dat_file} to {save_path}...")
    data = np.genfromtxt(dat_file, names=True)
    
    xs = np.unique(data['X'])
    gs = np.unique(data['Z'] if coord_label == 'Z' else data['Y'])
    
    nx = len(xs)
    ng = len(gs)
    
    X = data['X'].reshape((nx, ng))
    G = (data['Z'] if coord_label == 'Z' else data['Y']).reshape((nx, ng))
    
    DEN = data['DEN'].reshape((nx, ng))
    VMAG = data['VMAG'].reshape((nx, ng))
    VX = data['VX'].reshape((nx, ng))
    VG = (data['VZ'] if coord_label == 'Z' else data['VY']).reshape((nx, ng))
    W_EV = data['W_eV'].reshape((nx, ng))
    T_MK = (data['T_K'] / 1e6).reshape((nx, ng)) # 10^6 K
    RBS = data['RBS'].reshape((nx, ng))
    RMP = data['RMP'].reshape((nx, ng))
    IFLAG = data['IFLAG'].reshape((nx, ng))
    
    R = np.sqrt(X**2 + G**2)
    plasma_mask = (IFLAG > 0)
    
    den_plot = np.where(IFLAG == 0, np.nan, DEN)
    vmag_plot = np.where(IFLAG == 0, np.nan, VMAG)
    t_plot = np.where(IFLAG == 0, np.nan, T_MK)
    
    fig, axes = plt.subplots(1, 3, figsize=(21, 6.8), dpi=300)
    
    # -------------------------------------------------------------
    # 1. Density Plot
    # -------------------------------------------------------------
    ax1 = axes[0]
    cmap1 = plt.cm.inferno.copy()
    cmap1.set_bad('midnightblue', 0.9)
    
    cf1 = ax1.contourf(X, G, den_plot, levels=np.linspace(0, 30, 61), cmap=cmap1, extend='max')
    c1 = ax1.contour(X, G, den_plot, levels=[5, 10, 15, 20, 25], colors='white', linewidths=0.6, alpha=0.6)
    ax1.clabel(c1, inline=True, fontsize=8, fmt='%.0f')
    
    ax1.contour(X, G, RMP - R, levels=[0], colors='cyan', linewidths=2.2, linestyles='-')
    ax1.contour(X, G, RBS - R, levels=[0], colors='magenta', linewidths=2.2, linestyles='--')
    draw_earth(ax1)
    
    cb1 = fig.colorbar(cf1, ax=ax1, fraction=0.046, pad=0.04)
    cb1.set_label(r'Proton Density $N_p\ [\mathrm{cm^{-3}}]$', fontsize=12, fontweight='bold')
    
    ax1.set_title(r'(a) Proton Number Density $N_p$', fontsize=13, fontweight='bold', pad=8)
    ax1.set_xlabel(r'$X_{\mathrm{GSM}}\ [R_E]$', fontsize=12, fontweight='bold')
    ax1.set_ylabel(rf'${coord_label}_{{\mathrm{{GSM}}}}\ [R_E]$', fontsize=12, fontweight='bold')
    ax1.set_xlim(xmin, xmax)
    ax1.set_ylim(gmin, gmax)
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle=':', alpha=0.4, color='gray')
    
    legend_elements = [
        Line2D([0], [0], color='cyan', lw=2.2, linestyle='-', label='Magnetopause (Lin et al. 2010)'),
        Line2D([0], [0], color='magenta', lw=2.2, linestyle='--', label='Bow Shock (Lu et al. 2019)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markeredgecolor='k', markersize=8, label='Earth (Day/Night)')
    ]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.9, facecolor='white')
    
    # -------------------------------------------------------------
    # 2. Velocity Plot + Streamlines
    # -------------------------------------------------------------
    ax2 = axes[1]
    cmap2 = plt.cm.turbo.copy()
    cmap2.set_bad('midnightblue', 0.9)
    
    cf2 = ax2.contourf(X, G, vmag_plot, levels=np.linspace(0, 450, 61), cmap=cmap2, extend='max')
    
    vx_stream = np.where(plasma_mask, VX, 0.0)
    vg_stream = np.where(plasma_mask, VG, 0.0)
    U = vx_stream.T
    V = vg_stream.T
    
    ax2.streamplot(xs, gs, U, V, color='white', density=1.2, linewidth=0.8,
                   arrowsize=1.0, arrowstyle='->')
    
    ax2.contour(X, G, RMP - R, levels=[0], colors='cyan', linewidths=2.2, linestyles='-')
    ax2.contour(X, G, RBS - R, levels=[0], colors='magenta', linewidths=2.2, linestyles='--')
    draw_earth(ax2)
    
    cb2 = fig.colorbar(cf2, ax=ax2, fraction=0.046, pad=0.04)
    cb2.set_label(r'Bulk Flow Velocity $|V|\ [\mathrm{km/s}]$', fontsize=12, fontweight='bold')
    
    ax2.set_title(r'(b) Bulk Velocity & Streamlines', fontsize=13, fontweight='bold', pad=8)
    ax2.set_xlabel(r'$X_{\mathrm{GSM}}\ [R_E]$', fontsize=12, fontweight='bold')
    ax2.set_ylabel(rf'${coord_label}_{{\mathrm{{GSM}}}}\ [R_E]$', fontsize=12, fontweight='bold')
    ax2.set_xlim(xmin, xmax)
    ax2.set_ylim(gmin, gmax)
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.4, color='gray')
    
    # -------------------------------------------------------------
    # 3. Temperature / Thermal Energy Plot
    # -------------------------------------------------------------
    ax3 = axes[2]
    cmap3 = plt.cm.magma.copy()
    cmap3.set_bad('midnightblue', 0.9)
    
    cf3 = ax3.contourf(X, G, t_plot, levels=np.linspace(0, 3.5, 71), cmap=cmap3, extend='max')
    c3 = ax3.contour(X, G, t_plot, levels=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0], colors='white', linewidths=0.6, alpha=0.6)
    ax3.clabel(c3, inline=True, fontsize=8, fmt='%.1f')
    
    ax3.contour(X, G, RMP - R, levels=[0], colors='cyan', linewidths=2.2, linestyles='-')
    ax3.contour(X, G, RBS - R, levels=[0], colors='magenta', linewidths=2.2, linestyles='--')
    draw_earth(ax3)
    
    cb3 = fig.colorbar(cf3, ax=ax3, fraction=0.046, pad=0.04)
    cb3.set_label(r'Proton Temperature $T\ [10^6\ \mathrm{K}]$', fontsize=12, fontweight='bold')
    
    # Annotate eV range on temperature plot subtitle
    ax3.set_title(r'(c) Proton Temperature $T$ & Thermal Energy $W$' + '\n' +
                  r'($1.0\times 10^6\ \mathrm{K} \approx 86.2\ \mathrm{eV};\ 3.0\times 10^6\ \mathrm{K} \approx 258.5\ \mathrm{eV}$)',
                  fontsize=12, fontweight='bold', pad=8)
    ax3.set_xlabel(r'$X_{\mathrm{GSM}}\ [R_E]$', fontsize=12, fontweight='bold')
    ax3.set_ylabel(rf'${coord_label}_{{\mathrm{{GSM}}}}\ [R_E]$', fontsize=12, fontweight='bold')
    ax3.set_xlim(xmin, xmax)
    ax3.set_ylim(gmin, gmax)
    ax3.set_aspect('equal')
    ax3.grid(True, linestyle=':', alpha=0.4, color='gray')
    
    plt.suptitle(title_text, fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved figure to {save_path} successfully!")

if __name__ == '__main__':
    plot_case(
        dat_file="msh_meridional_data.dat",
        title_text=r"Magnetosheath Plasma Distribution in Noon-Midnight Meridian ($Y_{\mathrm{GSM}}=0$)" + "\n" +
                   r"$V_{\mathrm{sw}}=400\ \mathrm{km/s},\ N_{\mathrm{sw}}=5\ \mathrm{cm^{-3}},\ W_{\mathrm{sw}}=10\ \mathrm{eV}\ (1.16\times 10^5\ \mathrm{K}),\ \mathbf{B}_{\mathrm{IMF}}=(0, 0, +5)\ \mathrm{nT},\ \Psi=0^\circ$",
        coord_label="Z",
        save_path="msh_meridional_distribution.png",
        xmin=-12.0, xmax=18.0, gmin=-16.0, gmax=16.0
    )
    
    plot_case(
        dat_file="msh_equatorial_data.dat",
        title_text=r"Magnetosheath Plasma Distribution in Equatorial Plane ($Z_{\mathrm{GSM}}=0$)" + "\n" +
                   r"$V_{\mathrm{sw}}=400\ \mathrm{km/s},\ N_{\mathrm{sw}}=5\ \mathrm{cm^{-3}},\ W_{\mathrm{sw}}=10\ \mathrm{eV}\ (1.16\times 10^5\ \mathrm{K}),\ \mathbf{B}_{\mathrm{IMF}}=(-4, +5, 0)\ \mathrm{nT}\ (\mathrm{Parker\ Spiral}),\ \Psi=0^\circ$",
        coord_label="Y",
        save_path="msh_equatorial_distribution.png",
        xmin=-12.0, xmax=18.0, gmin=-16.0, gmax=16.0
    )
