
import numpy as np
import matplotlib.cm as cm

import cmasher as cmr

from scipy.optimize import curve_fit

import flare.plt as fplt
import pickle

from load import *

from util import truncnorm, halfnorm








# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]




D = pickle.load(open('distributions.p','rb'))




binw = 10
bins = np.arange(0.0, 1500., binw)
binc = 0.5*(bins[:-1]+bins[1:])

colors = cmr.take_cmap_colors('cmr.ember', len(D[5]['linear'].keys()), cmap_range=(0.1, 1.0)) #

# --- single redshift

z = 5.

fig, ax = fplt.simple()

cfig, cax = fplt.simple()

d = D[z]['linear']


f = truncnorm(max_age = 1500)
# f = halfnorm()


for (log10Mstar, N), c in zip(d.items(), colors):

    label = rf'$\rm [{log10Mstar-0.25:.1f}, {log10Mstar+0.25:.1f})$'

    y = N/np.sum(N)/binw
    obs_cdf = np.cumsum(y[::-1])*10.

    x = bins[:-1][::-1]

    params, _  = curve_fit(f.pdf, binc, y, p0 = f.p0)
    y_fit = f.pdf(binc, *params)
    fit_cdf = 1-f.cdf(x[::-1], *params)

    ax.plot(binc, y_fit, c=c, ls='-',lw=3,alpha=0.4)
    ax.plot(binc, y, label = label, c=c, lw=1)

    KS = np.max(np.fabs(obs_cdf-fit_cdf[::-1]))

    cax.plot(x[::-1], fit_cdf, c=c, ls='-',lw=3,alpha=0.4)
    cax.plot(x, obs_cdf, c=c, lw=1)

    print(log10Mstar, *params, KS)




ax.set_xlabel(r'$\rm age/Myr$')
ax.set_ylabel(r'$\rm N$')
ax.set_xlim([0, 1000])
ax.set_ylim([0, 0.0039])

ax.legend(fontsize = 8, title = rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
fig.savefig('figs/age_distribution.pdf')
fig.clf()


cax.set_xlabel(r'$\rm age/Myr$')
cax.set_ylabel(r'$\rm C$')
cax.set_xlim([0, 1000])
cax.set_ylim([0, 1.2])

cax.legend(fontsize = 8, title = rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
cfig.savefig('figs/age_cumulative.pdf')
cfig.clf()
