#!/home/kilrock/anaconda2/bin/python

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

fullstackfile = open('final_science/XRTbayes/fullstack.txt','w')

confidenceLimits = [[.99,'99'],
                    [norm.cdf(3, loc=0, scale=1),'threeSig'],
                    [norm.cdf(4, loc=0, scale=1),'fourSig'],
                    [norm.cdf(5, loc=0, scale=1),'fiveSig']]

def fullstack(limit,filename):

    datafile = open(filename,'r')
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

    stackdata = get_limits(sum(N),sum(B),limit)

    Fmin = stackdata[0]/sum(exp)*flux_conversion
    Fbest = stackdata[1]/sum(exp)*flux_conversion
    Fmax = stackdata[2]/sum(exp)*flux_conversion
    Lmin = Fmin/sqcm_in_sqMpc*luminosity_conversion
    Lbest = Fbest/sqcm_in_sqMpc*luminosity_conversion
    Lmax = Fmax/sqcm_in_sqMpc*luminosity_conversion
    
    return(Fmin, Fbest, Fmax, Lmin, Lbest, Lmax)

for limit in confidenceLimits:
    fileString = 'final_science/XRTbayes/' + limit[1] + '.txt'
    limits = fullstack(limit[0],fileString)
    fullstackfile.write('%s\n%.3e %.3e %.3e %.3e %.3e %.3e\n' %(limit[1], limits[0], limits[1], limits[2], limits[3], limits[4], limits[5]))
