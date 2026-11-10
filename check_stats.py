import numpy as np

data = np.genfromtxt('test_O0.dat', names=True)
names = ['Magnetosphere', 'Magnetosheath', 'Solar Wind']
for flag in [0, 1, 2]:
    subset = data[data['IFLAG'] == flag]
    if len(subset) > 0:
        print(f"Flag {int(flag)} ({names[int(flag)]}, count={len(subset)}):")
        print(f"  Density N_p range:  [{np.min(subset['DEN']):.2f}, {np.max(subset['DEN']):.2f}] cm^-3")
        print(f"  Thermal Energy range: [{np.min(subset['W_eV']):.2f}, {np.max(subset['W_eV']):.2f}] eV")
        print(f"  Temperature range:    [{np.min(subset['T_K']):.2e}, {np.max(subset['T_K']):.2e}] K")
        print(f"  Velocity |V| range:   [{np.min(subset['VMAG']):.2f}, {np.max(subset['VMAG']):.2f}] km/s")
