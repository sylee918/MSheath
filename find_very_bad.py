import numpy as np

d = np.genfromtxt('omni_20180101_meridional.dat', names=True)
msh = d[d['IFLAG'] == 1]
R = np.sqrt(msh['X']**2 + msh['Z']**2)
very_bad = msh[(R <= 15) & (msh['VMAG'] > 1000)]
print(f"Very bad count: {len(very_bad)}")
for row in very_bad:
    print(f"X={row['X']:.2f}, Z={row['Z']:.2f}, DEN={row['DEN']:.4f}, VMAG={row['VMAG']:.1f}, FX={row['FX']:.3f}, FZ={row['FZ']:.3f}")
