

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

quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/SFR_30', 'dataset': f'SFR_50_Myr', 'name': f'SFR_50', 'log10': True})


x = 'log10Mstar_30'
y = 'log10sSFR'

D = {}
s = {}

for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9

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


Tacchella21 = {}
Tacchella21['continuity'] = ascii.read('obs/table_result_eazy.cat')
Tacchella21['parametric'] = ascii.read('obs/table_result_eazy_param.cat')
Tacchella21['bursty'] = ascii.read('obs/table_result_eazy_bursty.cat')



add_Salmon_legend = True
add_Tacchella_legend = True

for tag, z, ax in zip(fl.tags, fl.zeds, axes):

    # Salmon+

    for obsname in ['Salmon+15']:

        for zobs in observations[obsname]['redshifts']:

            obs = observations[obsname][zobs]

            if np.fabs(zobs-z)<0.51: # if points at this redshift

                if add_Salmon_legend:
                    # label = rf'$\rm {obsname}\ (z={zobs})$'
                    label = rf'$\rm {obsname}$'
                    add_Salmon_legend = False
                    print('bang')
                else:
                    label = None

                ax.errorbar(obs['log10M*'], obs['log10sSFR'], yerr = obs['error'], color=observations[obsname]['c'], markersize=observations[obsname]['s'], label = label, marker = 'o', linestyle='none')





    # % Tacchella

    colors = cmr.take_cmap_colors('cmr.apple', 3, cmap_range=(0.15, 0.85), return_fmt='hex')

    if add_Tacchella_legend:
        add_label = True
        add_Tacchella_legend = False
    else:
        add_label = False


    for prior, c in zip(['continuity','parametric','bursty'], colors):

        s = np.fabs(Tacchella21[prior]['redshift_q50']-z)<0.51

        if len(Tacchella21[prior]['log_stellar_mass_q50'][s])>0:

            x = Tacchella21[prior]['log_stellar_mass_q50'][s]
            y = Tacchella21[prior]['log_ssfr_50_q50'][s]+9
            xerr = (x-Tacchella21[prior]['log_stellar_mass_q16'][s], Tacchella21[prior]['log_stellar_mass_q84'][s]-x)
            yerr = (y-(Tacchella21[prior]['log_ssfr_50_q16'][s]+9), (Tacchella21[prior]['log_ssfr_50_q84'][s]+9)-y)

            if add_label:
                label = rf'$\rm Tacchella+21\ {prior}\ prior$'
            else:
                label = None


            ax.errorbar(x, y, xerr=xerr, yerr=yerr, color=c, markersize=2, label = label, marker = 'o', linestyle='none', elinewidth = 1)






    ax.legend(fontsize = 7, labelspacing = 0.05)









fig.savefig(f'figs/ssfr_observations.pdf')
fig.savefig(f'figs/ssfr_observations.png')
