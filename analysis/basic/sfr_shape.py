



import numpy as np
import matplotlib.cm as cm

import flares
import flares_analysis
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
# fl.explore()

halo = fl.halos

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = fl.tags[3]  # --- tag 0 = 10
log10Mstar_limit = 8.5


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_10', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_200', 'name': None, 'log10': True})


# --- get quantities (and weights and deltas)
D = flares_analysis.get_datasets(fl, tag, quantities)

D['log10sSFR'] = D['log10SFR_inst_30'] - D['log10Mstar_30'] + 9.
D['R'] =  D['log10SFR_50'] - D['log10SFR_200']
D['R2'] =  D['log10SFR_10'] - D['log10SFR_50']
# ----------------------------------------------
# define selection
s = D['log10Mstar_30']>log10Mstar_limit

# ----------------------------------------------
# Print number of galaxies meeting the selection
print(f"Total number of galaxies: {len(D['log10Mstar_30'][s])}")


# ----------------------------------------------
# ----------------------------------------------
# plot with colour bar


# --- get default limits and modify them to match the selection range
limits = flares_analysis.limits
limits['log10Mstar_30'] = [log10Mstar_limit, 10.9]
limits['R'] = [-0.5,0.5]
limits['R2'] = limits['R']

# --- get default limits and modify them to match the selection range
labels = flares_analysis.labels



# --- make plot with colour bar plot
fig, ax, cax = flares_analysis.simple_wcbar(D, 'log10Mstar_30', 'R', 'R2', s, limits = limits, labels = labels, cmap = cm.coolwarm_r)

ax.axhline(0.0,c='k', alpha=0.1)

fig.savefig(f'figs/sfr_shape.pdf')

# --- make plot with colour bar plot
fig, ax, cax = flares_analysis.simple_wcbar(D, 'R', 'R2', 'log10Mstar_30', s, limits = limits, labels = labels, cmap = cm.viridis)

ax.axhline(0.0,c='k', alpha=0.1)
ax.axvline(0.0,c='k', alpha=0.1)

fig.savefig(f'figs/sfr_shape2.pdf')



#
# # --- make plot with colour bar plot
# fig, axes = flares_analysis.corner3(D, ['R','log10Mstar_30', 'R2'], s, {'log10Mstar_30': cm.viridis, 'R':cm.coolwarm_r, 'R2': cm.coolwarm_r}, limits = limits, labels = labels, full_width = False)
#
# fig.savefig(f'figs/sfr_shape_corner.pdf')
