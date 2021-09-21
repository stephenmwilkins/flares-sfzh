
import pickle

import numpy as np
import matplotlib.cm as cm


import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

# fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
fl = flares.flares('/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5', sim_type='FLARES')

# fl.explore()




s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/SFR_30', 'dataset': f'SFR_50_Myr', 'name': f'SFR_50', 'log10': True})


Dp = pickle.load(open('percentiles.p','rb'))

x = 'log10Mstar_30'

D = {}
s = {}


for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9

    D[z]['age'] = Dp[z]['P0.5']*1E3 # Myr
    D[z]['log10age'] = np.log10(D[z]['age'])

    # print(np.median(D[z]['log10age']))
    # print(np.median(D[z]['log10Mstar_30']))

    s[z] = D[z][x]>s_limit[x]

    # print(len(D[z][x][s[z]]))

    D[z]['ldelta'] = np.log10(1+D[z]['delta'])



for y in ['log10age','log10sSFR']:

    limits = fa.limits
    limits[x][0] = s_limit[x]

    fig = fa.linear_redshift_density(D, fl.zeds, 'log10Mstar_30', y, s, limits = limits, rows=1)

    fig.savefig(f'figs/{y}_environment.pdf')
    fig.savefig(f'figs/{y}_environment.png')
