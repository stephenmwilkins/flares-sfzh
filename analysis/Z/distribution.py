
import numpy as np
import matplotlib.cm as cm

import scipy.stats as stats

import pickle
import load

# ----------------------------------------------------------------------
# --- define quantities to read in [not those for the corner plot, that's done later]




D = pickle.load(open('distributions.p','rb'))

print(D.keys())
