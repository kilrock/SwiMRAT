import pyfits
import matplotlib.pyplot as plt
import numpy as np
import glob
import time
import math
from bayes import *
from astropy.time import Time
from scipy.stats import poisson
from scipy.stats import norm

flux_conversion = float(raw_input('Enter count rate to flux conversion factor: '))
luminosity_distance = float(raw_input('Enter luminosity distance in Mpc: '))

luminosity_conversion = 4.0*math.pi*(luminosity_distance**2)
sqcm_in_sqMpc = 1.05027E-49

confidenceLimits = [[.99,'99'],
                    [norm.cdf(3, loc=0, scale=1),'threeSig'],
                    [norm.cdf(4, loc=0, scale=1),'fourSig'],
                    [norm.cdf(5, loc=0, scale=1),'fiveSig']]

def splitstack(textfile,limit):

    #This is hard coded for ASASSN-15lh and its rebrightening phase
    datafile = open(textfile,'r')
    datalines = datafile.readlines()
    datafile.close()

    MJD = []
    exp = []
    N = []
    B = []

    for line in datalines:
        datapoint = line.split()
        MJD.append(float(datapoint[0]))
        exp.append(float(datapoint[1]))
        N.append(float(datapoint[2]))
        B.append(float(datapoint[3]))

    exp_1 = sum(exp[0:28])
    limits_1=get_limits(sum(N[0:28]),sum(B[0:28]),limit)

    Fmin_1 = limits_1[0]/exp_1*flux_conversion
    Fbest_1 = limits_1[1]/exp_1*flux_conversion
    Fmax_1 = limits_1[2]/exp_1*flux_conversion
    Lmin_1 = Fmin_1/sqcm_in_sqMpc*luminosity_conversion
    Lbest_1 = Fbest_1/sqcm_in_sqMpc*luminosity_conversion
    Lmax_1 = Fmax_1/sqcm_in_sqMpc*luminosity_conversion

    exp_2 = sum(exp[28:])
    limits_2=get_limits(sum(N[28:]),sum(B[28:]),limit)
    
    Fmin_2 = limits_2[0]/exp_2*flux_conversion
    Fbest_2 = limits_2[1]/exp_2*flux_conversion
    Fmax_2 = limits_2[2]/exp_2*flux_conversion
    Lmin_2 = Fmin_2/sqcm_in_sqMpc*luminosity_conversion
    Lbest_2 = Fbest_2/sqcm_in_sqMpc*luminosity_conversion
    Lmax_2 = Fmax_2/sqcm_in_sqMpc*luminosity_conversion

    stackfile.write('%s' %textfile)
    stackfile.write('%.2f:%.2f %i %.3e %.3e %.3e %.3e %.3e %.3e\n' %(MJD[0], MJD[27], exp_1, Fmin_1, Fbest_1, Fmax_1, Lmin_1, Lbest_1, Lmax_1))
    stackfile.write('%.2f:%.2f %i %.3e %.3e %.3e %.3e %.3e %.3e\n' %(MJD[28], MJD[83], exp_2, Fmin_2, Fbest_2, Fmax_2, Lmin_2, Lbest_2, Lmax_2))
