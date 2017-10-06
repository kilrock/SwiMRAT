#!/home/kilrock/anaconda2/bin/python

import pyfits
import matplotlib.pyplot as plt
import numpy as np
import glob
import time
import sys
from astropy.time import Time
import math
from scipy.stats import poisson
from scipy.stats import norm
from bayes import *

CRtoFlux = float(raw_input('Enter count rate to flux conversion factor: '))
luminosity_distance = float(raw_input('Enter luminosity distance in Mpc: '))

confidenceLimits = [[.99,'99'],
                    [norm.cdf(3, loc=0, scale=1),'threeSig'],
                    [norm.cdf(4, loc=0, scale=1),'fourSig'],
                    [norm.cdf(5, loc=0, scale=1),'fiveSig']]

def PCtoFlux(counts,expTime):
    return counts/expTime*CRtoFlux

def FluxtoLum(flux):
    sqcm_in_sqMpc = 1.05027E-49
    return flux*4.0*math.pi*(luminosity_distance**2)/sqcm_in_sqMpc

def PCtoLum(counts,expTime):
    return FluxtoLum(PCtoFlux(counts,expTime))

def bayesAnalysis(limit, filename):

    binsize = 5.0 #default binsize
    bkg_ratio = 396.0 #bkg to src ratio, bkg annulus 400R-2R, src circle R

    src = []
    bkg = []
    OBS_ID = []
    MJD = []
    expTimes = []
    fluxLimits = []
    luminosityLimits = []

    src_list = sorted(glob.glob('XRT_lightcurves/*src.lc'))
    bkg_list = sorted(glob.glob('XRT_lightcurves/*bkg.lc'))
    datafile = open(filename, 'w')

    for lcfile in src_list:

        src_lc = pyfits.open(lcfile)
        src_data = src_lc[1].data
        src_header = src_lc[1].header
        src_counts = (np.sum(src_data['rate'])) * binsize
        obsDate = src_header['DATE-OBS']

        expTimes.append(src_header['exposure'])
        src.append(int(src_counts))
        OBS_ID.append(src_header['OBS_ID'])
        MJD.append(Time(obsDate).mjd)

    for lcfile in bkg_list:

        bkg_lc = pyfits.open(lcfile)
        bkg_data = bkg_lc[1].data
        bkg_counts = ((np.sum(bkg_data['rate'])) * binsize) / bkg_ratio
        bkg.append(bkg_counts)

    fluxLimits = []
    luminosityLimits = []

    for (N, B, expTime) in zip(src, bkg, expTimes):
        countLimits = np.array(get_limits(N,B,limit))
        fluxLimits.append(PCtoFlux(countLimits,expTime))
        luminosityLimits.append(PCtoLum(countLimits,expTime))

    for (obs_id, mjd, expTime, N, B, fluxLim, lumLim) in zip(OBS_ID, MJD, expTimes, src, bkg, fluxLimits, luminosityLimits):
        datafile.write('%s %.2f %i %i %.5f %.3e %.3e %.3e %.3e %.3e %.3e\n' 
                       %(obs_id, mjd, expTime, N, B, fluxLim[0], fluxLim[1], fluxLim[2], lumLim[0], lumLim[1], lumLim[2]))
    
for limit in confidenceLimits:
    fileString = 'final_science/XRTbayes/raw/' + limit[1] + '.txt'
    bayesAnalysis(limit[0],fileString)
