

# Import CMasher to register colormaps
import cmasher as cmr

import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii

import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

# fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
fl = flares.flares('/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5', sim_type='FLARES')



s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_30', 'name': None, 'log10': True})

Dp = pickle.load(open('percentiles.p','rb'))

x = 'log10Mstar_30'
y = 'age'

D = {}
s = {}

for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['age'] = Dp[z]['P0.5']*1E3
    D[z]['log10age'] = np.log10(D[z]['age'])

    s[z] = D[z][x]>s_limit[x]






limits = fa.limits
limits[x][0] = s_limit[x]

fig, axes = fa.linear_redshift(D, fl.zeds, x, y, s, limits = limits, scatter = False, rows=2, add_weighted_range = True)


Tacchella21 = {}

Tacchella21['continuity'] = ascii.read('obs/table_result_eazy.cat')
Tacchella21['parametric'] = ascii.read('obs/table_result_eazy_param.cat')
Tacchella21['bursty'] = ascii.read('obs/table_result_eazy_bursty.cat')


for tag, z, ax in zip(fl.tags, fl.zeds, axes):

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
