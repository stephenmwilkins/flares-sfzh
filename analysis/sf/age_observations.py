

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
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})


Dp = pickle.load(open('moments_and_percentiles.p','rb'))


# x = 'log10FUV'
x = 'log10Mstar_30'
y = 'log10age'

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

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, rows=2, add_weighted_range = True, bins = 10, weighted = True)





# --- add observational comparisons


# --- determine the number of observational studies

observations = age_observations

observation_list = []
added_to_legend = []

for z in a.zeds:
    if z in observations.observed.keys():
        for obs in observations.observed[z]:
            observation_list.append(obs.label)


cmap = 'cmr.chroma'
colors = dict(zip(observation_list, cmr.take_cmap_colors(cmap, len(observation_list), cmap_range=(0.15, 0.85))))
markers = dict(zip(observation_list,  ['o','v','D','s','^','p','h','d']))

for ax, z in zip(axes, a.zeds):
    if z in observations.observed.keys():
        for obs in observations.observed[z]:

            id = obs.label

            if id not in added_to_legend:
                label = rf'$\rm {id}$'
                added_to_legend.append(id)
            else:
                label = None

            if obs.dt == 'io':
                ax.scatter(obs.log10Mstar, obs.log10age, c=[colors[id]], s=3, marker=markers[id], label = label)


        ax.legend(fontsize=7, handletextpad = 0.0)


for ax, z in zip(axes, a.zeds):
    ax.set_xticks(np.arange(9, 12, 1.0))



fig.savefig(f'figs/age_observations.pdf')
fig.savefig(f'figs/age_observations.png')
