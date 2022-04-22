
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds

from flares_utility.stats import weighted_median
from flares_utility.stats import weighted_quantile

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'50Myr', 'name': f'SFR_50', 'log10': True})





fig, ax = fplt.simple()


colors = flares_utility.colors.redshift


from astropy.cosmology import Planck18 as cosmo


f = {'age_of_Universe': [],'0': [], '-1': [], 'median': [], 'P2.2': []}

labels = {}
labels['age_of_Universe'] = r'$\rm sSFR<t_{\rm uni}^{-1}$'
labels['0'] = r'$\rm sSFR<1\ Gyr^{-1}$'
labels['-1'] = r'$\rm sSFR<-1\ Gyr^{-1}$'
labels['median'] = r'$\rm sSFR<0.1\times <sSFR>$'
labels['P2.2'] = r'$\rm sSFR<P_{2.2} $'

for tag, z in zip(tags, zeds):

    age_of_universe = cosmo.age(z)
    print(z, -np.log10(age_of_universe.value))

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    log10sSFR = D['log10SFR_50'] - D['log10Mstar_30'] + 9 # + 10

    s = D['log10Mstar_30']>10.

    w = D['weight']



    q = log10sSFR<-np.log10(age_of_universe.value)
    f['age_of_Universe'].append(np.sum(w[s&q])/np.sum(w[s]))

    q = log10sSFR<0.0
    f['0'].append(np.sum(w[s&q])/np.sum(w[s]))

    q = log10sSFR<-1
    f['-1'].append(np.sum(w[s&q])/np.sum(w[s]))

    med = weighted_median(log10sSFR[s], w[s])
    print(med)
    med = weighted_quantile(log10sSFR[s], [0.5], sample_weight = w[s])
    print(med)
    q = log10sSFR<med-1.0
    f['median'].append(np.sum(w[s&q])/np.sum(w[s]))


    twosigma = weighted_quantile(log10sSFR[s], [0.022], sample_weight = w[s])
    q = log10sSFR<twosigma
    f['P2.2'].append(np.sum(w[s&q])/np.sum(w[s]))

    # s_quiescent = log10sSFR<0.0
    # s_quiescent = log10sSFR<med-1.0


for t, ls in zip(['age_of_Universe','0','median'],['-','--','-.',':']):

    ax.plot(zeds, f[t], ls=ls, c='0.5', label = labels[t])


ax.legend(fontsize=8)


ax.set_xlim([10,5])

ax.set_xlabel(r'$\rm z$', fontsize = 9)
ax.set_ylabel(r'$\rm f_{\rm quiescent}(M_{\star}>10^{10}\ M_{\odot})$', fontsize = 9)


fig.savefig(f'figs/quiescent.pdf')
# fig.savefig(f'figs/combined_redshift_{x}.png')
