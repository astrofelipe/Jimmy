import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

alias_a = [0.997269/n for n in range(1,9)] #Dia sideral
alias_m = [27.322, 29.531]  #Mes sideral, mes sinodico

alias = np.concatenate([alias_a, alias_m])[:, np.newaxis]

def isAlias(p, tol=0.01):
  dper = np.abs(p - alias)
  isa  = np.any(dper <= tol, axis=0)
  return isa

def Grid4(row, col):
    gs    = gridspec.GridSpec(2,10)
    left  = col*0.24 + 0.04
    right = left + 0.2

    gs.update(left=left, right=right, top=row, bottom=(row-0.8))

    ax1 = plt.subplot(gs[0, :5])
    ax2 = plt.subplot(gs[1, :5])
    ax3 = plt.subplot(gs[0, 5:])
    ax4 = plt.subplot(gs[1, 5:])

    return ax1, ax2, ax3, ax4
