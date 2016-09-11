import glob
import numpy as np
from astropy.stats import mad_std

#Test de chi2
def redchi2(y, m, s, dof=0):
    chi2 = np.sum(np.square((y - m)/s))
    nu   = len(data) - 1 - dof
    return chi2/nu

#Abre curva de luz
def openlc(f):
    data = np.genfromtxt(f, usecols=(0,1,2))
    data = data[data[:,1] < 98]

    #Sigma clip
    med = np.median(data[:,1])
    std = mad_std(data[:,1])
    res = data[:,1] - med
    cli = np.abs(res) < 3*std

    #Variables
    t, m, e = np.transpose(data[cli])
    return t, m, e

#Abre y hace Test
def combo(f):
    t, m, e = openlc(f)

    m1 = np.mean(m)
    m2 = np.polyval(np.polyfit(t, m, 2), t)

varcandi = glob.glob('results/*varcandi.txt')

for v in varcandi:
    fns = np.genfromtxt(v, dtype='string')

    for f in fns:
        combo(f)
