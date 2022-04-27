
import numpy as np
import matplotlib.cm as cm

import cmasher as cmr

import scipy.stats as stats

from scipy.stats import lognorm
from scipy.optimize import curve_fit

import flare.plt as fplt
import pickle
import load


dist = getattr(stats, 'exponpow')

D = pickle.load(open('data/stacked_Z.p','rb'))



z = 5.

fig, ax = fplt.simple()

t = 'log10'
d = D[z][t]

binw = 0.1
bins = np.arange(-5.,-0.0,binw)
binc = 0.5*(bins[:-1]+bins[1:])

colors = cmr.take_cmap_colors('cmr.ember', len(d.keys()), cmap_range=(0.1, 1.0)) #




for (log10Mstar, N), c in zip(d.items(), colors):

    hist_dist = stats.rv_histogram((N, bins))
    data = hist_dist.rvs(size=100000)
    params = dist.fit(data)

    # label = rf'$\rm {log10Mstar-0.25:.1f}<\log_{{10}}(M_{{\star}}/M_{{\odot}})<{log10Mstar+0.25:.1f}$'
    label = rf'$\rm [{log10Mstar-0.25:.1f}, {log10Mstar+0.25:.1f})$'
    y = N/np.sum(N)/binw

    ax.plot(binc, dist(*params).pdf(binc), c=c, ls='-', lw=3, alpha=0.2)

    ax.plot(binc, y, label = label, c=c, lw=1)



ax.set_xlabel(r'$\rm \log_{10}(Z)$')
ax.set_ylabel(r'$\rm N$')
ax.set_xlim([-5, -1.])
ax.set_ylim([0, 0.99])

ax.legend(fontsize = 8, title = rf'$\rm z={z:.0f} $'+'\n'+rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
fig.savefig('figs/stacked_Z.pdf')
