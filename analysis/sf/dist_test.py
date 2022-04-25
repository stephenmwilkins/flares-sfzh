
import numpy as np
from scipy.stats import norm, truncnorm
from scipy.stats import moment
from scipy.stats import kstest, ks_2samp
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)



def tnorm(x, loc, scale):
    return truncnorm(a = -loc/scale, b = 10, scale = scale, loc = loc).pdf(x)

x_ = np.linspace(0, 10, 100)

# --- input

loc = -2
scale = 2
dist = truncnorm(a = -loc/scale, b = 10, scale = scale, loc = loc)

ax.plot(x_, truncnorm(a = -loc/scale, b = 10, loc=loc, scale=scale).pdf(x_))



# x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), 100)
# y = dist.pdf(x)

bin_edges = np.arange(0,10,1)
x = 0.5*(bin_edges[:-1]+bin_edges[1:])
r = dist.rvs(100)

y, _ = np.histogram(r, bins = bin_edges, density = True)

ax.plot(x, y)




(loc_fit, scale_fit), _  = curve_fit(tnorm, x, y)

print(loc_fit, loc, loc - loc_fit)
print(scale_fit, scale, scale - scale_fit)

ax.plot(x_, truncnorm(a = -loc_fit/scale_fit, b = 10, loc=loc_fit, scale=scale_fit).pdf(x_))

plt.show()


# N = 10000
# r = norm.rvs(size=N)
# print(kstest(r, 'norm'))
