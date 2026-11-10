import numpy as np

d = np.genfromtxt('omni_20180101_meridional.dat', names=True)
msh = d[d['IFLAG'] == 1]
R = np.sqrt(msh['X']**2 + msh['Z']**2)
for r_thresh in [15, 18, 20, 22, 25, 30]:
    sub = msh[R <= r_thresh]
    if len(sub) > 0:
        print(f"R <= {r_thresh} Re (N={len(sub)}):")
        print(f"  DEN range: [{np.min(sub['DEN']):.1f}, {np.max(sub['DEN']):.1f}]")
        print(f"  T_MK range: [{np.min(sub['T_K'])/1e6:.2f}, {np.max(sub['T_K'])/1e6:.2f}]")
        print(f"  VMAG range: [{np.min(sub['VMAG']):.1f}, {np.max(sub['VMAG']):.1f}]")
        print(f"  VX range: [{np.min(sub['VX']):.1f}, {np.max(sub['VX']):.1f}]")
        print(f"  VZ range: [{np.min(sub['VZ']):.1f}, {np.max(sub['VZ']):.1f}]")
