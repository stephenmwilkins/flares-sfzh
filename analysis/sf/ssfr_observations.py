
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
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_100', 'name': 'SFR', 'log10': True})

x = 'log10Mstar_30'
y = 'log10sSFR'

D = {}
s = {}

for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR'] - D[z]['log10Mstar_30'] + 9

    s[z] = D[z][x]>s_limit[x]



limits = fa.limits
limits[x][0] = s_limit[x]

fig, axes = fa.linear_redshift(D, fl.zeds, x, y, s, limits = limits, scatter = False, rows=2, add_weighted_range = True)


observations = {}
observations['Salmon+15'] = {}
observations['Salmon+15']['redshifts'] = [5.0, 6.0]
observations['Salmon+15']['c'] = 'b'
observations['Salmon+15']['s'] = 4

observations['Salmon+15'][5.0] = {}
observations['Salmon+15'][5.0]['log10M*'] = np.array([9.0,9.25,9.50,9.75,10.,10.25])
observations['Salmon+15'][5.0]['log10SFR'] = np.array([0.88,1.04,1.12,1.23,1.46,1.62])
observations['Salmon+15'][5.0]['error'] = np.array([0.42,0.38,0.41,0.43,0.31,0.37])

observations['Salmon+15'][6.0] = {}
observations['Salmon+15'][6.0]['log10M*'] = np.array([9.0,9.25,9.50,9.75,10.])
observations['Salmon+15'][6.0]['log10SFR'] = np.array([0.92,1.07,1.27,1.40,1.147])
observations['Salmon+15'][6.0]['error'] = np.array([0.19,0.21,0.35,0.26,0.07])

# --- calculate sSFRs
for z in observations['Salmon+15']['redshifts']:
    observations['Salmon+15'][z]['log10sSFR'] = observations['Salmon+15'][z]['log10SFR']-observations['Salmon+15'][z]['log10M*']+9.0 # convert to sSFR/Gyr


Tachella21 = ascii.read('obs/table_result_eazy.cat')


for tag, z, ax in zip(fl.tags, fl.zeds, axes):

    add_legend = False

    for obsname in ['Salmon+15']:

        for zobs in observations[obsname]['redshifts']:

            obs = observations[obsname][zobs]

            if np.fabs(zobs-z)<0.51:

                add_legend = True
                ax.errorbar(obs['log10M*'], obs['log10sSFR'], yerr = obs['error'], color=observations[obsname]['c'], markersize=observations[obsname]['s'], label = rf'$\rm {obsname}\ (z={zobs})$', marker = 'o', linestyle='none')



    # add Tachella21


    s = np.fabs(Tachella21['redshift_q50']-z)<0.51

    if len(Tachella21['log_stellar_mass_q50'][s])>0:

        add_legend = True

        x = Tachella21['log_stellar_mass_q50'][s]
        y = Tachella21['log_ssfr_100_q50'][s]+9
        xerr = (x-Tachella21['log_stellar_mass_q16'][s], Tachella21['log_stellar_mass_q84'][s]-x)
        yerr = (y-(Tachella21['log_ssfr_100_q16'][s]+9), (Tachella21['log_ssfr_100_q84'][s]+9)-y)

        ax.errorbar(x, y, xerr=xerr, yerr=yerr, color='r', markersize=2, label = rf'$\rm Tachella+21$', marker = 'o', linestyle='none', elinewidth = 1)



    if add_legend:
        ax.legend(fontsize = 8)









fig.savefig(f'figs/ssfr_observations.pdf')
fig.savefig(f'figs/ssfr_observations.png')
