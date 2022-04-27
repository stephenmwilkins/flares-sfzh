
import numpy as np
import scipy.stats as stats

import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
import cmasher as cmr


import flare.plt as fplt
import pickle





D = pickle.load(open('data/stacked_sfzh.p','rb'))

z = 5.

fig, ax = fplt.simple()

log10Mstar = 10.75

N = D[z][log10Mstar]

print(N.shape)
print(N)

ax.imshow(N, origin = 'lower', cmap = cmr.ocean)


# ax.set_xlabel(r'$\rm \log_{10}(Z)$')
# ax.set_ylabel(r'$\rm N$')
# ax.set_xlim([-5, -1.])
# ax.set_ylim([0, 0.99])


fig.savefig('figs/stacked_sfzh.pdf')
