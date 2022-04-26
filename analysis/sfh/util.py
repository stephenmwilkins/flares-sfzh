
import numpy as np
from scipy.stats import halfnorm as halfnorm_
from scipy.stats import truncnorm as truncnorm_
from scipy.stats import lognorm as lognorm_
from scipy.stats import expon as expon_

class expon():

    p0 = (1/200)
    nparams = 1

    def func(self, lam):
        return expon_(scale = 1/lam)

    def pdf(self, x, lam):
        return self.func(lam).pdf(x)

    def cdf(self, x, lam):
        return self.func(lam).cdf(x)


class halfnorm():

    p0 = (200)
    nparams = 1

    def func(self, scale):
        return halfnorm_(scale = scale)

    def pdf(self, x, scale):
        return self.func(scale).pdf(x)

    def cdf(self, x, scale):
        return self.func(scale).cdf(x)


class trunclognorm():

    nparams = 2

    def __init__(self, max_age = 1000):
        self.max_age = max_age
        self.p0 = (1,1)

    def func(self, mu, sigma):
        return lognorm_(s = sigma, scale = np.exp(mu))


    def pdf(self, x, mu, sigma):
        pdf_ = self.func(mu, sigma).pdf((self.max_age-x)/self.max_age)
        return pdf_/((x[1]-x[0])*np.sum(pdf_))

    def cdf(self, x, mu, sigma):
        cdf_ = (x[1]-x[0])*np.cumsum(self.pdf(x, mu, sigma)[::-1])
        return (1-cdf_[::-1])




class trunclognorm_freemax():

    nparams = 3

    def __init__(self):
        self.p0 = (1,1, 1000)

    def func(self, mu, sigma):
        return lognorm_(s = sigma, scale = np.exp(mu))

    def pdf(self, x, mu, sigma, max_age):
        pdf_ = self.func(mu, sigma).pdf((max_age-x)/max_age)
        return pdf_/((x[1]-x[0])*np.sum(pdf_))

    def cdf(self, x, mu, sigma, max_age):
        cdf_ = np.cumsum(self.pdf(x, mu, sigma, max_age)[::-1])
        return (1-cdf_[::-1])

class truncnorm():

    p0 = (0, 100)
    nparams = 2

    def __init__(self, max_age = 1500):
        self.max_age = 1500.

    def b(self, loc, scale):
        return (self.max_age - loc)/scale

    def func(self, loc, scale):
        b = self.b(loc, scale)
        return truncnorm_(a = -loc/scale, b = b, scale = scale, loc = loc)

    def pdf(self, x, loc, scale):
        return self.func(loc, scale).pdf(x)

    def cdf(self, x, loc, scale):
        return self.func(loc, scale).cdf(x)


# def tnorm(x, loc, scale):
#     max_age = 1500.
#     b = (max_age - loc)/scale
#     return truncnorm(a = -loc/scale, b = b, scale = scale, loc = loc).pdf(x)
