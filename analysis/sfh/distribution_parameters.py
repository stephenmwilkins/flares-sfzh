
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle
import h5py

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

x = 'log10Mstar_30'





limits = flares_utility.limits.limits

limits[x][0] = s_limit[x]
limits['D'] = [0, 0.2]



data_sf = h5py.File('data/sf.h5','r')
# D2.visit(print)

zeds = [8,9,10]

for dist_name in ['halfnorm','truncnorm', 'trunclognorm']:

    s = {}
    data = {}

    print(dist_name, '-'*20)

    for z in zeds:

        data[z] = a.get_datasets(a.tag_from_zed[z], quantities)

        data[z]['D'] =  data_sf[str(z)][dist_name]['D'][:]

        nparam = data_sf[str(z)][dist_name]['p'].shape[1]

        for i in range(nparam):

            data[z][f'p{i+1}'] =  data_sf[str(z)][dist_name]['p'][:,i]




        s[z] = data[z][x]>8.5
        D = data[z]['D'][s[z]]
        s_ = (~np.isnan(D))&(D!=0.0)

        print(z, np.sum(s_),np.mean(D[s_]),np.median(D[s_]))


    properties = ['D'] + [f'p{i+1}' for i in range(nparam)]

    fig, axes = flares_utility.plt.linear_redshift_mcol(data, zeds, x, properties, s, limits = limits, scatter = False, add_weighted_range = True)

    fig.savefig(f'figs/distribution_parameters_{dist_name}.pdf')
