
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




# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})

# quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_10', 'name': None, 'log10': True})
# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_100', 'name': None, 'log10': True})
# quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_200', 'name': None, 'log10': True})

quantities.append({'path': 'Galaxy/StellarAges', 'dataset': 'MassWeightedStellarAge', 'name': 'age', 'log10': True})
quantities.append({'path': 'Galaxy/Metallicity', 'dataset': 'MassWeightedStellarZ', 'name': 'Z', 'log10': True})

quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})



Dz = {}

for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    Dz[z] = fa.get_datasets(fl, tag, quantities)

    Dz[z]['log10sSFR'] = Dz[z]['log10SFR_100'] - Dz[z]['log10Mstar_30'] + 9





norm = mpl.colors.Normalize(vmin=8, vmax=11)
cmap = cm.viridis


limits = {}
limits['log10sSFR'] = [0.26, 1.14]
limits['log10age'] = [1.71, 2.69]
limits['log10Z'] = [-3.2, -1.51]





left = 0.15
top = 0.95
bottom = 0.1
right = 0.95

fig, axes = plt.subplots(2, 1, figsize = (3.5, 5), sharex = True)
plt.subplots_adjust(left=left, top=top, bottom=bottom, right=right, wspace=0.0, hspace=0.0)


for q, ax in zip(['log10sSFR', 'log10age'], axes):

    O = {}
    O['z'] = fl.zeds

    log10Mstar_limits = [8.5, 9.5, 10.5]

    for log10Mstar_limit in log10Mstar_limits:

        O[log10Mstar_limit] = {}

        for p in [2.5, 16, 50, 84, 97.5]:
            O[log10Mstar_limit][p] = []

    for tag, z in zip(fl.tags, fl.zeds):

        D = Dz[z]

        for log10Mstar_limit in log10Mstar_limits:

            s = (D['log10Mstar_30']>log10Mstar_limit-0.5)&(D['log10Mstar_30']<log10Mstar_limit+0.5)
            # s = D['log10Mstar_30']>log10Mstar_limit

            for p in [2.5, 16, 50, 84, 97.5]:
                O[log10Mstar_limit][p].append(np.percentile(D[q][s], p))





    for log10Mstar_limit, ls in zip(log10Mstar_limits, ['-','--','-.',':']):

        c = cmap(norm(log10Mstar_limit))

        # ax.fill_between(fl.zeds, O[log10Mstar_limit][2.5], O[log10Mstar_limit][97.5], alpha= 0.05, color = c)
        ax.fill_between(fl.zeds, O[log10Mstar_limit][16], O[log10Mstar_limit][84], alpha= 0.05, color = c)

        ax.plot(fl.zeds, O[log10Mstar_limit][50], ls = ls, c=c, lw=1, label = r'$\rm '+str(log10Mstar_limit-0.5)+'<log_{10}(M_{\star}/M_{\odot})<'+str(log10Mstar_limit+0.5)+'$')

    ax.set_ylabel(rf'$\rm {fa.labels[q]}$', fontsize = 9)
    ax.set_ylim(limits[q])
    ax.set_xlim([5,10])



axes[0].legend(fontsize = 7, labelspacing = 0.1)
axes[-1].set_xlabel(rf'$\rm z$', fontsize = 9)

fig.savefig(f'figs/mz_summary.pdf')
