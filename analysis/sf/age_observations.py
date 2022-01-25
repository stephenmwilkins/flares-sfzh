

# Import CMasher to register colormaps
import cmasher as cmr

import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds




# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

Dp = pickle.load(open('moments_and_percentiles.p','rb'))


x = 'log10Mstar_30'
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

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, rows=2, add_weighted_range = True)


Tacchella21 = {}

Tacchella21['continuity'] = ascii.read('obs/table_result_eazy.cat')
Tacchella21['parametric'] = ascii.read('obs/table_result_eazy_param.cat')
Tacchella21['bursty'] = ascii.read('obs/table_result_eazy_bursty.cat')


for tag, z, ax in zip(tags, zeds, axes):

    add_legend = False


    colors = cmr.take_cmap_colors('cmr.apple', 3, cmap_range=(0.15, 0.85), return_fmt='hex')

    for prior, c in zip(['continuity','parametric','bursty'], colors):

        s = np.fabs(Tacchella21[prior]['redshift_q50']-z)<0.51

        if len(Tacchella21[prior]['log_stellar_mass_q50'][s])>0:

            add_legend = True

            x = Tacchella21[prior]['log_stellar_mass_q50'][s]
            y = Tacchella21[prior]['time_50_q50'][s]*1E3
            xerr = (x-Tacchella21[prior]['log_stellar_mass_q16'][s], Tacchella21[prior]['log_stellar_mass_q84'][s]-x)
            yerr = (y-(Tacchella21[prior]['time_50_q16'][s]*1E3), (Tacchella21[prior]['time_50_q84'][s]*1E3)-y)

            ax.errorbar(x, y, xerr=xerr, yerr=yerr, color=c, markersize=2, label = rf'$\rm Tacchella+21\ {prior}\ prior$', marker = 'o', linestyle='none', elinewidth = 1)



    if add_legend:
        ax.legend(fontsize = 7, labelspacing = 0.05)









fig.savefig(f'figs/age_observations.pdf')
fig.savefig(f'figs/age_observations.png')
