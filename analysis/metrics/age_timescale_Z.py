
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

itag = 1# z=9
tag = fl.tags[itag]
z = fl.zeds[itag]
print(tag, z)




quantities = []

quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Metallicity', 'dataset': 'MassWeightedStellarZ', 'name': 'Z', 'log10': True})

# --- get quantities (and weights and deltas)
D = fa.get_datasets(fl, tag, quantities)

Dp = pickle.load(open('percentiles.p','rb'))

D['age'] = Dp[z]['P0.5']*1E3
D['timescale'] = (Dp[z]['P0.8']-Dp[z]['P0.2'])*1E3


s = np.fabs(D['log10Mstar_30']-9)<0.5

print(len(D['age'][s]), len(D['Z'][s]))


x = 'log10Z'
z = 'timescale'
y = 'age'

fig, ax, cax = fa.simple_wcbar(D, x, y, z, s = s)

fig.savefig(f'figs/age_timescale_Z.pdf')
