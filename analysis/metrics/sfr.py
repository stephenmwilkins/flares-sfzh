
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
tag = fl.tags[-3]  # --- select tag -3 = z=7


s_limit = {'log10Mstar_30': 8.5, 'log10FUV': 28.5}

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})

quantities.append({'path': 'Galaxy', 'dataset': 'SFR_inst_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_10', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_50', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/SFR', 'dataset': 'SFR_200', 'name': None, 'log10': True})



quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})


properties = ['log10SFRinst/10', 'log10SFR10/50','log10SFR50/200']
x_ = ['log10Mstar_30', 'log10FUV']

D = {}
s = {}
s['log10Mstar_30'] = {}
s['log10FUV'] = {}
for tag, z in zip(fl.tags, fl.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = fa.get_datasets(fl, tag, quantities)

    D[z]['log10SFRinst/10'] = D[z]['log10SFR_inst_30'] - D[z]['log10SFR_10']
    D[z]['log10SFR10/50'] = D[z]['log10SFR_10'] - D[z]['log10SFR_50']
    D[z]['log10SFR50/200'] = D[z]['log10SFR_50'] - D[z]['log10SFR_200']

    for x in x_:
        s[x][z] = D[z][x]>s_limit[x]



# --- get default limits and modify them to match the selection range

cmap = {'log10FUV': cm.viridis, 'log10Mstar_30': cm.inferno}




for x, z in zip(x_, x_[::-1]): #the colour map is for the other parameter

    limits = fa.limits
    limits[x][0] = s_limit[x]

    fig = fa.linear_redshift_mcol(D, fl.zeds, x, properties, s[x], limits = limits, scatter_colour_quantity = z, scatter_cmap = cmap[x], add_linear_fit = False)

    fig.savefig(f'figs/sfr_{x}.pdf')
    # fig.savefig(f'figs/combined_redshift_{x}.png')
