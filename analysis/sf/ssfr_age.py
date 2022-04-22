
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


x = 'log10Mstar_30'
z = 'log10FUV'

D = {}
s = {}

for tag, zed in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[zed] = a.get_datasets(tag, quantities)

    D[zed]['log10sSFR'] = D[zed]['log10SFR_50'] - D[zed]['log10Mstar_30'] + 9

    D[zed]['age'] = Dp[zed]['P0.5']#*1E3
    D[zed]['log10age'] = np.log10(D[zed]['age'])

    s[zed] = D[zed][x]>s_limit[x]




# for y in ['log10age', 'log10sSFR', 'log10Z']:
for y in ['log10sSFR','log10age']: #'log10age','age',


    limits = flares_utility.limits.limits
    limits[x][0] = s_limit[x]

    fig, ax = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter_colour_quantity = z, rows=2)

    fig.savefig(f'figs/{y}.pdf')
    fig.savefig(f'figs/{y}.png')
    # fig.savefig(f'figs/combined_redshift_{x}.png')


    fig, ax = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter_colour_quantity = z, rows=1)

    fig.savefig(f'figs/{y}_compact.pdf')
    fig.savefig(f'figs/{y}_compact.png')
    # fig.savefig(f'figs/combined_redshift_{x}.png')
