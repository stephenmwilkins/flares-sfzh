
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt

import cmasher as cmr

from scipy.optimize import curve_fit

import flare.plt as fplt
import pickle

from load import *

from util import expon, truncnorm, halfnorm, trunclognorm, trunclognorm_freemax



# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]


D = pickle.load(open('data/stacked_sfh.p','rb'))




binw = 10
bins = np.arange(0.0, 1500., binw)
binc = 0.5*(bins[:-1]+bins[1:])

colors = cmr.take_cmap_colors('cmr.ember', len(D[5]['linear'].keys()), cmap_range=(0.1, 1.0)) #

# --- single redshift

z = 5.



d = D[z]['linear']




dists = {'expon': expon(), 'halfnorm': halfnorm(), 'truncnorm': truncnorm(max_age = 1500), 'trunclognorm': trunclognorm(max_age = 1500)}
# dists['trunclognorm'] = trunclognorm_freemax()

# dist_names = ['halfnorm', 'truncnorm']
# dist_names = ['expon']
dist_names = ['expon', 'halfnorm', 'truncnorm', 'trunclognorm']

for dist_name in dist_names:

    fig, ax = fplt.simple()
    cfig, cax = fplt.simple()


    dist = dists[dist_name]

    for (log10Mstar, N), c in zip(d.items(), colors):

        y = N/np.sum(N)/binw
        obs_cdf = np.cumsum(y[::-1])*10.

        x = bins[:-1][::-1]

        params, _  = curve_fit(dist.pdf, binc, y, p0 = dist.p0, maxfev = 20000)
        y_fit = dist.pdf(binc, *params)
        fit_cdf = (1-dist.cdf(x[::-1], *params))


        KS = np.max(np.fabs(obs_cdf-fit_cdf[::-1]))

        label = rf'$\rm [{log10Mstar-0.25:.1f}, {log10Mstar+0.25:.1f})\ D={KS:.3f}$'

        ax.plot(binc, y_fit, c=c, ls='-',lw=3,alpha=0.4)
        ax.plot(binc, y, label = label, c=c, lw=1)



        cax.plot(x[::-1], fit_cdf, c=c, ls='-',lw=3,alpha=0.4)
        cax.plot(x, obs_cdf, c=c, lw=1)

        print(log10Mstar, *params, KS)



    ax.set_xlabel(r'$\rm age/Myr$')
    ax.set_ylabel(r'$\rm SFR$')
    ax.set_xlim([0, 1500])
    ax.set_ylim([0, 0.0039])

    ax.set_yticks(np.arange(0, 0.004, 0.001))

    ax.legend(fontsize = 7, title = rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
    fig.savefig(f'figs/stacked_sfh_{dist_name}.pdf')
    fig.clf()


    cax.set_xlabel(r'$\rm age/Myr$')
    cax.set_ylabel(r'$\rm C$')
    cax.set_xlim([0, 1500])
    cax.set_ylim([0, 1.2])

    cax.legend(fontsize = 8, title = rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
    cfig.savefig(f'figs/stacked_cumsfh_{dist_name}.pdf')
    cfig.clf()
