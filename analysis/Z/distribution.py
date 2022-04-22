
import numpy as np
import pickle

import flares_utility.analyse
import flares_utility.stats

from scipy.stats import pearsonr

filename = flares_utility.analyse.flares_master_file

a = flares_utility.analyse.analyse_flares(filename, default_tags = False)

# a.list_datasets()


x = 'log10Mstar_30'

s_limit = 8.5
quantiles = [0.022, 0.158, 0.5, 0.842, 0.978]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

iz = 5

O = {}

# for tag, z in zip(a.tags, a.zeds):


linear_bins = np.arange(0.0, 0.05, 0.001)
log10_bins = np.arange(-5.,-1.,0.1)

for tag, z in zip(a.tags, a.zeds):

    print(z, '-'*20)
    O[z] = {}
    O[z]['linear'] = {}
    O[z]['log10'] = {}

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    pD = a.get_particle_datasets(tag)

    for log10Mstar in np.arange(8.75, 11., 0.5):

        s = (np.fabs(D['log10Mstar_30']-log10Mstar)<0.25)

        # galaxy indices meeting criteria
        i_ = np.arange(len(s))[s]
        print(log10Mstar, len(i_))

        o = np.array([])
        for i in i_:
            o = np.concatenate((o, pD['S_Z'][i]))

        N, _ = np.histogram(o, bins = linear_bins)
        O[z]['linear'][log10Mstar] = N

        N, _ = np.histogram(o, bins = log10_bins)
        O[z]['log10'][log10Mstar] = N






pickle.dump(O, open('distributions.p','wb'))
