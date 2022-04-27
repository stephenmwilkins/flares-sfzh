
import numpy as np
import matplotlib.cm as cm

import cmasher as cmr

import scipy.stats as stats

from scipy.stats import lognorm
from scipy.optimize import curve_fit

import flare.plt as fplt
import pickle
import load


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

def lnorm(x, mu, sigma):
    return lognorm(s = sigma, scale = np.exp(mu)).pdf(-x)



D = pickle.load(open('data/stacked_Z_age.p','rb'))

print(D.keys())

z = 5.

fig, ax = fplt.simple()

d = D[z]

binw = 0.1
bins = np.arange(-6.,-0.0,binw)
binc = 0.5*(bins[:-1]+bins[1:])

colors = cmr.take_cmap_colors('cmr.ember', len(d.keys()), cmap_range=(0.1, 1.0)) #

for log10Mstar, c in zip(d.keys(), colors):

    print(d.keys())

    for ia, (ls, (al, au)) in enumerate(zip(['-','--','-.',':'],[[0, 50],[50, 200],[200, 1000]])):

        N = d[log10Mstar][ia]

        # label = rf'$\rm {log10Mstar-0.25:.1f}<\log_{{10}}(M_{{\star}}/M_{{\odot}})<{log10Mstar+0.25:.1f}$'
        # label = rf'$\rm [{log10Mstar-0.25:.1f}, {log10Mstar+0.25:.1f})$'
        label = None
        y = N/np.sum(N)/binw

        ax.plot(binc, y, label = label, c=c, lw=1, ls=ls)


ax.set_xlabel(r'$\rm \log_{10}(Z)$')
ax.set_ylabel(r'$\rm N$')
ax.set_xlim([-5, -1.])
ax.set_ylim([0, 0.99])

ax.legend(fontsize = 8, title = rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
fig.savefig('figs/stacked_Z_age.pdf')
