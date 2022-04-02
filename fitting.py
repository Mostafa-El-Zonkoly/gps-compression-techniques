import numpy as np
from numpy import exp, loadtxt, pi, sqrt
from lmfit import Model
     
def gaussian(x, amp, cen, wid):
    return amp * np.exp(-(x-cen)**2 / wid)

def curveFitting(data): 
    gmodel = Model(gaussian)
    result = gmodel.fit(data, tau=5, N=3)
    return(result)