
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


D = pickle.load(open('moments_and_percentiles.p','rb'))


x = 'log10Mstar_30'
s = {}

for z in D.keys():
    D[z]['age'] = D[z]['P0.5']
    D[z]['timescale'] = (D[z]['P0.8']-D[z]['P0.2'])
    s[z] = D[z][f'{x}_s']


x = 'log10Mstar_30'
y = 'timescale'


limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift(D, zeds, x, y, s, limits = limits, scatter = False, add_weighted_range = True)




fig.savefig(f'figs/timescale.pdf')
fig.savefig(f'figs/timescale.png')
