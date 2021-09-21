
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle


import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

# fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
fl = flares.flares('/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5', sim_type='FLARES')

s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}


D = pickle.load(open('percentiles.p','rb'))


for z in D.keys():
    D[z]['age'] = D[z]['P0.5']*1E3
    D[z]['timescale'] = (D[z]['P0.8']-D[z]['P0.2'])*1E3

properties = ['age','timescale']


s = pickle.load(open('s.p','rb'))

x = 'log10Mstar_30'
y = 'timescale'

limits = fa.limits
limits[x][0] = s_limit[x]

fig, axes = fa.linear_redshift(D, fl.zeds, x, y, s[x], limits = limits, scatter_colour_quantity = 'log10FUV', scatter_cmap = cm.inferno)




fig.savefig(f'figs/timescale.pdf')
fig.savefig(f'figs/timescale.png')
