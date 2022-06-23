
import numpy as np
import pickle

import flares_utility.analyse
import flares_utility.stats

from scipy.stats import pearsonr

filename = '/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5'

a = flares_utility.analyse.analyse_flares(filename, default_tags = False)

# a.list_datasets()


x = 'log10Mstar_30'


quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar_30', 'log10': True})


D = {}
outputs = {}

for tag, z in zip(a.tags, a.zeds):

    # --- get quantities (and weights and deltas)
    D[z] = a.get_datasets(tag, quantities)

    # print(z, len(D[z]['log10Mstar_30']), len(D[z]['log10Mstar_30'][D[z]['log10Mstar_30']>8.0]))

    # --- get particle datasets and measure properties
    P = a.get_particle_datasets(tag, quantities = ['S_Mass', 'S_Abundance_Oxygen', 'S_Abundance_Iron', 'S_Abundance_Hydrogen'])

    # --- define the outputs

    outputs[z] = {}
    outputs[z]['H'] = np.zeros(len(D[z]['log10Mstar_30']))
    outputs[z]['Fe'] = np.zeros(len(D[z]['log10Mstar_30']))
    outputs[z]['O'] = np.zeros(len(D[z]['log10Mstar_30']))


    for i, (H, O, Fe, mass) in enumerate(zip(P['S_Abundance_Hydrogen'], P['S_Abundance_Oxygen'], P['S_Abundance_Iron'], P['S_Mass'])):

        if len(mass)>1:
            outputs[z]['H'][i] = np.sum(mass*H)/np.sum(mass)
            outputs[z]['O'][i] = np.sum(mass*O)/np.sum(mass)
            outputs[z]['Fe'][i] = np.sum(mass*Fe)/np.sum(mass)

pickle.dump(outputs, open('data/HOFe.p','wb'))
