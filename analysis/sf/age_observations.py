
import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii

import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')

# fl.explore()

halo = fl.halos

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = fl.tags[-3]  # --- select tag -3 = z=7


s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})

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




Tachella21 = ascii.read('obs/table_result_eazy.cat')


for tag, z, ax in zip(fl.tags, fl.zeds, axes):

    add_legend = False


    # add Tachella21

    s = np.fabs(Tachella21['redshift_q50']-z)<0.51

    if len(Tachella21['log_stellar_mass_q50'][s])>0:

        add_legend = True

        x = Tachella21['log_stellar_mass_q50'][s]
        y = Tachella21['time_50_q50'][s]*1E3
        xerr = (x-Tachella21['log_stellar_mass_q16'][s], Tachella21['log_stellar_mass_q84'][s]-x)
        yerr = (y-(Tachella21['time_50_q16'][s]*1E3), (Tachella21['time_50_q84'][s]*1E3)-y)

        ax.errorbar(x, y, xerr=xerr, yerr=yerr, color='r', markersize=2, label = rf'$\rm Tachella+21$', marker = 'o', linestyle='none', elinewidth = 1)



    if add_legend:
        ax.legend(fontsize = 8)









fig.savefig(f'figs/age_observations.pdf')
fig.savefig(f'figs/age_observations.png')
