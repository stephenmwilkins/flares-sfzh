
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

properties = ['slope', 'intercept', 'rvalue', 'pvalue']


D = pickle.load(open('stats.p','rb'))

t = 'B'


s = {}
for z in zeds:

    print(D[z]['linregress'][t])

    D[z]['slope'] = D[z]['linregress'][t][:, 0]
    D[z]['intercept'] = D[z]['linregress'][t][:, 1]
    D[z]['rvalue'] = D[z]['linregress'][t][:, 2]
    D[z]['pvalue'] = D[z]['linregress'][t][:, 3]


    s[z] = D[z]['s']


# labels['rlog10a'] = 'PCC'
# limits['rlog10a'] = [-0.74,0.1]
#
# labels['range'] = 'P_{84.2}-P_{15.8}'
# limits['range'] = [0.51,2.49]

limits[x][0] = s_limit[x]



fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True)

# for ax in axes[0,:]:
#     ax.axhline(0.0, c='k',lw=3, alpha=0.1)


fig.savefig(f'figs/linregress.pdf')
