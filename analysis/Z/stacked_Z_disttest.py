

# ----
# -- find a distribution to fit



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





D = pickle.load(open('data/stacked_Z.p','rb'))

z = 5.


fig, ax = fplt.simple()

t = 'log10'
d = D[z][t]

log10Mstar = 9.75
# log10Mstar = 8.75
N = d[log10Mstar]



binw = 0.1
# bins = -np.arange(-5.,-0.0,binw)[::-1]
bins = np.arange(-5.,-0.0,binw)
binc = 0.5*(bins[:-1]+bins[1:])

c = 'k'

y = N/np.sum(N)/binw

# --- sample the histogram
hist_dist = stats.rv_histogram((N, bins))
data = hist_dist.rvs(size=1000)


try_all = True
plot_one = False

if try_all:

    list_of_dists = ['alpha','anglit','arcsine','beta','betaprime','bradford','burr','burr12','cauchy','chi','chi2','cosine','dgamma','dweibull','erlang','expon','exponnorm','exponweib','exponpow','f','fatiguelife','fisk','foldcauchy','foldnorm','frechet_r','frechet_l','genlogistic','genpareto','gennorm','genexpon','genextreme','gausshyper','gamma','gengamma','genhalflogistic','gilbrat','gompertz','gumbel_r','gumbel_l','halfcauchy','halflogistic','halfnorm','halfgennorm','hypsecant','invgamma','invgauss','invweibull','johnsonsb','johnsonsu','kstwobign','laplace','levy','levy_l','logistic','loggamma','loglaplace','lognorm','lomax','maxwell','mielke','nakagami','ncx2','ncf','nct','norm','pareto','pearson3','powerlaw','powerlognorm','powernorm','rdist','reciprocal','rayleigh','rice','recipinvgauss','semicircular','t','triang','truncexpon','truncnorm','tukeylambda','uniform','vonmises','vonmises_line','wald','weibull_min','weibull_max']


    results = []
    for i in list_of_dists:
        dist = getattr(stats, i)

        try:
            param = dist.fit(data)
            a = stats.kstest(data, i, args=param)
            results.append((i,a[0],a[1],len(param)))
        except:
            print(i, 'failed')

    results.sort(key=lambda x:float(x[2]), reverse=True)

    print('-'*50)
    print('-'*50)
    for j in results[:20]:
        print(f"{j[0]:}: statistic={j[1]:.3f} nparam={j[3]}")


if plot_one:

    dist_name = 'exponpow'
    dist_name = 'loggamma'
    dist_name = 'beta'
    dist_name = 'gumbel_l'

    dist = getattr(stats, dist_name)
    params = dist.fit(data)
    print('parameters:', params)


    ax.plot(binc, dist(*params).pdf(binc), c=c, ls='-',lw=3,alpha=0.4, label ='fit')
    ax.plot(binc, y, label = 'original', c=c, lw=1)
    ax.plot(binc, hist_dist.pdf(binc), label = 'hist_dist.pdf', c='r', lw=2, alpha=0.5, ls=':')

    # N, _ = np.histogram(data, bins=bins, density = True)
    # ax.plot(binc, N)

    ax.set_xlabel(r'$\rm \log_{10}(Z)$')
    ax.set_ylabel(r'$\rm N$')
    ax.set_xlim([-5, -1.])
    ax.set_ylim([0, 0.99])

    fig.savefig('figs/stacked_Z_disttest.pdf')
