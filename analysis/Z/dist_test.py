
import numpy as np
from scipy.stats import norm
from scipy.stats import moment

r = 10+norm.rvs(size=10000)


for n in range(1,5):
    print(n, moment(r, moment=n))

r = np.log10(r[r>0.0])

print('-'*10)

for n in range(1,5):
    print(n, moment(r, moment=n))
