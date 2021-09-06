
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt

import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')

# fl.explore()

halo = fl.halos

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = fl.tags[-3]  # --- select tag -3 = z=7


limit = 8.5

limits = fa.limits
limits['log10Mstar_30'][0] = limit

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})

# quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_10', 'name': None, 'log10': True})
# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_100', 'name': None, 'log10': True})
# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_200', 'name': None, 'log10': True})




bins = np.linspace(*fa.limits['log10Mstar_30'], 12)
bincen = (bins[:-1]+bins[1:])/2.


fig, ax = fplt.simple()

norm = mpl.colors.Normalize(vmin=5, vmax=10)


for tag, z in zip(fl.tags, fl.zeds):

    c = cm.plasma(norm(z))

    # --- get quantities (and weights and deltas)
    D = fa.get_datasets(fl, tag, quantities)

    log10sSFR = D['log10SFR_100'] - D['log10Mstar_30'] + 9

    s = D['log10Mstar_30']>limit
    s_quiescent = log10sSFR<0.0

    # all, bin_edges = np.histogram(D['log10Mstar_30'][s], bins=bins, weights=D['weight'][s])
    # quiescent, bin_edges  = np.histogram(D['log10Mstar_30'][s&s_quiescent], bins=bins, weights=D['weight'][s&s_quiescent])

    all, bin_edges = np.histogram(D['log10Mstar_30'][s], bins=bins)
    quiescent, bin_edges  = np.histogram(D['log10Mstar_30'][s&s_quiescent], bins=bins)


    f = quiescent/all

    ax.plot(bincen, f, c=c, label = rf'$\rm z={z}$')

ax.legend(fontsize=8)


ax.set_xlim(limits['log10Mstar_30'])

ax.set_xlabel(rf'$\rm {fa.labels["log10Mstar_30"]}$', fontsize = 9)
ax.set_ylabel(rf'$\rm N(sSFR/Gyr^{{-1}}<1)/N$', fontsize = 9)


fig.savefig(f'figs/quiescent.pdf')
# fig.savefig(f'figs/combined_redshift_{x}.png')
