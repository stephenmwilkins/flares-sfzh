
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})


x = 'log10Mstar_30'
y = 'rlog10a'

D = pickle.load(open('stats.p','rb'))
D2 = pickle.load(open('moments.p','rb'))

s = {}
for z in zeds:
    s[z] = D2[z]['s']


labels[y] = 'r'
limits[y] = [-0.75,0.2]
limits[x][0] = s_limit[x]


# fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True, zevo_cmap = flares_utility.colors.redshift_cmap)
fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, add_weighted_range = True)

for ax in axes:
    ax.axhline(0.0, c='k',lw=3, alpha=0.1)


fig.savefig(f'figs/Zr.pdf')
# fig.savefig(f'figs/moments.png')
# fig.savefig(f'figs/combined_redshift_{x}.png')
