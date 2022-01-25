
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle


from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})

properties = ['log10lambda', 'nvariance','skew','nkurtosis']
x_ = ['log10Mstar_30', 'log10FUV']


D = pickle.load(open('moments_and_percentiles.p','rb'))

s = {x : {} for x in x_ }
for z in zeds:
    D[z]['lambda'] = 1/(D[z]['moment1'])
    D[z]['log10lambda'] = np.log10(D[z]['lambda'])
    D[z]['nvariance'] = D[z]['moment2']*D[z]['lambda']**2
    D[z]['skew'] = D[z]['moment3']
    D[z]['nkurtosis'] = D[z]['moment4']-3

    for x in x_:
        s[x][z] = D[z][f'{x}_s']


x = 'log10Mstar_30'

limits = flares_utility.limits.limits

limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s[x], limits = limits, scatter_colour_quantity = 'log10FUV', scatter_cmap = cm.inferno, add_linear_fit = False)


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
fig.savefig(f'figs/moments.png')
# fig.savefig(f'figs/combined_redshift_{x}.png')
