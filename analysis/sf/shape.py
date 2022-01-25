
import numpy as np
import matplotlib.cm as cm

from load import * # loads flares_analysis as a and defined mass/luminosity limits and tags/zeds



# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []

# quantities.append({'path': 'Galaxy', 'dataset': 'Mstar_30', 'name': None, 'log10': True})
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})

for t in [10,50,200]:
    quantities.append({'path': f'Galaxy/SFR_aperture/30', 'dataset': f'{t}Myr', 'name': f'SFR_{t}', 'log10': True})

quantities.append({'path': f'Galaxy/BPASS_2.2.1/Chabrier300/Luminosity/DustModelI', 'dataset': 'FUV', 'name': None, 'log10': True})





properties = ['log10SFR10/50','log10SFR50/200']
x_ = ['log10Mstar_30', 'log10FUV']

D = {}
s = {}
s['log10Mstar_30'] = {}
s['log10FUV'] = {}
for tag, z in zip(tags, zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    print(D[z]['Mstar_30'].shape, D[z]['SFR_50'].shape, D[z]['FUV'].shape)


    # D[z]['log10SFRinst/10'] = D[z]['log10SFR_inst_30'] - D[z]['log10SFR_10']
    D[z]['log10SFR10/50'] = D[z]['log10SFR_10'] - D[z]['log10SFR_50']
    D[z]['log10SFR50/200'] = D[z]['log10SFR_50'] - D[z]['log10SFR_200']

    for x in x_:
        s[x][z] = D[z][x]>s_limit[x]





# ---- make plot

x = 'log10Mstar_30'

limits = flares_utility.limits.limits
limits[x][0] = s_limit[x]

fig, axes = flares_utility.plt.linear_redshift_mcol(D, zeds, x, properties, s[x], limits = limits, scatter_colour_quantity = 'log10FUV', scatter_cmap = cm.inferno, add_linear_fit = False, height = 2)

for ax in axes.flatten():
    ax.axhline(0.0, color='k',lw=2, alpha=0.1)


fig.savefig(f'figs/shape.pdf')
fig.savefig(f'figs/shape.png')
