


import numpy as np



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
tag = fl.tags[1]  # --- tag 0 = 10
log10Mstar_limit = 8.


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI/', 'dataset': 'FUV', 'name': None, 'log10': True})


# --- get quantities (and weights and deltas)
D = flares_analysis.get_datasets(fl, tag, quantities)

# ----------------------------------------------
# define new quantities
D['log10sSFR'] = D['log10SFR_inst_30'] - D['log10Mstar_30'] + 9.

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

# --- get default limits and modify them to match the selection range
labels = flares_analysis.labels


x = 'log10Mstar_30'
y = 'log10sSFR'
z = 'log10FUV' # used for the colour bar

# --- make plot with colour bar plot
fig, ax, cax, hax = flares_analysis.simple_wcbar_whist(D, x, y, z, s, limits = limits, labels = labels, cmap = cm.coolwarm)


fig.savefig(f'figs/ssfr.pdf')
