import numpy as np

alias_a = [0.997269/n for n in range(1,9)] #Dia sideral
alias_m = [27.322, 29.531]  #Mes sideral, mes sinodico

alias = np.concatenate([alias_a, alias_m])[:, np.newaxis]

def isAlias(p, tol=0.01):
  dper = np.abs(p - alias)
  isa  = np.any(dper <= tol, axis=0)
  return isa
