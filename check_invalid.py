import numpy as np

for f in ['omni_20180101_meridional.dat', 'omni_20080612_meridional.dat', 'omni_20180101_equatorial.dat', 'omni_20080612_equatorial.dat']:
    d = np.genfromtxt(f, names=True)
    msh = (d['IFLAG'] == 1)
    vsw = 370.0 if '2018' in f else 319.0
    nsw = 13.46 if '2018' in f else 6.90
    
    inv_v = msh & (d['VMAG'] > 1.35 * vsw)
    inv_n = msh & (d['DEN'] < 0.25 * nsw)
    inv_comb = inv_v | inv_n
    
    print(f)
    print('  Total MSH points:', np.sum(msh))
    print('  Invalid by V > 1.35*Vsw:', np.sum(inv_v))
    print('  Invalid by N < 0.25*Nsw:', np.sum(inv_n))
    print('  Invalid combined:', np.sum(inv_comb))
    if np.sum(inv_comb) > 0:
        print('  X range of invalid:', d['X'][inv_comb].min(), d['X'][inv_comb].max())
        coord = 'Z' if 'meridional' in f else 'Y'
        print(f'  {coord} range of invalid:', d[coord][inv_comb].min(), d[coord][inv_comb].max())
