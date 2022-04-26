

import sys

# import matplotlib as mpl
# import matplotlib.cm as cm
# mpl.use('Agg')
# import matplotlib.pyplot as plt

import numpy as np
import pickle

from scipy.optimize import curve_fit
from util import truncnorm, halfnorm


binw = 10
bins = np.arange(0.0, 1500., binw)
binc = 0.5*(bins[:-1]+bins[1:])

# f = halfnorm()
# # f = truncnorm(max_age = 1500)

import flares_utility.analyse
import flares_utility.stats



filename = flares_utility.analyse.flares_master_file
a = flares_utility.analyse.analyse_flares(filename, default_tags = False)



x = 'log10Mstar_30'

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

iz = int(sys.argv[1])



ff = {'halfnorm': halfnorm(), 'truncnorm': truncnorm(max_age = 1500)}


tag = a.tags[iz]
z = a.zeds[iz]


# --- get quantities (and weights and deltas)
D = a.get_datasets(tag, quantities)

pD = a.get_particle_datasets(tag)

n = len(D['log10Mstar_30'])

O = {}
for dist in ['halfnorm','truncnorm']:
    O[dist] = {'KS': np.empty(n), 'p':np.empty((n,ff[dist].nparams))}



for i, (ages, massinitial) in enumerate(zip(pD['S_Age'], pD['S_MassInitial'])):

    if len(ages)>100:

        N_obs, _ = np.histogram(ages, bins = bins, weights = massinitial, density = True)
        cdf_obs = np.cumsum(N_obs[::-1])*binw

        # --- fit

        for dist in ['halfnorm','truncnorm']:

            params, _  = curve_fit(ff[dist].pdf, binc, N_obs, p0 = ff[dist].p0)
            N_fit = ff[dist].pdf(binc, *params)
            cdf_fit = 1-ff[dist].cdf(bins[:-1], *params)

            KS = np.max(np.fabs(cdf_obs-cdf_fit[::-1])) # -- measure the KS

            O[dist]['KS'][i] = KS
            O[dist]['p'][i] = params


            # plt.plot(binc, N_fit, ls='-',lw=3,alpha=0.4)
            # plt.plot(binc, N_obs, lw=1)
            # plt.savefig(f'{i}_pdf.pdf')
            # plt.clf()
            #
            # plt.plot(bins[:-1], cdf_fit, ls='-',lw=3,alpha=0.4)
            # plt.plot(bins[:-1][::-1], cdf_obs, lw=1)
            # plt.savefig(f'{i}_cdf.pdf')
            # plt.clf()



pickle.dump(O, open(f'distribution_parameters/{z}.p','wb'))
