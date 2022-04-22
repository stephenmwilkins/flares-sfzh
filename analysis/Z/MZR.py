

# Import CMasher to register colormaps
import cmasher as cmr

import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii



import flare.obs.literature.age as age_observations

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds




# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy/Metallicity/', 'dataset': f'MassWeightedStellarZ', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})




# x = 'log10FUV'
x = 'log10Mstar_30'
y = 'log10MassWeightedStellarZ'

D = {}
s = {}

for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)
    s[z] = D[z][x]>s_limit[x]


labels['log10MassWeightedStellarZ'] = 'log_{10}(Z)'

limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, rows=2, add_weighted_range = True, bins = 10, weighted = True)

for ax in axes:
    ax.set_xticks(np.arange(9, 12, 1.0))
    ax.set_yticks(np.arange(-3, -1, 0.5))



# --- add observational comparisons


# --- determine the number of observational studies


fig.savefig(f'figs/MZR.pdf')
