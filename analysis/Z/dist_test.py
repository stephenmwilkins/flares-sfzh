
import numpy as np
from scipy.stats import norm
from scipy.stats import moment

from scipy.stats import kstest, ks_2samp

N = 100000
r = norm.rvs(size=N)
print(kstest(r, 'norm'))


for n in range(1,5):
    print(n, moment(r, moment=n))

# r = np.log10(r[r>0.0])
#
# print('-'*10)
#
# for n in range(1,5):
#     print(n, moment(r, moment=n))




r2 = norm.rvs(size=N)
print(ks_2samp(r, r2))
