import numpy as np

d = np.genfromtxt('omni_20180101_meridional.dat', names=True)
msh = d[d['IFLAG'] == 1]
bad = msh[msh['VMAG'] > 500.0]
print(f"Total bad points: {len(bad)} / {len(msh)}")
for row in bad[:10]:
    print(f"X={row['X']:.2f}, Z={row['Z']:.2f}, DEN={row['DEN']:.3f}, VMAG={row['VMAG']:.1f}, FX={row['FX']:.3f}, FZ={row['FZ']:.3f}")
