
import numpy as np
import matplotlib.cm as cm

import pickle

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds
from astropy.cosmology import Planck18 as cosmo

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'50Myr', 'name': f'SFR_50', 'log10': True})

Dp = pickle.load(open('moments_and_percentiles.p','rb'))


x = 'log10Mstar_30'
z = 'log10FUV'

D = {}
s = {}

for tag, zed in zip(tags, zeds):

    log10aou = np.log10(cosmo.age(zed).value)


    # --- get quantities (and weights and deltas)
    D[zed] = a.get_datasets(tag, quantities)

    D[zed]['log10sSFR'] = D[zed]['log10SFR_50'] - D[zed]['log10Mstar_30'] + 9

    D[zed]['age'] = Dp[zed]['P0.5']#*1E3
    D[zed]['log10age'] = np.log10(D[zed]['age'])

    D[zed]['log10age_aou'] = D[zed]['log10age'] - log10aou - 3
    D[zed]['log10sSFR_aou'] = D[zed]['log10sSFR'] + log10aou

    print(np.median(D[zed]['log10age_aou']))

    s[zed] = D[zed][x]>s_limit[x]




labels['log10age_aou'] = r'\log_{10}(age/t_{uni})'
labels['log10sSFR_aou'] = r'\log_{10}(sSFR/t_{uni}^{-1})'

limits[x][0] = s_limit[x]
limits['log10age_aou'] = [-1.24,-0.5]
limits['log10sSFR_aou'] = [0.01,0.99]

for y, y_ in zip(['log10sSFR_aou','log10age_aou'], ['ssfr','age']):

    fig, ax = flares_utility.plt.zevo(D, zeds, x, y, s, limits = limits, labels = labels, bins = 10, fig_size = (3.5, 2.25))

    fig.savefig(f'figs/{y_}_evo.pdf')
