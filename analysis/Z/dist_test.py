

from scipy.stats import norm
from scipy.stats import kstest

N = 10000
r = norm.rvs(size=N)
print(kstest(r, 'norm'))


from scipy.stats import moment

for n in range(1,5):
    print(n, moment(r, moment=n))

# r = np.log10(r[r>0.0])
#
# print('-'*10)
#
# for n in range(1,5):
#     print(n, moment(r, moment=n))


from scipy.stats import ks_2samp

r2 = norm.rvs(size=N)
print(ks_2samp(r, r2))
