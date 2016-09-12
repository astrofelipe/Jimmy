import numpy as np
import sys
import matplotlib.pyplot as plt
from astropy.stats import mad_std

name = np.genfromtxt(sys.argv[1], usecols=(0,), dtype='string')
chi1, chi3 = np.genfromtxt(sys.argv[1], usecols=(1,2))

#Faltan los matches aca

row = int(np.ceil(len(name)/5.0))

#Plot
fig, ax = plt.subplots(ncols=5, nrows=row, figsize=[3*6, 3*row*3/5.0], sharex=True)
aa      = np.ravel(ax)

for i in range(len(name)):
    a = aa[i]
    l = name[i]
    t,m,e = np.genfomtxt(l, unpack=True, usecols=(0,1,2))
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

    lims  = a.get_ylim()
    ticks = np.arange(12, 21)
    a.set_yticks(ticks)
    a.set_xticks([])
    a.set_ylim(lims)

for a in aa[i+1:]:
    fig.delaxes(a)

fig.tight_layout()
fig.savefig(sys.argv[1].replace('varchis.txt','LPVs.png'), dpi=200, bbox_inches='tight')
