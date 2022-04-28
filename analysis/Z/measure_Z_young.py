
import numpy as np
import pickle

import flares_utility.analyse
import flares_utility.stats

from scipy.stats import pearsonr

filename = flares_utility.analyse.flares_master_file

a = flares_utility.analyse.analyse_flares(filename, default_tags = False)

# a.list_datasets()


x = 'log10Mstar_30'


quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})


D = {}
O = {}

for tag, z in zip(a.tags, a.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    # print(z, len(D[z]['log10Mstar_30']), len(D[z]['log10Mstar_30'][D[z]['log10Mstar_30']>8.0]))

    # --- get particle datasets and measure properties
    pD = a.get_particle_datasets(tag)

    # --- define the outputs

    O[z] = np.zeros(len(D[z]['log10Mstar_30']))


    for i, (age, Z, massinitial, mass) in enumerate(zip(pD['S_Age'], pD['S_Z'], pD['S_MassInitial'], pD['S_Mass'])):

        s = age<10

        if len(Z[s])>1:

            Z[Z==0] = 1E-6

            O[z][i] =  flares_utility.stats.weighted_median(Z[s], massinitial[s])




pickle.dump(O, open('data/young.p','wb'))
