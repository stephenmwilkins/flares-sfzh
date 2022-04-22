

# Import CMasher to register colormaps
import cmasher as cmr

import numpy as np
import matplotlib.cm as cm

import pickle

from astropy.io import ascii



import flare.obs.literature.OIIIHb as OIIIHb_observations

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds


redshift = 7
x_limit = 28.5

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_30', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/SFR_30', 'dataset': f'SFR_50_Myr', 'name': f'SFR_50', 'log10': True})

quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Lines/DustModelI/HI4861', 'dataset': 'EW', 'name': 'HI4861_EW', 'log10': False})
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Lines/DustModelI/OIII5007', 'dataset': 'EW', 'name': 'OIII5007_EW', 'log10': False})
quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Lines/DustModelI/OIII4959', 'dataset': 'EW', 'name': 'OIII4959_EW', 'log10': False})



# --- get quantities (and weights and deltas)
D = a.get_datasets(a.tag_from_zed[redshift], quantities)

D['OIIIHbEW'] = D['HI4861_EW']+D['OIII5007_EW']+D['OIII4959_EW']
D['log10OIIIHbEW'] = np.log10(D['OIIIHbEW'])
D['log10sSFR'] = D['log10SFR_50'] - D['log10Mstar_30'] + 9

s = D['log10FUV']>x_limit



x = 'log10FUV'
y = 'OIIIHbEW'
z = 'log10sSFR'


print()

limits = flares_utility.limits.limits
limits[x][0] = x_limit
limits['log10sSFR'] = [np.min(D['log10sSFR'][s]), np.max(D['log10sSFR'][s])]

fig, ax, cax, hax = flares_utility.plt.simple_wcbar_whist(D, x, y, z, s, limits = limits, add_weighted_median = True)





# --- add observational comparisons

markers = ['o','d','s']

print(OIIIHb_observations.observed)

if redshift in OIIIHb_observations.observed.keys():

    print('yo')

    colors = cmr.take_cmap_colors('cmr.chroma', len(OIIIHb_observations.observed[redshift]), cmap_range=(0.15, 0.85))

    for obs, marker, c in zip(OIIIHb_observations.observed[redshift], markers, colors):

        if obs.dt == 'io':

            ax.scatter(obs.log10L1500, obs.OIIIHbEW, c='r', s=3, marker=marker, label = rf'$\rm {obs.label}$')


            hax.hist(obs.OIIIHbEW, bins=30, orientation='horizontal',color='r',density=True, alpha = 0.5)

ax.legend(fontsize=7, handletextpad = 0.0, loc = 'upper left')
ax.set_xticks(np.arange(29, 31, 1.0))






fig.savefig(f'figs/OIIIHb_observations.pdf')
