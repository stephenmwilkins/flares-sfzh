
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
quantiles = [0.022, 0.158, 0.5, 0.658, 0.978]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})


D = {}

for tag, z in zip(a.tags, a.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    print(z, len(D[z]['log10Mstar_30']), len(D[z]['log10Mstar_30'][D[z]['log10Mstar_30']>8.0]))

    # --- get particle datasets and measure properties
    pD = a.get_particle_datasets(tag)



    # --- define the outputs

    D[z]['r'] = np.zeros(len(D[z]['log10Mstar_30']))
    D[z]['rlog10a'] = np.zeros(len(D[z]['log10Mstar_30']))
    D[z]['rlog10b'] = np.zeros(len(D[z]['log10Mstar_30']))

    for q in quantiles:
        D[z][f'Q{q}'] = np.zeros(len(D[z]['log10Mstar_30']))


    for i, (age, Z, massinitial, mass) in enumerate(zip(pD['S_Age'], pD['S_Z'], pD['S_MassInitial'], pD['S_Mass'])):
        if len(Z)>0:

            Z[Z==0] = 1E-5

            # --- measure the pearson correlation coefficient of the age/Z distribution
            D[z]['r'][i] = pearsonr(age, Z)[0]
            D[z]['rlog10a'][i] = pearsonr(age, np.log10(Z))[0]
            D[z]['rlog10b'][i] = pearsonr(np.log10(age), np.log10(Z))[0]

            # --- measure the quantiles of the metallicity distribution
            for q in quantiles:
                D[z][f'Q{q}'][i] =  flares_utility.stats.weighted_quantile(Z, q, sample_weight = massinitial)



pickle.dump(D, open('stats.p','wb'))
