
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})


x = 'log10Mstar_30'
y = 'range'

D = pickle.load(open('stats.p','rb'))


print(D[5])


s = {}
for z in zeds:
    D[z]['range'] = np.log10(D[z]['Q0.842']/D[z]['Q0.158'])
    print(np.median(D[z]['range']))
    s[z] = D[z]['s']


labels[y] = r'(P_{84.2}-P_{15.8})'
limits[y] = [0.5,2.5]
limits[x][0] = s_limit[x]


# fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True, zevo_cmap = flares_utility.colors.redshift_cmap)
fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, add_weighted_range = True)




fig.savefig(f'figs/Zrange.pdf')
# fig.savefig(f'figs/moments.png')
# fig.savefig(f'figs/combined_redshift_{x}.png')
