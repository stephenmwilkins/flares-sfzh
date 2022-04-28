
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


O = {}

for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    N = len(D['log10Mstar_30'])

    print(z, N, len(D['log10Mstar_30'][D['log10Mstar_30']>8.0]))

    # --- get particle datasets and measure properties
    pD = a.get_particle_datasets(tag)



    # --- define the outputs

    O[z] = {}
    for t in ['A','B','C']:
        O[z][t] = {}
        for t2 in ['slope', 'intercept', 'r', 'p', 'se']:
            O[z][t][t2] = np.zeros(N)


    for i, (age, Z, massinitial, mass) in enumerate(zip(pD['S_Age'], pD['S_Z'], pD['S_MassInitial'], pD['S_Mass'])):
        if len(Z)>0:

            Z[Z==0] = 1E-5

            # --- calculate the linear fit between age and log10(Z)

            slope, intercept, r, p, se = linregress(age, Z)
            O[z]['A']['slope'][i] = slope
            O[z]['A']['intercept'][i] = intercept
            O[z]['A']['r'][i] = r
            O[z]['A']['p'][i] = p
            O[z]['A']['se'][i] = se


            slope, intercept, r, p, se = linregress(age, np.log10(Z))
            O[z]['B']['slope'][i] = slope
            O[z]['B']['intercept'][i] = intercept
            O[z]['B']['r'][i] = r
            O[z]['B']['p'][i] = p
            O[z]['B']['se'][i] = se

            slope, intercept, r, p, se = linregress(np.log10(age), np.log10(Z))
            O[z]['C']['slope'][i] = slope
            O[z]['C']['intercept'][i] = intercept
            O[z]['C']['r'][i] = r
            O[z]['C']['p'][i] = p
            O[z]['C']['se'][i] = se



pickle.dump(O, open('data/linregress.p','wb'))
