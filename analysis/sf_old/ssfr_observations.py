

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
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_30', 'name': f'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/SFR_30', 'dataset': f'SFR_50_Myr', 'name': f'SFR_50', 'log10': True})



y = 'log10sSFR'

D = {}
s = {}
s['log10FUV'] = {}
s['log10Mstar_30'] = {}

for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9



    for x in ['log10FUV','log10Mstar_30']:
        s[x][z] = D[z][x]>s_limit[x]




x = 'log10Mstar_30'

limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s[x], limits = limits, scatter = False, rows=2, add_weighted_range = True, bins = 20)


# --- add observational comparisons

markers = ['o','d','s']

for ax, z in zip(axes, a.zeds):
    if z in ssfr_observations.observed.keys():

        colors = cmr.take_cmap_colors('cmr.chroma', len(ssfr_observations.observed[z]), cmap_range=(0.15, 0.85))

        for obs, marker, c in zip(ssfr_observations.observed[z], markers, colors):

            print(obs.label)
            if obs.dt == 'io':

                # ax.errorbar(obs.log10Mstar, obs.age, xerr = obs.log10Mstar_err, yerr = obs.age_err, c='k',fmt='o',elinewidth=1, ms=3, label = rf'$\rm {obs.label}$')

                ax.scatter(obs.log10Mstar, obs.log10sSFR, c=[c], s=3, marker=marker, label = rf'$\rm {obs.label}$')

            if obs.dt == 'binned':
                print(type(obs.log10Mstar[z]))

                if type(obs.log10Mstar[z])==np.ndarray:

                    ax.errorbar(obs.log10Mstar[z], obs.log10sSFR[z], xerr = obs.log10Mstar_err[z], yerr = obs.log10sSFR_err[z], c=c, fmt='o', elinewidth=1, ms=3, label = rf'$\rm {obs.label}$')


    # ax.legend(fontsize=7, handletextpad = 0.0, loc = 'upper right')
    ax.legend(fontsize=7, handletextpad = 0.0)
    # ax.set_xticks(np.arange(29, 31, 1.0))



fig.savefig(f'figs/ssfr_observations_log10Mstar.pdf')


fig.clf()

x = 'log10FUV'

limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s[x], limits = limits, scatter = False, rows=2, add_weighted_range = True, bins = 20)


# --- add observational comparisons

markers = ['o','d','s']

for ax, z in zip(axes, a.zeds):
    if z in ssfr_observations.observed.keys():

        colors = cmr.take_cmap_colors('cmr.chroma', len(ssfr_observations.observed[z]), cmap_range=(0.15, 0.85))

        for obs, marker, c in zip(ssfr_observations.observed[z], markers, colors):

            print(obs.label)
            if obs.dt == 'io':

                # ax.errorbar(obs.log10Mstar, obs.age, xerr = obs.log10Mstar_err, yerr = obs.age_err, c='k',fmt='o',elinewidth=1, ms=3, label = rf'$\rm {obs.label}$')

                ax.scatter(obs.log10L1500, obs.log10sSFR, c=[c], s=3, marker=marker, label = rf'$\rm {obs.label}$')

            if obs.dt == 'binned':

                if type(obs.log10L1500[z])==np.array:

                    ax.errorbar(obs.log10L1500[z], obs.log10sSFR[z], xerr = obs.log10L1500_err[z], yerr = obs.log10sSFR_err[z], c='k', fmt='o', elinewidth=1, ms=3, label = rf'$\rm {obs.label}$')


    ax.legend(fontsize=7, handletextpad = 0.0)
    ax.set_xticks(np.arange(29, 31, 1.0))



fig.savefig(f'figs/ssfr_observations_log10FUV.pdf')
fig.savefig(f'figs/ssfr_observations_log10FUV.png')
