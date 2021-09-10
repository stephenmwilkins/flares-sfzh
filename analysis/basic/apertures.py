import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import cmasher as cmr

cmap = cmr.rainforest

import flares
import flares_analysis
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5', sim_type='FLARES')
# fl.explore()

halo = fl.halos

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = fl.tags[-1]  # --- tag 0 = 10




apertures = [1, 3, 5, 10, 30, 50, 100]

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy', 'dataset': 'Mstar', 'name': None, 'log10': True}) # total
quantities.append({'path': 'Galaxy', 'dataset': 'SFR', 'name': 'SFR_100', 'log10': True}) # total

for r in apertures:
    quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_{r}', 'name': None, 'log10': True})
    quantities.append({'path': f'Galaxy/SFR_aperture/SFR_{r}', 'dataset': 'SFR_100_Myr', 'name': f'SFR_100_{r}', 'log10': True})



# --- get quantities (and weights and deltas)
D = flares_analysis.get_datasets(fl, tag, quantities)


D['log10sSFR_100'] = D['log10SFR_100'] - D['log10Mstar'] + 9. # total

for r in apertures:
    D[f'log10sSFR_100_{r}'] = D[f'log10SFR_100_{r}'] - D[f'log10Mstar_{r}'] + 9. #aperture based


print(np.min(D['log10SFR_100']), np.max(D['log10SFR_100']))
print(np.min(D['log10Mstar']), np.max(D['log10Mstar']))

limits = {}
limits['log10Mstar'] = [8.05,12]
limits['log10SFR_100'] = [-1.,3.]

labels = {}
labelss = {} # short label
labels['log10Mstar'] = r'log_{10}(M_{\star}/M_{\odot})'
labelss['log10Mstar'] = 'M_{\star}'
labels['log10SFR_100'] = r'log_{10}(SFR_{100}/M_{\odot}\ yr^{-1})'
labelss['log10SFR_100'] = 'SFR_{100}'
labels['log10sSFR_100'] = r'log_{10}(sSFR_{100}/Gyr^{-1})'
labelss['log10sSFR_100'] = 'sSFR_{100}'


#
# # --- individual plots
#
# x = 'log10Mstar'
#
# for y in ['log10Mstar', 'log10SFR_100', 'log10sSFR_100']:
#
#     N = len(apertures)
#
#     left = 0.2
#     top = 0.95
#     bottom = 0.05
#     right = 0.9
#     panel_width = (right-left)/N
#     panel_height = top-bottom
#     fig, axes = plt.subplots(N, 1, figsize = (3,2*N), sharex = True)
#     plt.subplots_adjust(left=left, top=top, bottom=bottom, right=right, wspace=0.0, hspace=0.01)
#
#     for ax, r in zip(axes, apertures):
#
#         ax.axhline(0.0, color='k', lw=2, alpha=0.2)
#
#         yy = f'{y}_{r}'
#
#         # --- weighted median Lines
#
#         print(np.min(D[yy]), np.max(D[yy]))
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
#         ax.set_ylim([-0.5,0.5])
#
#         ax.set_ylabel(rf'$\rm log_{{10}}({labelss[y]}^{{ {r} }}/{labelss[y]}^{{tot}})$', fontsize = 9)
#
#     axes[-1].set_xlabel(rf'$\rm {labels[x]}$', fontsize = 9)
#
#     fig.savefig(f'figs/apertures_{y}.pdf')
#



# --- individual plots

x = 'log10Mstar'

for y in ['log10Mstar', 'log10SFR_100', 'log10sSFR_100']:

    fig, ax = fplt.simple_sm(size=2.5)

    ax.axhline(0.0, color='k', lw=2, alpha=0.2)

    for i,r in enumerate(apertures):

        c = cmap(i/len(apertures))

        yy = f'{y}_{r}'

        # --- weighted median Lines
        R = D[yy]-D[y]



        bins = np.linspace(*limits[x], 20)
        bincen = (bins[:-1]+bins[1:])/2.
        out = flares.binned_weighted_quantile(D[x], R, D['weight'],bins,[0.84,0.50,0.16])

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
    ax.set_ylim([-0.5,0.5])

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
