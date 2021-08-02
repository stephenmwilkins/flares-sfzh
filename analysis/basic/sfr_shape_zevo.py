



import numpy as np
import matplotlib.cm as cm

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
tag = fl.tags[3]  # --- tag 0 = 10
log10Mstar_limit = 8.5


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_10', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_200', 'name': None, 'log10': True})




D = {}
s = {}

for tag, z in zip(fl.tags, fl.zeds):


    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['R'] =  D[z]['log10SFR_50'] - D[z]['log10SFR_200']

    # ----------------------------------------------
    # define selection
    s[z] = D[z]['log10Mstar_30']>log10Mstar_limit

    # ----------------------------------------------
    # Print number of galaxies meeting the selection
    print(f"Total number of galaxies: {len(D[z]['log10Mstar_30'][s[z]])}")


    # ----------------------------------------------
    # ----------------------------------------------
    # plot with colour bar

    # --- get default limits and modify them to match the selection range
    limits = fa.limits
    limits['log10Mstar_30'] = [log10Mstar_limit, 10.9]
    limits['R'] = [-0.5,0.5]


    # --- get default limits and modify them to match the selection range
    labels = fa.labels
    labels['R'] = r'log_{10}(SFR_{50}/SFR_{200})'



fig, ax = fa.simple_zevo(D, 'log10Mstar_30', 'R', s)


ax.axhline(0.0,c='k', alpha=0.1)

fig.savefig(f'figs/sfr_shape_zevo.pdf')
