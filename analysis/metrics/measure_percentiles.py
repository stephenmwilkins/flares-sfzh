
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle

import flares
import flares_analysis as fa
import flare.plt as fplt



def n_weighted_moment(values, weights, n):

    assert n>0 & (values.shape == weights.shape)
    w_avg = np.average(values, weights = weights)
    w_var = np.sum(weights * (values - w_avg)**2)/np.sum(weights)

    if n==1:
        return w_avg
    elif n==2:
        return w_var
    else:
        w_std = np.sqrt(w_var)
        return np.sum(weights * ((values - w_avg)/w_std)**n)/np.sum(weights)
              #Same as np.average(((values - w_avg)/w_std)**n, weights=weights)



# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')

# fl.explore()

halo = fl.halos

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = fl.tags[-3]  # --- select tag -3 = z=7


s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_100', 'name': None, 'log10': True})
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})


x_ = ['log10Mstar_30', 'log10FUV']

D = {}
s = {}
s['log10Mstar_30'] = {}
s['log10FUV'] = {}
for tag, z in zip(fl.tags, fl.zeds):

    print(z)

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_100'] - D[z]['log10Mstar_30'] + 9



    # --- get particle datasets and measure properties
    pD = fa.get_particle_datasets(fl, tag)


    # --- measure the moments



    percentiles = [0.9,0.5,0.1]
    for p in percentiles:
        D[z][f'P{p}'] = np.zeros(len(D[z]['log10Mstar_30']))

    for i, (ages, massinitial) in enumerate(zip(pD['Age'], pD['MassInitial'])):
        for p in percentiles:
            D[z][f'P{p}'][i] =  flares.weighted_quantile(ages, p, sample_weight = massinitial)

    for x in x_:
        s[x][z] = D[z][x]>s_limit[x]

pickle.dump(D, open('percentiles.p','wb'))
pickle.dump(s, open('s.p','wb'))
