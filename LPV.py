import matplotlib
matplotlib.use('Agg')

import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.stats import mad_std

#Test de chi2
def redchi2(y, m, s, dof=0):
    chi2 = np.sum(np.square((y - m)/s))
    nu   = len(y) - 1 - dof
    return chi2/nu

#Abre curva de luz
def openlc(f):
    data = np.genfromtxt(f, usecols=(0,1,2))
    data = data[data[:,1] < 98]
    data[:,2][data[:,2] == 0] = 0.001

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
    
    A0  = np.ones(len(t))
    A   = np.transpose([A0, t, t**2])
    ATA = np.dot(A.T, A / e[:, np.newaxis]**2)
    mu  = np.linalg.solve(ATA, np.dot(A.T, m/e**2))

    m2 = np.polyval(mu[::-1], t)
    
    chi1 = redchi2(m, m1, e)
    chi3 = redchi2(m, m2, e, dof=2)

    return f, chi1, chi3

varcandi = glob.glob('results/*varcandi.txt')

figa, axa = plt.subplots(figsize=[4,3])

for v in varcandi:
    print v
    fns = np.genfromtxt(v, dtype='string')

    chi = np.array([combo(f) for f in fns])
    np.savetxt(v.replace('varcandi.txt', 'varchis.txt'), chi, fmt='%s', header='FILE CHI1 CHI3')

    chi1 = chi[:,1].astype(float)
    chi3 = chi[:,2].astype(float)
    fchi = chi3 / chi1

    fmed = np.median(fchi)
    fstd = mad_std(fchi)

    fig, ax = plt.subplots(figsize=[4,3])
    ax.plot(chi3, fchi, '.k', ms=2)
    axa.plot(chi3, fchi, '.k', ms=.5)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('%s\nMED=%.4f / STD=%.4f' % (v, fmed, fstd))
    ax.set_ylim(0.001, 2)
    print fchi.min(), fchi.max()
    ax.set_xlabel('$\chi^2_{N-3}$')
    ax.set_ylabel('$\chi^2_{N-3} / \chi^2_{N-1}$')
    ax.axhline(0.4, dashes=(5,5), color='k', lw=.5)
    fig.savefig(v.replace('varcandi.txt', 'LPVchi.png'), dpi=200, bbox_inches='tight')
    plt.close(fig)

axa.set_xscale('log')
axa.set_yscale('log')
axa.set_title('All Fields')
axa.set_ylim(0.001, 2)
axa.set_xlabel('$\chi^2_{N-3}$')
axa.set_ylabel('$\chi^2_{N-3} / \chi^2_{N-1}$')
axa.axhline(0.4, dashes=(5,5), color='k', lw=.5)
figa.savefig('results/all_LPVchi.png', dpi=200, bbox_inches='tight')
