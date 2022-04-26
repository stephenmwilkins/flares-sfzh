

from scipy.stats import halfnorm as halfnorm_
from scipy.stats import truncnorm as truncnorm_






class halfnorm():

    p0 = (200)
    nparams = 1

    def func(self, scale):
        return halfnorm_(scale = scale)

    def pdf(self, x, scale):
        return self.func(scale).pdf(x)

    def cdf(self, x, scale):
        return self.func(scale).cdf(x)




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
