
import numpy as np
import pickle

import flares_utility.analyse
import flares_utility.stats

from scipy.stats import pearsonr, linregress

from load import *


x = 'log10Mstar_30'

s_limit = 8.5

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})


D = {}

for tag, z in zip(a.tags, a.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    N = len(D[z]['log10Mstar_30'])

    print(z, N, len(D[z]['log10Mstar_30'][D[z]['log10Mstar_30']>8.0]))


    # --- get particle datasets and measure properties
    pD = a.get_particle_datasets(tag)

    D[z]['s'] = D[z][x]>s_limit

    # --- define the outputs

    for t in ['A','B','C']:
        D[z][t] = {}
        for t2 in ['slope', 'intercept', 'r', 'p', 'se']:
            D[z][t][t2] = np.zeros(N)


    for i, (age, Z, massinitial, mass) in enumerate(zip(pD['S_Age'], pD['S_Z'], pD['S_MassInitial'], pD['S_Mass'])):
        if len(Z)>0:

            Z[Z==0] = 1E-5

            # --- calculate the linear fit between age and log10(Z)

            slope, intercept, r, p, se = linregress(age, Z)
            D[z]['A']['slope'][i] = slope
            D[z]['A']['intercept'][i] = intercept
            D[z]['A']['r'][i] = r
            D[z]['A']['p'][i] = p
            D[z]['A']['se'][i] = se


            slope, intercept, r, p, se = linregress(age, np.log10(Z))
            D[z]['B']['slope'][i] = slope
            D[z]['B']['intercept'][i] = intercept
            D[z]['B']['r'][i] = r
            D[z]['B']['p'][i] = p
            D[z]['B']['se'][i] = se

            slope, intercept, r, p, se = linregress(np.log10(age), np.log10(Z))
            D[z]['C']['slope'][i] = slope
            D[z]['C']['intercept'][i] = intercept
            D[z]['C']['r'][i] = r
            D[z]['C']['p'][i] = p
            D[z]['C']['se'][i] = se



pickle.dump(D, open('data/linregress.p','wb'))
