
import numpy as np
from scipy.stats import norm, truncnorm, lognorm
from scipy.stats import moment
from scipy.stats import kstest, ks_2samp
from scipy.optimize import curve_fit

from util import trunclognorm

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)



# def tnorm(x, loc, scale):
#     return truncnorm(a = -loc/scale, b = 10, scale = scale, loc = loc).pdf(x)
#
# x_ = np.linspace(0, 10, 100)
#
# # --- input
#
# loc = -2
# scale = 2
# dist = truncnorm(a = -loc/scale, b = 10, scale = scale, loc = loc)
#
# ax.plot(x_, truncnorm(a = -loc/scale, b = 10, loc=loc, scale=scale).pdf(x_))
#
# # x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), 100)
# # y = dist.pdf(x)
#
# bin_edges = np.arange(0,10,1)
# x = 0.5*(bin_edges[:-1]+bin_edges[1:])
# r = dist.rvs(100)
#
# y, _ = np.histogram(r, bins = bin_edges, density = True)
#
# ax.plot(x, y)
#
# (loc_fit, scale_fit), _  = curve_fit(tnorm, x, y)
#
# print(loc_fit, loc, loc - loc_fit)
# print(scale_fit, scale, scale - scale_fit)
#
# ax.plot(x_, truncnorm(a = -loc_fit/scale_fit, b = 10, loc=loc_fit, scale=scale_fit).pdf(x_))
#
# plt.show()




x = np.linspace(0.01, 1000, 100)

# --- input

max_age = 1000
mu = 1
sigma = 1

dist = lognorm(s = sigma, scale = np.exp(mu))

pdf = dist.pdf((max_age-x)/max_age)

ax.plot(x, pdf/np.sum(pdf[~np.isnan(pdf)]))

dist = trunclognorm(max_age = max_age)

pdf = dist.pdf(x, mu, sigma)


ax.plot(x, pdf)




# x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), 100)
# y = dist.pdf(x)

# bin_edges = np.arange(0,10,1)
# x = 0.5*(bin_edges[:-1]+bin_edges[1:])
# r = dist.rvs(100)
#
# y, _ = np.histogram(r, bins = bin_edges, density = True)
#
# ax.plot(x, y)
#
# (loc_fit, scale_fit), _  = curve_fit(tnorm, x, y)
#
# print(loc_fit, loc, loc - loc_fit)
# print(scale_fit, scale, scale - scale_fit)
#
# ax.plot(x_, truncnorm(a = -loc_fit/scale_fit, b = 10, loc=loc_fit, scale=scale_fit).pdf(x_))

plt.show()
