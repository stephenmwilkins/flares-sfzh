
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


t = 'truncnorm'

s = {}
D = {}

for z, tag in zip(a.zeds[:-1], a.tags):

    D[z] = a.get_datasets(tag, quantities)

    d = pickle.load(open(f'distribution_parameters/{z}.p','rb'))

    D[z]['KS'] =  d[t]['KS']
    D[z]['scale'] =  d[t]['p'][:,0]
    D[z]['loc'] =  d[t]['p'][:,1]
    s[z] = D[z][x]>8.5


properties = ['KS','scale','loc']

limits = flares_utility.limits.limits

limits['KS'] = [0, 0.2]
limits['scale'] = [-500, 500]
limits['loc'] = [-500, 500]


limits[x][0] = s_limit[x]

# fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True, zevo_cmap = flares_utility.colors.redshift_cmap)
fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds[:-1], x, properties, s, limits = limits, scatter = False, add_weighted_range = True)




fig.savefig(f'figs/truncnorm.pdf')
