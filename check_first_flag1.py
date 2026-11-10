import numpy as np

data = np.genfromtxt('test_xz.dat', names=True)
subset1 = data[data['IFLAG'] == 1]
print("First 10 rows of Flag 1:")
for row in subset1[:10]:
    print(f"X={row['X']}, Z={row['Z']}, DEN={row['DEN']}, W_eV={row['W_eV']}, RBS={row['RBS']}, RMP={row['RMP']}")
