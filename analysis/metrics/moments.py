
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

quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_10', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_200', 'name': None, 'log10': True})

quantities.append({'path': 'Galaxy/StellarAges', 'dataset': 'MassWeightedStellarAge', 'name': 'age', 'log10': True})


quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})


properties = ['log10lambda', 'nvariance','skew','nkurtosis']
x_ = ['log10Mstar_30', 'log10FUV']




D = pickle.load(open('moments.p','rb'))
s = pickle.load(open('s.p','rb'))

for z in fl.zeds:
    D[z]['lambda'] = 1/D[z]['moment1']
    D[z]['log10lambda'] = np.log10(D[z]['lambda'])
    D[z]['nvariance'] = D[z]['moment2']*D[z]['lambda']**2
    D[z]['skew'] = D[z]['moment3']
    D[z]['nkurtosis'] = D[z]['moment4']-3



x = 'log10Mstar_30'

limits = fa.limits
limits[x][0] = s_limit[x]

fig, axes = fa.linear_redshift_mcol(D, fl.zeds, x, properties, s[x], limits = limits, scatter_colour_quantity = 'log10FUV', scatter_cmap = cm.inferno, add_linear_fit = False)

print(axes.shape)


# normalised variance, should be 1 for exp
for ax in axes[1,:]:
    ax.axhline(1.0, lw=1, c='k',alpha=0.2)

# skew, should be 2 for exp
for ax in axes[2,:]:
    ax.axhline(2.0, lw=1, c='k',alpha=0.2)

# kurtosis, should be 6 for exp
for ax in axes[3,:]:
    ax.axhline(6.0, lw=1, c='k',alpha=0.2)


fig.savefig(f'figs/moments.pdf')
# fig.savefig(f'figs/combined_redshift_{x}.png')
