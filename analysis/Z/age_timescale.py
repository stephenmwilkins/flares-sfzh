
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle


import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')

s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}






D = pickle.load(open('percentiles.p','rb'))

print(list(D.keys()))


for z in D.keys():
    D[z]['age'] = D[z]['P0.5']*1E3
    D[z]['timescale'] = (D[z]['P0.8']-D[z]['P0.2'])*1E3

properties = ['age','timescale']


s = pickle.load(open('s.p','rb'))

x = 'log10Mstar_30'

limits = fa.limits
limits[x][0] = s_limit[x]

fig, axes = fa.linear_redshift_mcol(D, fl.zeds, x, properties, s[x], limits = limits, scatter_colour_quantity = 'log10FUV', scatter_cmap = cm.inferno, add_linear_fit = False)

#
# # normalised variance, should be 1 for exp
# for ax in axes[1,:]:
#     ax.axhline(1.0, lw=1, c='k',alpha=0.2)
#
# # skew, should be 2 for exp
# for ax in axes[2,:]:
#     ax.axhline(2.0, lw=1, c='k',alpha=0.2)
#
# # kurtosis, should be 6 for exp
# for ax in axes[3,:]:
#     ax.axhline(6.0, lw=1, c='k',alpha=0.2)


fig.savefig(f'figs/age_timescale.pdf')
fig.savefig(f'figs/age_timescale.png')
# fig.savefig(f'figs/combined_redshift_{x}.png')
