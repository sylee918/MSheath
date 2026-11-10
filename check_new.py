import numpy as np

data = np.genfromtxt('test_xz_new.dat', names=True)
print('Total points:', len(data))
print('NaN count DEN:', np.sum(np.isnan(data['DEN'])))
print('NaN count W_eV:', np.sum(np.isnan(data['W_eV'])))
print('NaN count VMAG:', np.sum(np.isnan(data['VMAG'])))
for flag in [0, 1, 2]:
    subset = data[data['IFLAG'] == flag]
    if len(subset) > 0:
        print(f'Flag {int(flag)} (count={len(subset)}):')
        print(f'  DEN range: [{np.nanmin(subset["DEN"]):.2f}, {np.nanmax(subset["DEN"]):.2f}] cm^-3')
        print(f'  W_eV range: [{np.nanmin(subset["W_eV"]):.2f}, {np.nanmax(subset["W_eV"]):.2f}] eV')
        print(f'  VMAG range: [{np.nanmin(subset["VMAG"]):.2f}, {np.nanmax(subset["VMAG"]):.2f}] km/s')
