import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib import rc
from astropy.stats import mad_std
from utils import isAlias

rc('ytick', labelsize=6) 
rc('axes.formatter', useoffset=False)

f = sys.argv[1]

lc = np.genfromtxt(f, usecols=(0,), dtype=str)
p, fap     = np.genfromtxt(f, usecols=(3,6), unpack=True)
lcn, match = np.genfromtxt(f.replace('results/', 'lists/').replace('varstats.txt', 'list_matches.txt'), delimiter=',', unpack=True, dtype=str)
lcc             = np.genfromtxt(f.replace('results/', 'lists/').replace('varstats.txt', 'list_crowd.txt'), usecols=(0,), dtype=str)
capass, casassn = np.genfromtxt(f.replace('results/', 'lists/').replace('varstats.txt', 'list_crowd.txt'), unpack=True, usecols=(2,4))

#print lc.size, lcn.size

lcord = np.argsort(lc)
lc    = lc[lcord]
p     = p[lcord]
fap   = fap[lcord]

#match = match[np.argsort(lcn)]

#print len(match), len(lc), np.in1d(lc, match).sum() 
#print match, lc

nlc = len(lc)

row   = int(np.ceil(nlc/5.0))
faptf = -fap < -50
fapco = np.array(['#017d3f' if fa else '#a4142a' for fa in faptf])

if len(sys.argv)>2:
    row = int(np.ceil(faptf.sum()/5.0))
    lc  = lc[faptf]
    p   = p[faptf]
    #match = match[faptf]
    fap = fap[faptf]
    fapco = fapco[faptf]

alias = isAlias(p)
acols = ['#017d3f' if not al  else '#a4142a' for al in alias]

nmatches = 0

print 'Total curvas:        %d' % len(lc)
print 'Total matches:       %d' % np.sum(match!='no match')
print 'Matches esperados:   %d' % np.sum(np.in1d(lc, lcn[match!='no match']))

nfma = np.in1d(lcn[match!='no match'], lc, invert=True)
notfound = lcn[nfma]
np.savetxt(f.replace('varstats.txt', 'matchnotfound.txt'), notfound, fmt='%s')

#nfo = np.sum(nfma)
#nma = np.sum(lcn!='no match')
#nom = np.sum(lcn=='no match')
#nfa = np.sum(faptf)
nal = (-fap < -50) & np.in1d(lc, lcn[match=='no match'])

allok = ['#017d3f' if yes else 'k' for yes in nal]

def do_plot(lc, end=0, first=0):
  nrows = np.min([20, row])
  #print 3*6, 3*row*3/5.0, row, nrows
  fig, ax = plt.subplots(ncols=5, nrows=nrows, figsize=[3*6, 3*nrows*3/5.0], sharex=True)
  aa      = np.ravel(ax)
  end     = int(end)
  first   = int(first)
  global nmatches

  for i in range(len(lc)):
      a = aa[i]
      l = lc[i]
      t,m,e = np.genfromtxt(l, unpack=True, usecols=(0,1,2))
      ph    = t/p[i+first] % 1.0

      mag_ma = m < 90
      std    = mad_std(m[mag_ma])
      med    = np.median(m[mag_ma])
      cli_ma = np.abs(m-med) < 5*std
      ma     = mag_ma & cli_ma

      maidx  = np.where(lcn==l)
      lmatch = match[maidx][0]

      cridx    = np.where(lcc==l)
      lcapass  = capass[cridx][0]
      lcasassn = casassn[cridx][0]
      crowdcol = '#017d3f' if ((lcapass==1) and (lcasassn==1)) else 'orange'

      a.plot(ph[ma], m[ma], 'o', color='#0083cb', ms=3)
      a.plot(ph[ma]+1, m[ma], 'o', color='#0083cb', ms=3)
      t1 = a.text(0.05, 1.06, l.split('/')[-1], ha='left', va='center', transform=a.transAxes, color=allok[i+first], fontsize=8)
      t2 = a.text(0.95, 0.1, 'P = %f' % p[i+first], ha='right', va='center', transform=a.transAxes, color=acols[i+first])
      t3 = a.text(0.05, 0.1, '$\log_{10}$FAP = %.3f' % -fap[i+first], ha='left', va='center', transform=a.transAxes, color=fapco[i+first])
      msplit = lmatch.split(' ')
      #print msplit
      if msplit[0] != 'no':
          t4 = a.text(0.95, 0.925, '%s\n%s' % (msplit[0], msplit[3]), ha='right', va='top', transform=a.transAxes, color='#000000', fontsize=8)
          t4.set_bbox(dict(color='white', alpha=.5))
          nmatches += 1
      t5 = a.text(0.95, 1.06, '%.3f %.3f' % (lcapass, lcasassn), ha='right', va='center', transform=a.transAxes, fontsize=8, color=crowdcol)
      t1.set_bbox(dict(color='white', alpha=.25))
      t2.set_bbox(dict(color='white', alpha=.5))
      t3.set_bbox(dict(color='white', alpha=.5, lw=0))
      lims  = a.get_ylim()
      #ticks = np.arange(12, 21, 0.5)
      #a.set_yticks(ticks)
      a.set_xticks([])
      #a.set_ylim(lims)
      a.invert_yaxis()
  aa[-1].set_xlim(0,2)

  for a in aa[i+1:]:
      fig.delaxes(a)
  #info = fig.add_axes([0,1,1,0.1])
  fig.suptitle('Total: %d    Total matches: %d    Matches found: %d    FAP OK: %d    All OK: %d' % (len(lc), np.sum(match!='no match'),np.sum(np.in1d(lc, lcn[match!='no match'])), np.sum(faptf), np.sum(nal)) , y=1.01)
  fig.tight_layout()#rect=[0, 0, 1, 0.98])

  foutn = f.replace('varstats.txt', 'lcs')
  if end!=0:
      foutn = foutn + '_%d' % end

  if len(sys.argv)>2:
      fig.savefig(foutn + '_f.png', bbox_inches='tight')
  else:
      fig.savefig(foutn, bbox_inches='tight')
  plt.close(fig)

if nlc <= 100:
    do_plot(lc)
else:
    nplots = int(np.ceil(nlc/100.0))
    lnum   = nlc - (nplots-2)*100
    #first  = [lc[100*j:100*(j+1)] for j in range(nplots-2)]
    chunks = np.array_split(lc, nplots)
    lchunk = np.array([len(ch) for ch in chunks])
    #print lchunk

    for j in range(len(chunks)):
        #print j+1, np.sum(lchunk[:j])
        do_plot(chunks[j], end=j+1, first=np.sum(lchunk[:j]))
    #do_plot(lc[100*(nplots-2):100*(nplots-2)+int(np.ceil(lnum/2.0))], end=nplots-1, first=100*(nplots-2))
    #do_plot(lc[100*(nplots-2)+int(np.ceil(lnum/2.0)):], end=nplots, first=100*(nplots-2)+int(np.ceil(lnum/2.0)))

print 'Matches recuperados: %d' % nmatches
