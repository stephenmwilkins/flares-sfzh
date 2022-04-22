
import numpy as np
import pickle

from load import *


s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})

x_ = ['log10Mstar_30', 'log10FUV']

D = {}

for tag, z in zip(a.tags, a.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    print(z, len(D[z]['log10Mstar_30']), len(D[z]['log10Mstar_30'][D[z]['log10Mstar_30']>8.0]))

    # --- get particle datasets and measure properties
    pD = a.get_particle_datasets(tag)


    # --- measure the percentiles
    percentiles = [0.9,0.8,0.5,0.2,0.1]

    for p in percentiles:
        D[z][f'P{p}'] = np.zeros(len(D[z]['log10Mstar_30']))

    for i, (ages, massinitial, mass) in enumerate(zip(pD['S_Age'], pD['S_MassInitial'], pD['S_Mass'])):
        # print(np.log10(np.sum(mass)), D[z]['log10Mstar_30'][i]) # sanity check to make sure masses are the same

        if len(ages)>0:
            for p in percentiles:
                D[z][f'P{p}'][i] =  flares_utility.stats.weighted_quantile(ages, p, sample_weight = massinitial)

    # --- measure the moments
    for n in range(1, 5):
        D[z][f'moment{n}'] = np.zeros(len(D[z]['log10Mstar_30']))

    for i, (ages, massinitial) in enumerate(zip(pD['S_Age'], pD['S_MassInitial'])):
        if len(ages)>0:
            for n in range(1, 5):
                D[z][f'moment{n}'][i] =  flares_utility.stats.n_weighted_moment(ages, massinitial, n)

    for x in x_:
        D[z][x+'_s'] = D[z][x]>s_limit[x]


pickle.dump(D, open('moments_and_percentiles.p','wb'))
