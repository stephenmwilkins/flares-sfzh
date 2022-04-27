
import h5py
import numpy as np


m = h5py.File('sf.h5','w')


for z in np.arange(8.,15,1.):
    print(z)
    for dist_name in ['halfnorm','truncnorm','trunclognorm']:
        print(dist_name)
        d = h5py.File(f'temp_{z}_{dist_name}.h5','r')

        m.copy(d, f'{int(z)}/{dist_name}')


m.visit(print)

D = m['8']['halfnorm']['D'][:]
print(len(D))

s = (~np.isnan(D))&(D!=0.0)

print(np.sum(s))

print(np.mean(D[s]))
print(np.median(D[s]))
