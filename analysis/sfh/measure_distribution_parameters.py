

import sys

# import matplotlib as mpl
# import matplotlib.cm as cm
# mpl.use('Agg')
# import matplotlib.pyplot as plt

import numpy as np
import pickle

import h5py


from scipy.optimize import curve_fit
from util import expon, truncnorm, halfnorm, trunclognorm


binw = 10
bins = np.arange(0.0, 1500., binw)
binc = 0.5*(bins[:-1]+bins[1:])


import flares_utility.analyse
import flares_utility.stats



filename = flares_utility.analyse.flares_master_file
a = flares_utility.analyse.analyse_flares(filename, default_tags = False)



x = 'log10Mstar_30'

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

iz = int(sys.argv[1])

dist_name = sys.argv[2]

dists = {'halfnorm': halfnorm(), 'truncnorm': truncnorm(max_age = 1500)}
dists = {'expon': expon(), 'halfnorm': halfnorm(), 'truncnorm': truncnorm(max_age = 1500), 'trunclognorm': trunclognorm(max_age = 1500)}




dist = dists[dist_name]

tag = a.tags[iz]
z = a.zeds[iz]

print(z, dist_name)



# -- temporary file
o = h5py.File(f'data/temp_{z}_{dist_name}.h5', 'w')


# --- get quantities (and weights and deltas)
D = a.get_datasets(tag, quantities)
pD = a.get_particle_datasets(tag)

n = len(D['log10Mstar_30'])

print(n)

o.create_dataset('D', data=np.empty(n))
o.create_dataset('p', data=np.empty((n, dist.nparams)))



for i, (ages, massinitial) in enumerate(zip(pD['S_Age'], pD['S_MassInitial'])):

    if len(ages)>100:

        N_obs, _ = np.histogram(ages, bins = bins, weights = massinitial, density = True)
        cdf_obs = np.cumsum(N_obs[::-1])*binw

        # --- fit

        params, _  = curve_fit(dist.pdf, binc, N_obs, p0 = dist.p0)
        N_fit = dist.pdf(binc, *params)
        cdf_fit = 1-dist.cdf(bins[:-1], *params)

        KS = np.max(np.fabs(cdf_obs-cdf_fit[::-1])) # -- measure the KS

        o['D'][i] = KS
        o['p'][i] = params



with h5py.File('data/sf.h5', 'w') as f:
    f.create_dataset(f'{z}/{dist_name}/D', data=o['D'])
    f.create_dataset(f'{z}/{dist_name}/p', data=o['p'])
