
import numpy as np

import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd


import flares
import flares_analysis as fa
import flare
import flare.plt as fplt


def n_weighted_moment(values, weights, n):

    assert n>0 & (values.shape == weights.shape)
    w_avg = np.average(values, weights = weights)
    w_var = np.sum(weights * (values - w_avg)**2)/np.sum(weights)

    if n==1:
        return w_avg
    elif n==2:
        return w_var
    else:
        w_std = np.sqrt(w_var)
        return np.sum(weights * ((values - w_avg)/w_std)**n)/np.sum(weights)
              #Same as np.average(((values - w_avg)/w_std)**n, weights=weights)



# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
# fl.explore()

# s = D['log10Mstar_30']>9
# print(len(s[s]))
# print(len(D['Age'][s]))
# print(np.sum(D['Mstar_30'][s])/1E10)
# print(np.sum(np.concatenate(D['Mass'][s])))

norm = mpl.colors.Normalize(vmin=8, vmax=11)
cmap = cm.viridis



N = len(fl.zeds)

left = 0.1
top = 0.95
bottom = 0.1
right = 0.9

panel_width = (right-left)/(N/2)
panel_height = top-bottom

fig, axes = plt.subplots(2, 3, figsize = (7,2*7/(panel_height/panel_width)), sharey = True, sharex = True)
plt.subplots_adjust(left=left, top=top, bottom=bottom, right=right, wspace=0.0, hspace=0.1)

axes = axes.flatten()

for ax, tag, z in zip(axes, fl.tags, fl.zeds):
# for ax, tag, z in zip(axes, fl.tags[:1], fl.zeds):

    cosmo = flare.default_cosmo()

    ax.fill_between([cosmo.age(z).to('Gyr').value,1.5],[0.0, 0.0],[1.0,1.0],color='k',alpha=0.05)

    print('-'*20)
    print(z)
    D = fa.get_particle_datasets(fl, tag)

    for log10Mstar_limit, ls in zip([8.5, 9.5, 10.5], ['-','--',':']):

        c = cmap(norm(log10Mstar_limit))

        s = (D['log10Mstar_30']>log10Mstar_limit-0.5)&(D['log10Mstar_30']<log10Mstar_limit+0.5)

        Age = np.concatenate(D['Age'][s])*1000
        MassInitial = np.concatenate(D['MassInitial'][s])
        Weight = np.concatenate(D['pweight'][s])

        sfr, bin_edges = np.histogram(np.log10(Age), weights = MassInitial*Weight, bins = np.arange(0,3, 0.1))

        bin_centres = bin_edges[:-1]+0.5*(bin_edges[1:]-bin_edges[:-1])

        N = len(D['log10Mstar_30'][s])
        mean = n_weighted_moment(Age, MassInitial*Weight, 1)
        skew = n_weighted_moment(Age, MassInitial*Weight, 3)

        print(log10Mstar_limit, N, skew)

        # ax.axvline(mean, lw=1.5, alpha =0.2, color=c)




        # sfr /= np.sum(sfr)

        ax.plot(bin_centres, np.log10(sfr), ls = ls, lw = 1.5,  c = c, label = rf'$\rm \log_{{10}}M^{{\star}}={log10Mstar_limit-0.5:.1f}-{log10Mstar_limit+0.5:.1f}$')


    ax.text(0.5, 1.02, rf'$\rm z={z}$', horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes, fontsize = 7)


axes[0].legend(fontsize=7)
axes[0].set_ylabel(rf'$\rm normalised\ SFR$', fontsize = 9)
axes[3].set_ylabel(rf'$\rm normalised\ SFR$', fontsize = 9)
axes[0].set_xlim([0., 1.1])
axes[0].set_ylim([0., 0.15])

fig.text(left+(right-left)/2, 0.04, rf'$\rm age/Gyr$', ha='center', fontsize = 9)


fig.savefig('figs/log10sfh.pdf')
