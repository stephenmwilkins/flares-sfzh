

# Import CMasher to register colormaps
import cmasher as cmr

import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii

import flare.obs.literature.ssfr as ssfr_observations


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'50Myr', 'name': f'SFR_50', 'log10': True})


x = 'log10Mstar_30'
y = 'log10sSFR'

D = {}
s = {}


for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9

    s[z] = D[z][x]>s_limit[x]




x = 'log10Mstar_30'

limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, rows=2, add_weighted_range = True, bins = 10, weighted = True)




# --- determine the number of observational studies

observations = ssfr_observations

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
                ax.scatter(obs.log10Mstar, obs.log10sSFR, c=[colors[id]], s=3, marker=markers[id], label = label)
            if obs.dt == 'binned':

                if type(obs.log10Mstar[z])==np.ndarray:
                    ax.errorbar(obs.log10Mstar[z], obs.log10sSFR[z], xerr = obs.log10Mstar_err[z], yerr = obs.log10sSFR_err[z], fmt='o', elinewidth=1, ms=5, label = label, c='k', mec='k', mfc=colors[id])

        ax.legend(fontsize=7, handletextpad = 0.0)


for ax, z in zip(axes, a.zeds):
    ax.set_xticks(np.arange(9, 12, 1.0))


fig.savefig(f'figs/ssfr_observations.pdf')
