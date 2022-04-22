
import numpy as np
import matplotlib.cm as cm

import cmasher as cmr

import scipy.stats as stats

import flare.plt as fplt
import pickle
import load


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]




D = pickle.load(open('distributions.p','rb'))

print(D.keys())

z = 5.

fig, ax = fplt.simple()

t = 'log10'

bins = {}
bins['linear'] = np.arange(0.0, 0.1, 0.001)
bins['log10'] = np.arange(-5.,-0.0,0.1)

d = D[z][t]

colors = cmr.take_cmap_colors('cmr.ember', len(d.keys()), cmap_range=(0.1, 1.0)) #

for (log10Mstar, N), c in zip(d.items(), colors):

    # label = rf'$\rm {log10Mstar-0.25:.1f}<\log_{{10}}(M_{{\star}}/M_{{\odot}})<{log10Mstar+0.25:.1f}$'
    label = rf'$\rm [{log10Mstar-0.25:.1f}, {log10Mstar+0.25:.1f})$'
    N = N/np.sum(N)
    ax.plot(bins[t][:-1], N, label = label, c=c)


ax.set_xlabel(r'$\rm \log_{10}(Z)$')
ax.set_ylabel(r'$\rm N$')
ax.set_xlim([-5, -1.])
ax.set_ylim([0, 0.099])

ax.legend(fontsize = 8, title = rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
fig.savefig('figs/distribution.pdf')
