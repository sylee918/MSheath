import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Patch
from matplotlib.lines import Line2D
from matplotlib.colors import TwoSlopeNorm

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

def plot_six_panels_masked(dat_file, save_path, plane_name, coord_label, title_info, psi_deg, xmin, xmax, gmin, gmax, vsw_val, nsw_val):
    print(f"Plotting masked 6 panels for {plane_name} from {dat_file}...")
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
    
    msh_mask = (IFLAG == 1)
    v_cap = max(vsw_val * 1.35, 480.0)
    
    # User requirement:
    # Equatorial plane: Keep full spatial coverage (X in [-10, 20])
    # Meridional plane: Keep range [-10, 20], but MASK entire X < 0 region!
    if is_meridian:
        # In meridional plane, mask all X < 0, plus any rare cusp numerical singularities on dayside
        is_invalid = (X < 0.0) | (msh_mask & ((VMAG > v_cap) | (DEN < 0.25 * nsw_val)))
    else:
        # Equatorial plane: only filter out unphysical singularities if any (equatorial has satellite coverage down to X >= -10)
        is_invalid = msh_mask & ((VMAG > v_cap) | (DEN < 0.25 * nsw_val))
        
    valid_msh = msh_mask & (~is_invalid)
    
    print(f"  Plane: {plane_name}, Total MSH cells: {np.sum(msh_mask)}, Invalid/Masked cells: {np.sum(is_invalid)}")
    
    # Mask magnetosphere and invalid regions
    den_p = np.where((IFLAG == 0) | is_invalid, np.nan, DEN)
    t_p = np.where((IFLAG == 0) | is_invalid, np.nan, T_MK)
    vmag_p = np.where((IFLAG == 0) | is_invalid, np.nan, VMAG)
    vx_p = np.where((IFLAG == 0) | is_invalid, np.nan, VX)
    vy_p = np.where((IFLAG == 0) | is_invalid, np.nan, VY)
    vz_p = np.where((IFLAG == 0) | is_invalid, np.nan, VZ)
    
    # Dynamic non-saturating range calculation based on VALID MSH points
    if np.any(valid_msh):
        p995_den = np.nanpercentile(den_p[valid_msh], 99.5)
        den_max = np.ceil(p995_den / 10.0) * 10.0 + 10.0
        den_max = max(den_max, 40.0)
        
        p995_t = np.nanpercentile(t_p[valid_msh], 99.5)
        t_max = np.ceil(p995_t * 2.0) / 2.0 + 0.5
        t_max = max(t_max, 2.5)
        
        vx_max_abs = max(abs(np.nanmin(vx_p[valid_msh])), abs(np.nanmax(vx_p[valid_msh])), vsw_val)
        vx_lim = np.ceil(vx_max_abs / 50.0) * 50.0
        
        vy_max_abs = max(abs(np.nanmin(vy_p[valid_msh])), abs(np.nanmax(vy_p[valid_msh]))) if np.any(valid_msh) else 100.0
        vy_lim = max(np.ceil(vy_max_abs / 25.0) * 25.0 + 25.0, 100.0)
        
        vz_max_abs = max(abs(np.nanmin(vz_p[valid_msh])), abs(np.nanmax(vz_p[valid_msh]))) if np.any(valid_msh) else 100.0
        vz_lim = max(np.ceil(vz_max_abs / 25.0) * 25.0 + 25.0, 100.0)
    else:
        den_max, t_max, vx_lim, vy_lim, vz_lim = 60.0, 3.0, 400.0, 150.0, 150.0

    vmag_max = np.ceil(v_cap / 50.0) * 50.0
    
    cmap_jet = plt.cm.jet.copy()
    cmap_jet.set_bad('midnightblue', 0.95)
    
    cmap_rdbu = plt.cm.RdBu_r.copy()
    cmap_rdbu.set_bad('midnightblue', 0.95)
    
    fig, axes = plt.subplots(2, 3, figsize=(22, 13), dpi=300)
    
    has_invalid = np.any(is_invalid)
    
    def format_ax(ax, title, xlabel=True, ylabel=True, show_legend=False):
        # Boundaries
        ax.contour(X, G, RMP - R, levels=[0], colors='cyan', linewidths=2.0)
        ax.contour(X, G, RBS - R, levels=[0], colors='magenta', linewidths=2.0, linestyles='--')
        
        # Shade masked/invalid region if present
        if has_invalid:
            ax.contourf(X, G, np.where(is_invalid, 1.0, np.nan), levels=[0.5, 1.5], colors=['#e4e4e4'], alpha=0.92, zorder=4)
            ax.contourf(X, G, np.where(is_invalid, 1.0, np.nan), levels=[0.5, 1.5], colors='none', hatches=['///'], alpha=0.45, zorder=5)
            ax.contour(X, G, np.where(is_invalid, 1.0, 0.0), levels=[0.5], colors=['#707070'], linewidths=1.2, linestyles='-', zorder=6)
        
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
        
        if show_legend:
            custom_handles = [
                Line2D([0], [0], color='cyan', lw=2.0, label='Magnetopause (Lin et al. 2010)'),
                Line2D([0], [0], color='magenta', lw=2.0, ls='--', label='Bow Shock (Lu et al. 2019)'),
                Line2D([0], [0], marker='o', color='black', label='Earth', markerfacecolor='black', markersize=7, lw=0)
            ]
            if is_meridian:
                custom_handles.append(Patch(facecolor='#e4e4e4', edgecolor='#707070', hatch='///', label='Masked Nightside ($X < 0$)'))
            elif has_invalid:
                custom_handles.append(Patch(facecolor='#e4e4e4', edgecolor='#707070', hatch='///', label='Outside Validity'))
            ax.legend(handles=custom_handles, loc='upper left', fontsize=8.5, framealpha=0.9)

    # (1) Density Np
    ax = axes[0, 0]
    cf = ax.contourf(X, G, den_p, levels=np.linspace(0, den_max, 91), cmap=cmap_jet, extend='max')
    c_step = 10 if den_max <= 70 else 20
    c = ax.contour(X, G, den_p, levels=np.arange(c_step, den_max, c_step), colors='white', linewidths=0.5, alpha=0.6)
    ax.clabel(c, inline=True, fontsize=7.5, fmt='%.0f')
    format_ax(ax, r'(a) Proton Number Density $N_p$ [$\mathrm{cm^{-3}}$]', show_legend=True)
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$N_p\ [\mathrm{cm^{-3}}]$', fontsize=11, fontweight='bold')
    
    # (2) Temperature T
    ax = axes[0, 1]
    cf = ax.contourf(X, G, t_p, levels=np.linspace(0, t_max, 91), cmap=cmap_jet, extend='max')
    t_step = 0.5 if t_max <= 4.0 else 1.0
    c = ax.contour(X, G, t_p, levels=np.arange(t_step, t_max, t_step), colors='white', linewidths=0.5, alpha=0.6)
    ax.clabel(c, inline=True, fontsize=7.5, fmt='%.1f')
    format_ax(ax, r'(b) Proton Temperature $T$ [$10^6\ \mathrm{K}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$T\ [10^6\ \mathrm{K}]$', fontsize=11, fontweight='bold')
    
    # (3) Speed |V| + Streamlines
    ax = axes[0, 2]
    cf = ax.contourf(X, G, vmag_p, levels=np.linspace(0, vmag_max, 91), cmap=cmap_jet, extend='max')
    vx_stream = np.where((~is_invalid) & (valid_msh | (IFLAG == 2)), VX, np.nan)
    vg_stream = np.where((~is_invalid) & (valid_msh | (IFLAG == 2)), (VZ if is_meridian else VY), np.nan)
    ax.streamplot(xs, gs, vx_stream.T, vg_stream.T, color='white', density=1.2, linewidth=0.7, arrowsize=0.9)
    format_ax(ax, r'(c) Flow Speed $|V|$ [$\mathrm{km/s}$] & Streamlines')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$|V|\ [\mathrm{km/s}]$', fontsize=11, fontweight='bold')
    
    # (4) Vx (RdBu_r)
    ax = axes[1, 0]
    norm_x = TwoSlopeNorm(vmin=-vx_lim, vcenter=0.0, vmax=vx_lim)
    cf = ax.contourf(X, G, vx_p, levels=np.linspace(-vx_lim, vx_lim, 91), cmap=cmap_rdbu, norm=norm_x, extend='both')
    format_ax(ax, r'(d) Sun-Earth Flow Component $V_x$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_x\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=10.5, fontweight='bold')
    
    # (5) Vy (RdBu_r)
    ax = axes[1, 1]
    norm_y = TwoSlopeNorm(vmin=-vy_lim, vcenter=0.0, vmax=vy_lim)
    cf = ax.contourf(X, G, vy_p, levels=np.linspace(-vy_lim, vy_lim, 91), cmap=cmap_rdbu, norm=norm_y, extend='both')
    format_ax(ax, r'(e) Dawn-Dusk Flow Component $V_y$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_y\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=10.5, fontweight='bold')
    
    # (6) Vz (RdBu_r)
    ax = axes[1, 2]
    norm_z = TwoSlopeNorm(vmin=-vz_lim, vcenter=0.0, vmax=vz_lim)
    cf = ax.contourf(X, G, vz_p, levels=np.linspace(-vz_lim, vz_lim, 91), cmap=cmap_rdbu, norm=norm_z, extend='both')
    format_ax(ax, r'(f) North-South Flow Component $V_z$ [$\mathrm{km/s}$]')
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r'$V_z\ [\mathrm{km/s}]$ (Blue $< 0$, Red $> 0$)', fontsize=10.5, fontweight='bold')
    
    subtitle = "Noon-Midnight Meridian (Y = 0) [Dayside Only, X >= 0]" if is_meridian else "Equatorial Plane (Z = 0)"
    fig.suptitle(f"Tsyganenko MSheath Model [{title_info}]\n{subtitle}",
                 fontsize=14, fontweight='bold', y=0.985)
    
    plt.subplots_adjust(top=0.91, bottom=0.06, left=0.05, right=0.95, hspace=0.22, wspace=0.18)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"Saved figure: {save_path}")

if __name__ == '__main__':
    xmin, xmax = -10.0, 20.0
    gmin, gmax = -30.0, 30.0
    
    # 1. 2018-01-01 Meridian (X < 0 masked)
    plot_six_panels_masked(
        'omni_20180101_meridional.dat',
        'omni_20180101_meridional_masked.png',
        'Meridian Plane (2018)',
        'Z',
        r'2018-01-01 00:00 UT (00:01 UT)] — $V_{\mathrm{sw}} = 370.0\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 13.46\ \mathrm{cm^{-3}}$, $T_{\mathrm{sw}} = 75.4\ \mathrm{kK}$, $\mathbf{B}_{\mathrm{IMF}} = (+1.54, -6.64, -4.20)\ \mathrm{nT}$, $\Psi = -25.4^\circ$',
        -25.40, xmin, xmax, gmin, gmax, 370.0, 13.46
    )
    
    # 2. 2018-01-01 Equatorial (Full coverage as is)
    plot_six_panels_masked(
        'omni_20180101_equatorial.dat',
        'omni_20180101_equatorial_masked.png',
        'Equatorial Plane (2018)',
        'Y',
        r'2018-01-01 00:00 UT (00:01 UT)] — $V_{\mathrm{sw}} = 370.0\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 13.46\ \mathrm{cm^{-3}}$, $T_{\mathrm{sw}} = 75.4\ \mathrm{kK}$, $\mathbf{B}_{\mathrm{IMF}} = (+1.54, -6.64, -4.20)\ \mathrm{nT}$, $\Psi = -25.4^\circ$',
        -25.40, xmin, xmax, gmin, gmax, 370.0, 13.46
    )

    # 3. 2008-06-12 Meridian (X < 0 masked)
    plot_six_panels_masked(
        'omni_20080612_meridional.dat',
        'omni_20080612_meridional_masked.png',
        'Meridian Plane (2008)',
        'Z',
        r'2008-06-12 06:00 UT (Solar Minimum)] — $V_{\mathrm{sw}} = 319.0\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 6.90\ \mathrm{cm^{-3}}$, $T_{\mathrm{sw}} = 17.8\ \mathrm{kK}\ (1.53\ \mathrm{eV})$, $\mathbf{B}_{\mathrm{IMF}} = (+0.60, +0.60, +1.60)\ \mathrm{nT}$, $\Psi = +13.6^\circ$',
        13.57, xmin, xmax, gmin, gmax, 319.0, 6.90
    )

    # 4. 2008-06-12 Equatorial (Full coverage as is)
    plot_six_panels_masked(
        'omni_20080612_equatorial.dat',
        'omni_20080612_equatorial_masked.png',
        'Equatorial Plane (2008)',
        'Y',
        r'2008-06-12 06:00 UT (Solar Minimum)] — $V_{\mathrm{sw}} = 319.0\ \mathrm{km/s}$, $N_{\mathrm{sw}} = 6.90\ \mathrm{cm^{-3}}$, $T_{\mathrm{sw}} = 17.8\ \mathrm{kK}\ (1.53\ \mathrm{eV})$, $\mathbf{B}_{\mathrm{IMF}} = (+0.60, +0.60, +1.60)\ \mathrm{nT}$, $\Psi = +13.6^\circ$',
        13.57, xmin, xmax, gmin, gmax, 319.0, 6.90
    )
