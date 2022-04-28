
import pickle

import numpy as np
import matplotlib.cm as cm


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': 'Galaxy/Metallicity/', 'dataset': f'MassWeightedStellarZ', 'name': 'Zstar', 'log10': True})


x = 'log10Mstar_30'
y = 'log10Zstar'

D = {}
s = {}


for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    # print(np.median(D[z]['log10age']))
    # print(np.median(D[z]['log10Mstar_30']))

    s[z] = D[z][x]>s_limit[x]

    # print(len(D[z][x][s[z]]))

    D[z]['ldelta'] = np.log10(1+D[z]['delta'])



limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift_density(D, zeds, x, y, s, limits = limits)

fig.savefig(f'figs/environment_log10Z.pdf')
# fig.savefig(f'figs/{y}_environment.png')
