import math
import numpy


# ******************************
def get_const(B, N):

    invC = 0
    for n in numpy.arange(N + 1):
        invC += numpy.exp(-B) * B**n / math.factorial(n)
    return 1.0 / invC
    
    
# ******************************
def prob(N, B, S):

    C = get_const(B, N)
    return C * numpy.exp(- (S + B)) * (S + B) ** N / math.factorial(N)


# ******************************
def get_limits(N, B, cl):
    # N = number of counts in the aperture
    # B = expected number of background counts in the aperture
    # cl = desired confidence limit (e.g. 0.95 for 95%).

    S = numpy.linspace(0, 100, 10000)
    fnb = prob(N, B, S)

    pcut = fnb.max()
    ptot = fnb[ fnb >= pcut ].sum() / fnb.sum()
    while ptot < cl:
        pcut = fnb[ fnb < pcut ].max()
        ptot = fnb[ fnb >= pcut ].sum() / fnb.sum()

    Smin = S[ fnb >= pcut ].min()
    Sbest = S [ fnb.argmax() ] 
    Smax = S[ fnb >= pcut ].max()

    return (Smin, Sbest, Smax)
    
