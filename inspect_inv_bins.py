import numpy as np

d = np.genfromtxt('omni_20180101_meridional.dat', names=True)
msh = (d['IFLAG'] == 1)
vsw = 370.0
nsw = 13.46

inv_comb = msh & ((d['VMAG'] > 1.35 * vsw) | (d['DEN'] < 0.25 * nsw))
print("Inv points by X bins:")
for x_val in np.arange(-10, 11, 2):
    sub = inv_comb & (d['X'] >= x_val) & (d['X'] < x_val + 2)
    tot = msh & (d['X'] >= x_val) & (d['X'] < x_val + 2)
    if np.sum(tot) > 0:
        z_inv = d['Z'][sub]
        z_str = f"Z in [{z_inv.min():.1f}, {z_inv.max():.1f}]" if len(z_inv) > 0 else "None"
        print(f"  X in [{x_val:3d}, {x_val+2:3d}]: {np.sum(sub):4d} / {np.sum(tot):4d} ({np.sum(sub)/np.sum(tot)*100:5.1f}%) | {z_str}")
