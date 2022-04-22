

# Import CMasher to register colormaps
import cmasher as cmr

import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii



import flare.obs.literature.age as age_observations

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds




# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})
# quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_30', 'name': 'Mstar_30', 'log10': True})

Dp = pickle.load(open('moments_and_percentiles.p','rb'))


x = 'log10FUV'
y = 'age'

D = {}
s = {}

for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    D[z]['age'] = Dp[z]['P0.5']
    D[z]['log10age'] = np.log10(D[z]['age'])

    s[z] = D[z][x]>s_limit[x]




limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, rows=2, add_weighted_range = True, bins = 20)


# --- add observational comparisons

markers = ['o','d','s']

for ax, z in zip(axes, a.zeds):
    if z in age_observations.observed.keys():

        colors = cmr.take_cmap_colors('cmr.chroma', len(age_observations.observed[z]), cmap_range=(0.15, 0.85))

        for obs, marker, c in zip(age_observations.observed[z], markers, colors):
            if obs.dt == 'io':

                # ax.errorbar(obs.log10Mstar, obs.age, xerr = obs.log10Mstar_err, yerr = obs.age_err, c='k',fmt='o',elinewidth=1, ms=3, label = rf'$\rm {obs.label}$')

                ax.scatter(obs.log10L1500, obs.age, c=[c], s=3, marker=marker, label = rf'$\rm {obs.label}$')

    ax.legend(fontsize=7, handletextpad = 0.0, loc = 'upper left')
    ax.set_xticks(np.arange(29, 31, 1.0))






fig.savefig(f'figs/age_observations.pdf')
fig.savefig(f'figs/age_observations.png')
