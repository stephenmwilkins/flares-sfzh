
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



bins = np.arange(-6.,0.,0.1)

for tag, z in zip(a.tags, a.zeds):

    print(z, '-'*20)
    O[z] = {}

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    pD = a.get_particle_datasets(tag)

    for log10Mstar in np.arange(8.75, 11., 0.5):

        O[z][log10Mstar] = {}
        s = (np.fabs(D['log10Mstar_30']-log10Mstar)<0.25)

        for ia, (al, au) in enumerate([[0, 50],[50, 200],[200, 1000]]):

            # galaxy indices meeting criteria
            i_ = np.arange(len(s))[s]
            print(log10Mstar, len(i_))

            o = np.array([])
            for i in i_:

                sa = (pD['S_Age'][i]>al)&(pD['S_Age'][i]<au)

                print(i, np.sum(sa))
                if np.sum(sa)>0:
                    o = np.concatenate((o, pD['S_Z'][i][sa]))



            N, _ = np.histogram(np.log10(o), bins = log10_bins)
            O[z][log10Mstar][ia] = N



pickle.dump(O, open('data/Z_age.p','wb'))
