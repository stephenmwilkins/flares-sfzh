
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import pickle

import numpy as np

import flares_utility.analyse
import flares_utility.stats
import flares_utility.limits
import flares_utility.plt

import flare.plt as fplt

from load import *

r = '30'
t = '50'


# testing
# tags2 = ['000_z015p000','001_z014p000']
# zeds2 = np.array([float(tag[5:].replace('p','.')) for tag in tags2])



# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'{r}', 'name': 'Mstar_30', 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/{r}', 'dataset': f'{t}Myr', 'name': f'SFR_50', 'log10': True})

Dp = pickle.load(open('moments_and_percentiles.p','rb'))

Dz = {}




for tag, z in zip(tags2, zeds2):

    # --- get quantities (and weights and deltas)
    Dz[z] = a.get_datasets(tag, quantities)

    print(z, len(Dz[z]['log10SFR_50']), len(Dz[z]['log10Mstar_30']))

    Dz[z]['log10sSFR'] = Dz[z]['log10SFR_50'] - Dz[z]['log10Mstar_30'] + 9
    Dz[z]['age'] = Dp[z]['P0.5']#*1E3
    Dz[z]['log10age'] = np.log10(Dz[z]['age'])




norm = mpl.colors.Normalize(vmin=8, vmax=11)
cmap = cm.viridis


limits = {}
limits['log10sSFR'] = [0.26, 1.4]
limits['log10age'] = [1.1, 2.69]
# limits['log10Z'] = [-3.2, -1.51]





left = 0.15
top = 0.95
bottom = 0.1
right = 0.95

fig, axes = plt.subplots(2, 1, figsize = (3.5, 5), sharex = True)
plt.subplots_adjust(left=left, top=top, bottom=bottom, right=right, wspace=0.0, hspace=0.0)


for q, ax in zip(['log10sSFR', 'log10age'], axes):


    # ----

    if q=='log10sSFR':


        redshifts = np.arange(5, 15, 0.1)

        ages = flares_utility.analyse.cosmo.age(redshifts).to('Myr').value

        SFR = 5.
        Mstar = (ages-flares_utility.analyse.cosmo.age(20).to('Myr').value)*SFR*1E6 # technically wrong as no recycling
        log10sSFR = np.log10(SFR/Mstar)+9

        print(log10sSFR)

        ax.plot(redshifts, log10sSFR, c='k', alpha=0.2, ls='--', label = r'$\rm const\ SF\ since\ z=20$')







    print('-'*20, q)

    O = {}
    O['z'] = zeds

    log10Mstar_limits = [9.5, 10.5]

    for log10Mstar_limit in log10Mstar_limits:

        O[log10Mstar_limit] = {}

        for p in [2.5, 16, 50, 84, 97.5]:
            O[log10Mstar_limit][p] = []

    for tag, z in zip(tags2, zeds2):

        D = Dz[z]

        for log10Mstar_limit in log10Mstar_limits:

            s = (D['log10Mstar_30']>log10Mstar_limit-0.5)&(D['log10Mstar_30']<log10Mstar_limit+0.5)
            # s = D['log10Mstar_30']>log10Mstar_limit



            if sum(s)>0:
                for p in [2.5, 16, 50, 84, 97.5]:
                    O[log10Mstar_limit][p].append(np.percentile(D[q][s], p))
                print(z, log10Mstar_limit, sum(s), O[log10Mstar_limit][50][-1])

            else:
                for p in [2.5, 16, 50, 84, 97.5]:
                    O[log10Mstar_limit][p].append(np.nan)
                print(z, log10Mstar_limit, sum(s), '-')


    for log10Mstar_limit, ls in zip(log10Mstar_limits, ['-','--','-.',':']):

        c = cmap(norm(log10Mstar_limit))

        # ax.fill_between(fl.zeds, O[log10Mstar_limit][2.5], O[log10Mstar_limit][97.5], alpha= 0.05, color = c)
        ax.fill_between(zeds2, O[log10Mstar_limit][16], O[log10Mstar_limit][84], alpha= 0.05, color = c)

        ax.plot(zeds2, O[log10Mstar_limit][50], ls = ls, c=c, lw=1, label = r'$\rm '+str(log10Mstar_limit-0.5)+'<log_{10}(M_{\star}/M_{\odot})<'+str(log10Mstar_limit+0.5)+'$')

    ax.set_ylabel(rf'$\rm {flares_utility.labels.labels[q]}$', fontsize = 9)
    ax.set_ylim(limits[q])
    ax.set_xlim([5,15])



axes[0].legend(fontsize = 7, labelspacing = 0.1)
axes[-1].set_xlabel(rf'$\rm z$', fontsize = 9)

fig.savefig(f'figs/ssfr_age_summary.pdf')
fig.savefig(f'figs/ssfr_age_summary.png')
