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

confidenceLimits = [[.99,'99'],
                    [norm.cdf(3, loc=0, scale=1),'threeSig'],
                    [norm.cdf(4, loc=0, scale=1),'fourSig'],
                    [norm.cdf(5, loc=0, scale=1),'fiveSig']]

def littlestack(filename,limit):

    datafile = open(filename,'r')
    datalines = datafile.readlines()
    datafile.close()

    MJD = []
    exp = []
    N = []
    B = []
    Fmin = []
    Fbest = []
    Fmax = []
    Lmin = []
    Lbest = []
    Lmax = []

    for line in datalines:
        datapoint = line.split()
        MJD.append(float(datapoint[0]))
        exp.append(float(datapoint[1]))
        N.append(float(datapoint[2]))
        B.append(float(datapoint[3]))
        Fmin.append(float(datapoint[4]))
        Fbest.append(float(datapoint[5]))
        Fmax.append(float(datapoint[6]))
        Lmin.append(float(datapoint[7]))
        Lbest.append(float(datapoint[8]))
        Lmax.append(float(datapoint[9]))

    if len(MJD) == 1:
        return

    i = 0
    j = 1
    newlimits = []

    datafile = open(filename,'w')

    while j<len(MJD):
        if MJD[i] == MJD[j]:
            newexp = exp[i]+exp[j]
            newN = N[i]+N[j]
            newB = B[i]+B[j]

            newlimits = get_limits(newN, newB, limit)
            newFmin = newlimits[0]/newexp*flux_conversion
            newFbest = newlimits[1]/newexp*flux_conversion
            newFmax = newlimits[2]/newexp*flux_conversion
            newLmin = newFmin/sqcm_in_sqMpc*luminosity_conversion
            newLbest = newFbest/sqcm_in_sqMpc*luminosity_conversion
            newLmax = newFmax/sqcm_in_sqMpc*luminosity_conversion

            datafile.write('%.2f %i %i %.5f %.3e %.3e %.3e %.3e %.3e %.3e\n' %(MJD[i], newexp, newN, newB, newFmin, newFbest, newFmax, newLmin, newLbest, newLmax))
            i+=2
            j+=2
        else:
            datafile.write('%.2f %i %i %.5f %.3e %.3e %.3e %.3e %.3e %.3e\n' %(MJD[i], exp[i], N[i], B[i], Fmin[i], Fbest[i], Fmax[i], Lmin[i], Lbest[i], Lmax[i]))
            if j==(len(MJD)-1):
                datafile.write('%.2f %i %i %.5f %.3e %.3e %.3e %.3e %.3e %.3e\n' %(MJD[j], exp[j], N[j], B[j], Fmin[j], Fbest[j], Fmax[j], Lmin[j], Lbest[j], Lmax[j]))
            i+=1
            j+=1

for limit in confidenceLimits:
    fileString = 'final_science/XRTbayes/' + limit[1] + '.txt'
    littlestack(fileString,limit[0]) 
