
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


age_bins = np.arange(0., 3.5, 0.1)
Z_bins = np.arange(-6, 0.0, 0.25)


O['age_bins'] = age_bins
O['Z_bins'] = Z_bins


# a.tags = [a.tags[4]]
# a.zeds = [a.zeds[4]]

for tag, z in zip(a.tags, a.zeds):

    print(z, '-'*20)

    O[z] = {}

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    pD = a.get_particle_datasets(tag)

    for log10Mstar in np.arange(8.75, 11., 0.5):

        s = (np.fabs(D['log10Mstar_30']-log10Mstar)<0.25)

        # galaxy indices meeting criteria
        i_ = np.arange(len(s))[s]
        print(log10Mstar, len(i_))

        age = np.array([])
        Z = np.array([])
        w = np.array([])
        for i in i_:

            w = np.concatenate((w, pD['S_MassInitial'][i]*D['weight'][i]))
            age = np.concatenate((age, pD['S_Age'][i]))
            Z = np.concatenate((Z, pD['S_Z'][i]))

        N, _, _ = np.histogram2d(np.log10(age), np.log10(Z), bins = [age_bins, Z_bins], weights = w)
        O[z][log10Mstar] = N


pickle.dump(O, open('data/stacked_sfzh.p','wb'))
