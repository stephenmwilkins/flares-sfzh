

import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pickle

from scipy.optimize import curve_fit
from util import truncnorm, halfnorm


binw = 10
bins = np.arange(0.0, 1500., binw)
binc = 0.5*(bins[:-1]+bins[1:])

if func == 'truncnorm':
    f = truncnorm(max_age = 1500)

if func == 'halfnorm':
    f = halfnorm()


import flares_utility.analyse
import flares_utility.stats



filename = flares_utility.analyse.flares_master_file
a = flares_utility.analyse.analyse_flares(filename, default_tags = False)



x = 'log10Mstar_30'

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

iz = 5

O = {}

a.tags = [a.tags[iz]]


for tag, z in zip(a.tags, a.zeds):

    print(z, '-'*20)
    O[z] = {}

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    pD = a.get_particle_datasets(tag)


    for i, (ages, massinitial) in enumerate(zip(pD['S_Age'], pD['S_MassInitial'])):

        if len(ages)>1000:

            N_obs, _ = np.histogram(ages, bins = bins, weights = massinitial, density = True)
            cdf_obs = np.cumsum(y[::-1])

            # --- fit
            params, _  = curve_fit(f.pdf, binc, N_obs, p0 = f.p0)
            N_fit = f.pdf(binc, *params)
            cdf_fit = 1-f.cdf(bins[:-1], *params)

            KS = np.max(np.fabs(obs_cdf-fit_cdf[::-1])) # -- measure the KS

            print(*params, KS)

            plt.plot(binc, y_fit, c=c, ls='-',lw=3,alpha=0.4)
            plt.plot(binc, y, label = label, c=c, lw=1)
            plt.show()

            plt.plot(bins[:-1], fit_cdf, c=c, ls='-',lw=3,alpha=0.4)
            plt.plot(bins[:-1][::-1], obs_cdf, c=c, lw=1)
            plt.show()



# pickle.dump(O, open('distributions.p','wb'))
