
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

properties = ['KS','scale','loc']
x = 'log10Mstar_30'


t = 'truncnorm'

D = pickle.load(open('distribution_parameters.p','rb'))
D2 = pickle.load(open('moments_and_percentiles.p','rb'))

zeds = [10.,10.,10.,10.]


s = {}
for z in zeds:
    D[z][t]['scale'] =  D[z][t]['p'][:,0]
    D[z][t]['loc'] =  D[z][t]['p'][:,1]

    s[z] = D2[z][f'{x}_s']




limits = flares_utility.limits.limits

limits['KS'] = [0, 0.2]
limits['scale'] = [0, 500]
labels['loc'] = [0, 500]


limits[x][0] = s_limit[x]

# fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True, zevo_cmap = flares_utility.colors.redshift_cmap)
fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True)




fig.savefig(f'figs/truncnorm.pdf')
