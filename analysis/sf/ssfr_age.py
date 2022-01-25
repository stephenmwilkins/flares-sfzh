
import numpy as np
import matplotlib.cm as cm

import pickle

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'50Myr', 'name': f'SFR_50', 'log10': True})
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})


Dp = pickle.load(open('moments_and_percentiles.p','rb'))


x_ = ['log10Mstar_30', 'log10FUV']

D = {}
s = {}
s['log10Mstar_30'] = {}
s['log10FUV'] = {}
for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9

    D[z]['age'] = Dp[z]['P0.5']*1E3
    D[z]['log10age'] = np.log10(D[z]['age'])

    for x in x_:
        s[x][z] = D[z][x]>s_limit[x]

    print(len(D[z]['log10sSFR']), len(D[z]['log10Mstar_30']), len(D[z]['log10FUV']), len(D[z]['log10age']))




# --- get default limits and modify them to match the selection range

cmap = {'log10FUV': cm.viridis, 'log10Mstar_30': cm.inferno}


# for y in ['log10age', 'log10sSFR', 'log10Z']:
for y in ['log10sSFR']: #'log10age','age',

    print(y)

    for x, z in zip(x_, x_[::-1]): #the colour map is for the other parameter

        limits = flares_utility.limits.limits
        limits[x][0] = s_limit[x]

        fig, ax = flares_utility.plt.linear_redshift(D, zeds, x, y, s[x], limits = limits, scatter_colour_quantity = z, scatter_cmap = cmap[x], rows=2)

        fig.savefig(f'figs/{y}_{x}.pdf')
        fig.savefig(f'figs/{y}_{x}.png')
        # fig.savefig(f'figs/combined_redshift_{x}.png')
