
import numpy as np
import matplotlib.cm as cm

import pickle

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

quantities.append({'path': 'Galaxy/Metallicity', 'dataset': 'MassWeightedStellarZ', 'name': 'Z', 'log10': True})

quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})



D = {}
s = {}
x = 'log10Mstar_30'

for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)
    s[z] = D[z][x]>s_limit[x]



# --- get default limits and modify them to match the selection range

cmap = {'log10FUV': cm.viridis, 'log10Mstar_30': cm.inferno}


y = 'log10Z'
z = 'log10FUV'

limits = fa.limits
limits[x][0] = s_limit[x]

fig, axes = fa.linear_redshift(D, fl.zeds, x, y, s, limits = limits, scatter_colour_quantity = z, scatter_cmap = cmap[x], rows=1)

for ax in axes:
    ax.axhline(np.log10(0.0112), c='k', alpha=0.1, lw=1)


fig.savefig(f'figs/Z.pdf')
fig.savefig(f'figs/Z.png')
