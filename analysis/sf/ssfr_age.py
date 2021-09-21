
import numpy as np
import matplotlib.cm as cm

import pickle

import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

# fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
fl = flares.flares('/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5', sim_type='FLARES')


s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': f'Galaxy/SFR_aperture/SFR_30', 'dataset': f'SFR_50_Myr', 'name': f'SFR_50', 'log10': True})


quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})


Dp = pickle.load(open('percentiles.p','rb'))


x_ = ['log10Mstar_30', 'log10FUV']

D = {}
s = {}
s['log10Mstar_30'] = {}
s['log10FUV'] = {}
for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['log10sSFR'] = D[z]['log10SFR_50'] - D[z]['log10Mstar_30'] + 9

    D[z]['age'] = Dp[z]['P0.5']*1E3
    D[z]['log10age'] = np.log10(D[z]['age'])

    for x in x_:
        s[x][z] = D[z][x]>s_limit[x]



# --- get default limits and modify them to match the selection range

cmap = {'log10FUV': cm.viridis, 'log10Mstar_30': cm.inferno}


# for y in ['log10age', 'log10sSFR', 'log10Z']:
for y in ['log10age','age','log10sSFR']:

    print(y)


    for x, z in zip(x_, x_[::-1]): #the colour map is for the other parameter

        limits = fa.limits
        limits[x][0] = s_limit[x]

        fig, ax = fa.linear_redshift(D, fl.zeds, x, y, s[x], limits = limits, scatter_colour_quantity = z, scatter_cmap = cmap[x], rows=2)

        fig.savefig(f'figs/{y}_{x}.pdf')
        fig.savefig(f'figs/{y}_{x}.png')
        # fig.savefig(f'figs/combined_redshift_{x}.png')
