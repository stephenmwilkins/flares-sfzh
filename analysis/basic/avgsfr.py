import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import cmasher as cmr

cmap = cmr.neon

import flares
import flares_analysis as fa
import flare.plt as fplt

from flares_utility import analyse
from flares_utility import stats as flares_stats

import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data and load analyser
a = analyse.analyse_flares(analyse.flares_master_file, default_tags = False)

# ----------------------------------------------------------------------
# --- list datasets (specifically for the 1st sim/tag)
# a.list_datasets()

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = a.tags[-1]  # --- tag 0 = 10
z = a.zed_from_tag[tag] # get redshift of that tag
print(tag, z, a.tag_from_zed[z]) # print, but also shows how to the tag from zed


timescales = [1,5,10,20,50,100,200] # sfr averaging timescales
r = 30 # radius

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]
quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'{r}', 'name': 'Mstar', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/{r}', 'dataset': f'inst', 'name': 'SFR_inst', 'log10': True})
for t in timescales:
    quantities.append({'path': f'Galaxy/SFR_aperture/{r}', 'dataset': f'{t}Myr', 'name': f'SFR_{t}', 'log10': True})



# --- get quantities (and weights and deltas)
D = a.get_datasets(tag, quantities)

# D['log10Mstar'] -= 10. # REMOVE LATER


print(np.median(D[f'log10SFR_inst']))

# D[f'log10SFR_inst'] =+ -10

D[f'log10sSFR_inst'] = D[f'log10SFR_inst'] - D[f'log10Mstar']  + 9. #aperture based

for t in timescales:
    D[f'log10sSFR_{t}'] = D[f'log10SFR_{t}'] - D[f'log10Mstar'] + 9. #aperture based


limits = {}
limits['log10Mstar'] = [8.05,12]
limits['log10SFR_100'] = [-1.,3.]

labels = {}
labelss = {} # short label
labels['log10Mstar'] = r'log_{10}(M_{\star}/M_{\odot})'
labelss['log10Mstar'] = 'M_{\star}'
labels['log10SFR'] = r'log_{10}(SFR/M_{\odot}\ yr^{-1})'
labelss['log10SFR'] = 'SFR'
labels['log10sSFR'] = r'log_{10}(sSFR/Gyr^{-1})'
labelss['log10sSFR'] = 'sSFR'




# --- individual plots

x = 'log10Mstar'

for y in ['log10SFR', 'log10sSFR']:

    print('--'*20)
    print(y)


    fig, ax = fplt.simple_sm(size=2.5)

    ax.axhline(0.0, color='k', lw=2, alpha=0.2)

    for i,t in enumerate(timescales):

        c = cmap(i/len(timescales))

        # --- weighted median Lines
        R = D[f'{y}_{t}']-D[f'{y}_50']

        print(t, np.min(R), np.median(R), np.max(R))

        ax = fa.add_median_line(ax, D[x], R, D['weight'], limits[x], c=c, label = rf'$\rm {t}\ Myr $')


    R = D[f'{y}_inst']-D[f'{y}_50']
    print('inst', np.min(R), np.median(R), np.max(R))
    print(R)
    ax = fa.add_median_line(ax, D[x], R, D['weight'], limits[x], c='k', label = rf'$\rm instantaneous $')



    ax.legend(fontsize = 6, labelspacing = 0.05)

    ax.set_xlim(limits[x])
    ax.set_ylim([-0.5,0.3])
    # ax.set_ylim([0, 3])

    ax.set_xlabel(rf'$\rm {labels[x]}$', fontsize = 9)
    ax.set_ylabel(rf'$\rm log_{{10}}({labelss[y]}/{labelss[y]}_{{50}})$', fontsize = 9)

    fig.savefig(f'figs/avgsfr_{y}.pdf')
