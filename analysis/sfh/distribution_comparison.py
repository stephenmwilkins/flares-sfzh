
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







limits[x][0] = s_limit[x]
limits['D'] = [0, 0.2]

labels['halfnorm'] = 'half\ normal'
labels['truncnorm'] = 'truncated\ normal'
labels['trunclognorm'] = 'truncated\ log-normal'

data_sf = h5py.File('data/sf.h5','r')

zeds = [8,9,10]
ylims = [0., 0.2]

dist_names = ['halfnorm','truncnorm', 'trunclognorm']

s = {}
data = {}

for z in zeds:

    data[z] = a.get_datasets(a.tag_from_zed[z], quantities)

    s[z] = data[z][x]>8.5

    for dist_name in dist_names:

        data[z][dist_name] =  data_sf[str(z)][dist_name]['D'][:]


        # D = data[z]['D'][s[z]]
        # s_ = (~np.isnan(D))&(D!=0.0)
        # print(z, np.sum(s_),np.mean(D[s_]),np.median(D[s_]))


fig, axes = flares_utility.plt.linear_redshift_comparison(data, zeds, x, dist_names, s, limits = limits, ylabel = 'D', bins = 10, ylims = ylims)

fig.savefig(f'figs/distribution_comparison.pdf')
