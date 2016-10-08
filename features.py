import numpy as np
from astropy.stats import median_absolute_deviation as mad

def p2p_scatter_pfold_over_mad(t, f, P):
    N   = len(t)
    MAD = mad(f)

    ph = (t/P) % 1.0
    so = np.argsort(ph)
    ph = ph[so]
    f  = f[so]

    num = np.sum(np.abs(np.diff(f)))

    return num / MAD
