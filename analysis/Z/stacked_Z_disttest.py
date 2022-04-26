

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
N = d[log10Mstar]



binw = 0.1
# bins = -np.arange(-5.,-0.0,binw)[::-1]
bins = np.arange(-5.,-0.0,binw)
binc = 0.5*(bins[:-1]+bins[1:])


c = 'k'

# label = rf'$\rm {log10Mstar-0.25:.1f}<\log_{{10}}(M_{{\star}}/M_{{\odot}})<{log10Mstar+0.25:.1f}$'
label = rf'$\rm [{log10Mstar-0.25:.1f}, {log10Mstar+0.25:.1f})$'
y = N/np.sum(N)/binw


print(bins)
print(N)

# --- sample the histogram
hist_dist = stats.rv_histogram((N, bins))
data = hist_dist.rvs(size=100000)

print(data)



list_of_dists = ['alpha','anglit','arcsine','beta','betaprime','bradford','burr','burr12','cauchy','chi','chi2','cosine','dgamma','dweibull','erlang','expon','exponnorm','exponweib','exponpow','f','fatiguelife','fisk','foldcauchy','foldnorm','frechet_r','frechet_l','genlogistic','genpareto','gennorm','genexpon','genextreme','gausshyper','gamma','gengamma','genhalflogistic','gilbrat','gompertz','gumbel_r','gumbel_l','halfcauchy','halflogistic','halfnorm','halfgennorm','hypsecant','invgamma','invgauss','invweibull','johnsonsb','johnsonsu','kstwobign','laplace','levy','levy_l','logistic','loggamma','loglaplace','lognorm','lomax','maxwell','mielke','nakagami','ncx2','ncf','nct','norm','pareto','pearson3','powerlaw','powerlognorm','powernorm','rdist','reciprocal','rayleigh','rice','recipinvgauss','semicircular','t','triang','truncexpon','truncnorm','tukeylambda','uniform','vonmises','vonmises_line','wald','weibull_min','weibull_max']


# results = []
# for i in list_of_dists:
#     dist = getattr(stats, i)
#
#     try:
#         param = dist.fit(data)
#         a = stats.kstest(data, i, args=param)
#         results.append((i,a[0],a[1]))
#         print(i, a[0])
#     except:
#         print(i, 'failed')
#
# results.sort(key=lambda x:float(x[2]), reverse=True)
# for j in results:
#     print("{}: statistic={}, pvalue={}".format(j[0], j[1], j[2]))
#

dist = getattr(stats, 'norm') # BAD
# dist = getattr(stats, 'lognorm') # BAD
dist = getattr(stats, 'exponpow')
# dist = getattr(stats, 'loggamma')
# dist = getattr(stats, 'johnsonsb')
# dist = getattr(stats, 'beta')
params = dist.fit(data)
print(params)

# def lnorm(x, mu, sigma):
#     return lognorm(s = sigma, scale = np.exp(mu)).pdf(x)

# (mu_fit, sigma_fit), _  = curve_fit(lnorm, binc, y, p0 = (1, 0.3))
#



# print(log10Mstar, mu_fit, sigma_fit)

# ax.plot(binc, lognorm(s = sigma_fit, scale = np.exp(mu_fit)).pdf(binc), c=c, ls='-',lw=3,alpha=0.4, label ='fit')

ax.plot(binc, dist(*params).pdf(binc), c=c, ls='-',lw=3,alpha=0.4, label ='fit')

ax.plot(binc, y, label = 'original', c=c, lw=1)

ax.plot(binc, hist_dist.pdf(binc), label = 'hist_dist.pdf', c='r', lw=2, alpha=0.5, ls=':')

N, _ = np.histogram(data, bins=bins, density = True)

ax.plot(binc, N)

ax.set_xlabel(r'$\rm \log_{10}(Z)$')
ax.set_ylabel(r'$\rm N$')
ax.set_xlim([-5, -1.])
# ax.set_xlim([1, 5.])
ax.set_ylim([0, 0.99])

ax.legend(fontsize = 8, title = rf'$\rm \log_{{10}}(M_{{\star}}/M_{{\odot}})\in $')
fig.savefig('figs/stacked_Z_disttest.pdf')
