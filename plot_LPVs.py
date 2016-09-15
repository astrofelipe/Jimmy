import matplotlib
matplotlib.use('Agg')
import numpy as np
import sys
import matplotlib.pyplot as plt
from astropy.stats import mad_std
from utils import isAlias

name = np.genfromtxt(sys.argv[1], usecols=(0,), dtype='string')
chi1, chi3, p, fap = np.genfromtxt(sys.argv[1], usecols=(1,2,3,4), unpack=True)

chi = chi3/chi1
ma  = chi < 0.4

name = name[ma]
chi  = chi[ma]
p    = p[ma]
fap  = fap[ma]

alias = isAlias(p)
acols = ['#017d3f' if not al  else '#a4142a' for al in alias]

#Faltan los matches aca

row = int(np.ceil(len(name)/5.0))

#Plot
fig, ax = plt.subplots(ncols=5, nrows=row, figsize=[3*6, 3*row*3/5.0], sharex=True)
aa      = np.ravel(ax)

for i in range(len(name)):
    a = aa[i]
    l = name[i]
    t,m,e = np.genfromtxt(l, unpack=True, usecols=(0,1,2))
    ph    = t / p[i] % 1.0

    mag_ma = m < 90
    std    = mad_std(m[mag_ma])
    med    = np.median(m[mag_ma])
    cli_ma = np.abs(m-med) < 5*std
    ma     = mag_ma & cli_ma

    #maidx  = np.where(lcm==l)
    #mat    = lcm[maidx][0]

    a.plot(ph[ma], m[ma], 'o', color='#0083cb', ms=3)
    a.plot(ph[ma]+1, m[ma], 'o', color='#0083cb', ms=3)

    a.text(0.95, 0.1, 'P = %f' % p[i], ha='right', va='center', transform=a.transAxes, color=acols[i])


    lims  = a.get_ylim()
    ticks = np.arange(12, 21)
    a.set_yticks(ticks)
    a.set_xticks([])
    a.set_ylim(lims)

for a in aa[i+1:]:
    fig.delaxes(a)

fig.tight_layout()
fig.savefig(sys.argv[1].replace('varchis.txt','LPVs.png'), dpi=200, bbox_inches='tight')
