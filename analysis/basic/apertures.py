import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import cmasher as cmr

cmap = cmr.rainforest

from flares_utility import analyse
from flares_utility import stats as flares_stats

import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data and load analyser

a = analyse.analyse_flares(analyse.flares_master_file, default_tags = False)

# ----------------------------------------------------------------------
# --- list datasets (specifically for the 1st sim/tag)
# a.list_datasets()

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = a.tags[-1]  # --- tag 0 = (z = 15)
z = a.zed_from_tag[tag] # get redshift of that tag
print(tag, z, a.tag_from_zed[z]) # print, but also shows how to the tag from zed

# --- define SFR averaging timescale
t = '50'

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy', 'dataset': 'Mstar', 'name': 'Mstar_total', 'log10': True}) # total? 30?
quantities.append({'path': 'Galaxy/SFR', 'dataset': f'{t}Myr', 'name': 'SFR_total', 'log10': True}) # total

for r in a.apertures:
    quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'{r}', 'name': f'Mstar_{r}', 'log10': True})
    quantities.append({'path': f'Galaxy/SFR_aperture/{r}', 'dataset': f'{t}Myr', 'name': f'SFR_{r}', 'log10': True})



# --- get quantities (and weights and deltas)
D = a.get_datasets(tag, quantities)

D['log10Mstar'] = D['log10Mstar_30']
D['log10SFR'] =  D['log10SFR_30']



# --- calculate sSFRs

D['log10sSFR'] = D['log10SFR'] - D['log10Mstar'] + 9. #default
D['log10sSFR_total'] = D['log10SFR_total'] - D['log10Mstar_total'] + 9. # total

for r in a.apertures:
    D[f'log10sSFR_{r}'] = D[f'log10SFR_{r}'] - D[f'log10Mstar_{r}'] + 9. #aperture based


for r in a.apertures:
    print(np.min(D[f'log10Mstar_{r}']), np.max(D[f'log10Mstar_{r}']))

limits = {}
limits['log10Mstar'] = [8.05,12]
limits['log10SFR_100'] = [-1.,3.]

labels = {}
labelss = {} # short label
labels['log10Mstar'] = r'log_{10}(M_{\star}/M_{\odot})'
labelss['log10Mstar'] = 'M_{\star}'
labels['log10SFR'] = r'log_{10}(SFR_{50}/M_{\odot}\ yr^{-1})'
labelss['log10SFR'] = 'SFR_{100}'
labels['log10sSFR'] = r'log_{10}(sSFR_{50}/Gyr^{-1})'
labelss['log10sSFR'] = 'sSFR_{50}'




# --- individual plots

x = 'log10Mstar'

for y in ['log10Mstar', 'log10SFR', 'log10sSFR']:

    fig, ax = fplt.simple_sm(size=2.5)

    ax.axhline(0.0, color='k', lw=2, alpha=0.2)

    for i,r in enumerate(a.apertures):

        c = cmap(i/len(a.apertures))

        yy = f'{y}_{r}'

        # --- weighted median Lines
        R = D[yy]-D[y+'_total']



        bins = np.linspace(*limits[x], 20)
        bincen = (bins[:-1]+bins[1:])/2.
        out = flares_stats.binned_weighted_quantile(D[x], R, D['weight'],bins,[0.84,0.50,0.16])

        N, bin_edges = np.histogram(D[x], bins=bins)

        i = np.array(range(len(N)))

        ss = i[N<1]
        if len(ss)>0:
            sN = i[i<ss[0]]
        else:
            sN = i

        ax.plot(bincen[sN], out[:,1][sN], ls = '--', color = c)

        ss = i[N<10]
        if len(ss)>0:
            sN = i[i<ss[0]]
        else:
            sN = i

        ax.plot(bincen[sN], out[:,1][sN], ls = '-', color = c, label = rf'$\rm {r}\ kpc $',)



    ax.legend(fontsize = 7, labelspacing = 0.1)

    ax.set_xlim(limits[x])

    if y in ['log10Mstar', 'log10SFR']:
        ax.set_ylim([-0.99,0.1])
    if y in ['log10sSFR']:
        ax.set_ylim([-0.4,0.4])

    ax.set_xlabel(rf'$\rm {labels[x]}$', fontsize = 9)
    ax.set_ylabel(rf'$\rm log_{{10}}({labelss[y]}/{labelss[y]}^{{tot}})$', fontsize = 9)

    fig.savefig(f'figs/apertures_{y}.pdf')






# --- combined

# x = 'log10Mstar'
# ys = ['log10Mstar', 'log10SFR_100', 'log10sSFR_100']
#
# N = len(apertures)
#
# left = 0.2
# top = 0.95
# bottom = 0.05
# right = 0.95
# panel_width = (right-left)/N
# panel_height = top-bottom
# fig, axes = plt.subplots(N, len(ys), figsize = (3.5,N), sharex = True, sharey = True)
# plt.subplots_adjust(left=left, top=top, bottom=bottom, right=right, wspace=0.05, hspace=0.01)
#
# print(axes.shape)
#
# for ix, y in enumerate(ys):
#     for iy, r in enumerate(apertures):
#
#         ax = axes[iy,ix]
#
#         ax.axhline(0.0, color='k', lw=2, alpha=0.2)
#
#         yy = f'{y}_{r}'
#
#         # --- weighted median Lines
#
#         R = D[yy]-D[y]
#
#         bins = np.linspace(*limits[x], 20)
#         bincen = (bins[:-1]+bins[1:])/2.
#         out = flares.binned_weighted_quantile(D[x], R, D['weight'],bins,[0.84,0.50,0.16])
#
#         ax.plot(bincen, out[:,1], ls = '-')
#
#         ax.set_xlim(limits[x])
#         ax.set_ylim([-0.49,0.49])
#
#         if ix == 0:
#             ax.set_ylabel(rf'$\rm {r}\ kpc$', fontsize = 9)
#
#         if iy == 0:
#             ax.text(0.5, 1.02, rf'$\rm log_{{10}}({labelss[y]}/{labelss[y]}^{{tot}})$', fontsize = 7, horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
#
# axes[-1,1].set_xlabel(rf'$\rm {labels[x]}$', fontsize = 9)
#
# fig.savefig(f'figs/apertures.pdf')
