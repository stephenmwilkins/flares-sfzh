
import numpy as np

import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import scipy.stats as stats


import flares
import flares_analysis as fa
import flare.plt as fplt

# ----------------------------------------------------------------------
# --- open data

fl = flares.flares('/cosma7/data/dp004/dc-payy1/my_files/flares_pipeline/data/flares.hdf5', sim_type='FLARES')
# fl.explore()

# s = D['log10Mstar_30']>9
# print(len(s[s]))
# print(len(D['Age'][s]))
# print(np.sum(D['Mstar_30'][s])/1E10)
# print(np.sum(np.concatenate(D['Mass'][s])))



i = 3
tag = fl.tags[i]
z = fl.zeds[i]
print(z)



D = fa.get_particle_datasets(fl, tag)

s = D['log10Mstar_30']>8.5


Ages = D['Age'][s]



for ages in Ages:
    lam = 1/np.mean(ages)
    skew = stats.skew(ages)
    print(ages.shape, lam, skew)



# Age = np.concatenate(D['Age'][s])
# MassInitial = np.concatenate(D['MassInitial'][s])
# Weight = np.concatenate(D['pweight'][s])
