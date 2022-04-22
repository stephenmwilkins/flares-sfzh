
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





bins = np.linspace(*flares_utility.limits.limits['log10Mstar_30'], 12)
bincen = (bins[:-1]+bins[1:])/2.


fig, ax = fplt.simple()

norm = mpl.colors.Normalize(vmin=5, vmax=10)


for tag, z in zip(tags, zeds):

    c = cm.plasma(norm(z))

    # --- get quantities (and weights and deltas)
    D = a.get_datasets(tag, quantities)

    print(np.median(D['log10SFR_50']))

    log10sSFR = D['log10SFR_50'] - D['log10Mstar_30'] + 9 # + 10


    print(np.min(log10sSFR),np.median(log10sSFR),np.max(log10sSFR))


    s = D['log10Mstar_30']>s_limit['log10Mstar_30']
    s_quiescent = log10sSFR<0.0

    # all, bin_edges = np.histogram(D['log10Mstar_30'][s], bins=bins, weights=D['weight'][s])
    # quiescent, bin_edges  = np.histogram(D['log10Mstar_30'][s&s_quiescent], bins=bins, weights=D['weight'][s&s_quiescent])

    all, bin_edges = np.histogram(D['log10Mstar_30'][s], bins=bins)
    quiescent, bin_edges  = np.histogram(D['log10Mstar_30'][s&s_quiescent], bins=bins)


    f = quiescent/all

    ax.plot(bincen, f, c=c, label = rf'$\rm z={z}$')

ax.legend(fontsize=8)


ax.set_xlim(flares_utility.limits.limits['log10Mstar_30'])

ax.set_xlabel(rf'$\rm {flares_utility.labels.labels["log10Mstar_30"]}$', fontsize = 9)
ax.set_ylabel(rf'$\rm N(sSFR/Gyr^{{-1}}<1)/N$', fontsize = 9)


fig.savefig(f'figs/quiescent.pdf')
# fig.savefig(f'figs/combined_redshift_{x}.png')
