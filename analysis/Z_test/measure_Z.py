
import numpy as np
import pickle

import flares_utility.analyse
import flares_utility.stats

from scipy.stats import pearsonr

filename = '/cosma7/data/dp004/dc-love2/codes/flares/data/flares.hdf5'

a = flares_utility.analyse.analyse_flares(filename, default_tags = False)

a.list_datasets()


x = 'log10Mstar_30'


quantities = []
quantities.append({'path': 'Galaxy/Mstar_aperture', 'dataset': f'30', 'name': 'Mstar', 'log10': True})
quantities.append({'path': 'Galaxy/Metallicity', 'dataset': f'MassWeightedStellarZ', 'name': None, 'log10': True})


tag = a.tags[-2]

# --- get quantities (and weights and deltas)
D = a.get_datasets(tag, quantities)


s = D['log10Mstar']>10.
print('the number of galaxies with M*>1E10:', np.sum(s))


# print(z, len(D[z]['log10Mstar_30']), len(D[z]['log10Mstar_30'][D[z]['log10Mstar_30']>8.0]))

# --- get particle datasets and measure properties
P = a.get_particle_datasets(tag, quantities = ['S_Age', 'S_Mass', 'S_MassInitial', 'S_Z', 'S_Z_smooth', 'S_Abundance_Oxygen', 'S_Abundance_Iron', 'S_Abundance_Hydrogen'])

FeH = []
Z_Fe = []
Z_O = []
Ztot = []

for i in np.arange(len(s))[s]:

    age = P['S_Age'][i]
    Z = P['S_Z'][i]
    massinitial = P['S_MassInitial'][i]
    mass = P['S_Mass'][i]
    Z_smooth = P['S_Z_smooth'][i]

    print('-'*10)
    print(f"{D['log10Mstar'][i]:.2f} {np.log10(np.sum(mass)):.2f}")

    Zp = np.sum(mass*Z)/np.sum(mass)
    Ztot.append(np.log10(Zp))
    print(f"mass weighted {D['log10MassWeightedStellarZ'][i]:.2f} {np.log10(Zp):.2f}")
    Zp = np.sum(massinitial*Z)/np.sum(massinitial)
    print(f"initial mass weighted {D['log10MassWeightedStellarZ'][i]:.2f} {np.log10(Zp):.2f}")
    Zp = np.sum(mass*Z_smooth)/np.sum(mass)
    print(f"smooth {D['log10MassWeightedStellarZ'][i]:.2f} {np.log10(Zp):.2f}")

    Zp = np.sum(mass*P['S_Abundance_Iron'][i])/np.sum(mass)
    Z_Fe.append(np.log10(Zp))
    print(f"iron {np.log10(Zp):.2f}")

    Zp = np.sum(mass*P['S_Abundance_Oxygen'][i])/np.sum(mass)
    Z_O.append(np.log10(Zp))
    print(f"iron {np.log10(Zp):.2f}")

    Zp = np.sum(mass*P['S_Abundance_Iron'][i]/56)/np.sum(mass*P['S_Abundance_Hydrogen'][i])
    print(f"Fe/H {np.log10(Zp):.2f}")

    FeH.append(np.log10(Zp))

    # Z_m = D['log10MassWeightedStellarZ'][i]
    #
    # Z_p1 = np.log10(flares_utility.stats.weighted_median(Z, massinitial))
    #
    # print(f'{Z_m:.2f} {Z_p1:.2f}')

print('-'*30)
print('(Fe/H):', np.median(FeH))
print('Z_Fe:', np.median(Z_Fe))
print('Z_O:', np.median(Z_O))
print('Z:',np.median(Ztot))
