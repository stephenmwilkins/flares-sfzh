import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


from flares_utility import analyse
from flares_utility import stats as flares_stats

import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data and load analyser


fname = analyse.flares_master_file

# fname = '../../../../simulations/flares/flares_noparticlesed.hdf5'


a = analyse.analyse_flares(fname, default_tags = False)




# ----------------------------------------------------------------------
# --- list datasets (specifically for the 1st sim/tag)
a.list_datasets()

# ----------------------------------------------------------------------
# --- define parameters and tag
tag = a.tags[-1]  # --- tag 0 = z=10
z = a.zed_from_tag[tag] # get redshift of that tag
print(tag, z, a.tag_from_zed[z]) # print, but also shows how to the tag from zed

# --- define SFR averaging timescale
t = '50'

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]

quantities = []
quantities.append({'path': 'Galaxy', 'dataset': 'Mstar', 'name': 'Mstar_total', 'log10': True}) # total? 30?

for aperture in [1,30,100]:
    quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'{aperture}', 'name': f'Mstar_{aperture}', 'log10': True})




# --- get quantities (and weights and deltas)
D = a.get_datasets(tag, quantities)


for aperture in [1,30,100]:
    P = a.get_particle_datasets(tag, quantities = ['S_Mass'], aperture = aperture)
    D[f'log10Mstar_{aperture}_particle'] = np.log10(np.array([np.sum(P['S_Mass'][i]) for i in np.arange(len(D['log10Mstar_total']))]))

P = a.get_particle_datasets(tag, quantities = ['S_Mass'], aperture = False)
D['log10Mstar_total_particle'] = np.log10(np.array([np.sum(P['S_Mass'][i]) for i in np.arange(len(D['log10Mstar_total']))]))


from prettytable import PrettyTable

for suf in ['','_particle']:

    my_table = PrettyTable()
    my_table.field_names = ["", "min", "median", "max"]

    for x in ['log10Mstar_total','log10Mstar_1','log10Mstar_30','log10Mstar_100']: #
        my_table.add_row([x+suf, f'{np.min(D[x+suf]):.2f}', f'{np.median(D[x+suf]):.2f}', f'{np.max(D[x+suf]):.2f}'])

    print(my_table)

#
# for r in a.apertures:
#     print(np.min(D[f'log10Mstar_{r}']), np.max(D[f'log10Mstar_{r}']))
