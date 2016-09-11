import glob
import numpy as np

#Test de chi2
def redchi2(y, m, s, dof=0):
    chi2 = np.sum(np.square((y - m)/s))
    nu   = len(data) - 1 - dof
    return chi2/nu

varcandi = glob.glob('results/*varcandi.txt')

for v in varcandi:
    fns = np.genfromtxt(v, dtype='string')

    for f in fns:
        t, f, e = np.genfromtxt(f, usecols=(0,1,2), unpack=True)

        #m1 = np.mean
        print f.max(), f.min()
