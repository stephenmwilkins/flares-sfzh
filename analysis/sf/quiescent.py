
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'50Myr', 'name': f'SFR_50', 'log10': True})





bins = np.arange(*[8.5, 12], 0.25)
bincen = (bins[:-1]+bins[1:])/2.


fig, ax = fplt.simple()


colors = flares_utility.colors.redshift


from astropy.cosmology import Planck18 as cosmo



for tag, z, c in zip(tags, zeds, colors):

    age_of_universe = cosmo.age(z)
    print(z, -np.log10(age_of_universe.value))

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    log10sSFR = D['log10SFR_50'] - D['log10Mstar_30'] + 9 # + 10

    s = D['log10Mstar_30']>s_limit['log10Mstar_30']

    med = np.median(log10sSFR[s])

    s_quiescent = log10sSFR<-np.log10(age_of_universe.value)
    # s_quiescent = log10sSFR<0.0
    # s_quiescent = log10sSFR<med-1.0


    # all, bin_edges = np.histogram(D['log10Mstar_30'][s], bins=bins, weights=D['weight'][s])
    # quiescent, bin_edges  = np.histogram(D['log10Mstar_30'][s&s_quiescent], bins=bins, weights=D['weight'][s&s_quiescent])

    weights = D['weight']
    # weights = np.ones(len(weights))

    all, bin_edges = np.histogram(D['log10Mstar_30'][s], bins=bins, weights = weights[s])
    quiescent, bin_edges  = np.histogram(D['log10Mstar_30'][s&s_quiescent], bins=bins, weights = weights[s&s_quiescent])


    f = quiescent/all

    ax.plot(bincen, f, c=c, label = rf'$\rm z={z:.0f}$')

ax.legend(fontsize=8)


ax.set_xlim(flares_utility.limits.limits['log10Mstar_30'])

ax.set_xlabel(rf'$\rm {flares_utility.labels.labels["log10Mstar_30"]}$', fontsize = 9)
ax.set_ylabel(rf'$\rm N(sSFR/Gyr^{{-1}}<1)/N$', fontsize = 9)


fig.savefig(f'figs/quiescent.pdf')
# fig.savefig(f'figs/combined_redshift_{x}.png')
