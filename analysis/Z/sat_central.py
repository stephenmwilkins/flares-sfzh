
import numpy as np
import matplotlib.cm as cm

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
quantities.append({'path': 'Galaxy', 'dataset': 'SubGroupNumber', 'name': None, 'log10': False})
quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_10', 'name': None, 'log10': True})

D = fa.get_datasets(fl, tag, quantities)


print(D['SubGroupNumber'])


x = 'log10SFR_10'
y = 'log10SFR_inst_30'

s = D['log10Mstar_30']>8
s_cen = s&(D['SubGroupNumber']==0)
s_sat = s&~(D['SubGroupNumber']==0)

fig, ax = fplt.simple()

# --- plot
ax.scatter(D[x][s_sat],D[y][s_sat], s=1, alpha=0.5, c = 'b', label = 'satellites')
ax.scatter(D[x][s_cen],D[y][s_cen], s=1, alpha=0.5, c = 'r', label = 'centrals')

ax.legend()

ax.set_xlim(fa.limits[x])
ax.set_ylim(fa.limits[y])

ax.set_ylabel(rf'$\rm {fa.labels[y]}$', fontsize = 9)
ax.set_xlabel(rf'$\rm {fa.labels[x]}$', fontsize = 9)

fig.savefig(f'figs/sat_central.pdf')
# fig.savefig(f'figs/combined_redshift_{x}.png')
