#!/home/kilrock/anaconda2/bin/python

import pyfits
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import glob
import time
import math
from astropy.time import Time
from scipy.stats import poisson
from scipy.stats import norm

MET_zero = 51910 #in MJD
xstring = "Modified Julian Day"
object_name = raw_input('Enter Object Name: ')
CRtoFluX = float(raw_input('Enter count rate to flux conversion factor: '))
luminosity_distance = float(raw_input('Enter luminosity distance in Mpc: '))

def PCtofluX(counts,expTime):
    return counts/expTime*CRtoFluX

def fluXtoLum(fluX):
    sqcm_in_sqMpc = 1.05027E-49
    FluXtoLum = 4.0*math.pi*(luminosity_distance**2)/sqcm_in_sqMpc
    return fluX*FluXtoLum

def PCtoLum(counts,expTime):
    return fluXtoLum(PCtofluX(counts,expTime))
    
def Xplot():
    binsize = 5.0 #default binsize
    bkg_ratio = 396.0 #bkg to src ratio, bkg annulus 400R-2R, src circle R

    src = []
    src_list = sorted(glob.glob('XRT_lightcurves/*src.lc'))

    MET = []
    expTimes = []

    for lcfile in src_list:

        src_lc = pyfits.open(lcfile)
        src_data = src_lc[1].data
        src_header = src_lc[1].header
        src_counts = (np.sum(src_data['rate'])) * binsize
        expTimes.append(src_header['exposure'])
        src.append(src_counts)
        head1 = src_lc[1].header
        median_MET = head1['tstart'] + ((head1['tstop']-head1['tstart'])/2)
        MET.append(median_MET)

    bkg = []
    bkg_list = sorted(glob.glob('XRT_lightcurves/*bkg.lc'))

    for lcfile in bkg_list:

        bkg_lc = pyfits.open(lcfile)
        bkg_data = bkg_lc[1].data
        bkg_counts = ((np.sum(bkg_data['rate'])) * binsize) / bkg_ratio
        bkg.append(bkg_counts)

    three_sig = norm.cdf(3, loc=0, scale=1)
    four_sig = norm.cdf(4, loc=0, scale=1)
    five_sig = norm.cdf(5, loc=0, scale=1)
    three_sig_uplims = []
    four_sig_uplims = []
    five_sig_uplims = []

    for (mu, src_point) in zip(bkg, src):
        if mu == 0.0:
            three_sig_uplim = 0.0
            three_sig_uplims.append(three_sig_uplim)
            four_sig_uplim = 0.0
            four_sig_uplims.append(four_sig_uplim)
            five_sig_uplim = 0.0
            five_sig_uplims.append(five_sig_uplim)

        else:
            three_sig_uplim = poisson.ppf(three_sig, mu, loc = 0)
            three_sig_uplims.append(three_sig_uplim)
            four_sig_uplim = poisson.ppf(four_sig, mu, loc = 0)
            four_sig_uplims.append(four_sig_uplim)
            five_sig_uplim = poisson.ppf(five_sig, mu, loc = 0)
            five_sig_uplims.append(five_sig_uplim)

    uplim_markers = []

    for u in three_sig_uplims:
            uplim_markers.append(True)

    three_sig_uplims = np.array(three_sig_uplims)
    five_sig_uplims = np.array(five_sig_uplims)

    corrected_times = []
    MET = np.array(MET)

    corrected_times = (MET/3600/24) + MET_zero

    errorbar_length = []
    errorbar_length = five_sig_uplims - three_sig_uplims

    for (MJD, counts, expTime, three_sig, four_sig, five_sig, err) in zip(corrected_times, src, expTimes, three_sig_uplims, four_sig_uplims, five_sig_uplims, errorbar_length):
        luminosity = PCtoLum(counts,expTime)
        if counts > five_sig:
            plt.plot(MJD, luminosity, 'bo')
        elif counts > four_sig:
            plt.plot(MJD, luminosity, 'steelblueo')
        elif counts > three_sig:
            plt.plot(MJD, luminosity, 'co')
        else:
            plt.errorbar(MJD, PCtoLum(five_sig,expTime), yerr = PCtoLum(err,expTime), uplims=True, fmt = ',', color = 'k')

    plt.yscale('log')
    plt.xlabel(xstring)
    plt.ylabel('Luminosity ergs/s')
    plt.ylim([1e40,1e45])
    Xtitle = object_name + ' X-photometry'
    plt.title(Xtitle) 
    plt.show()

Xplot()
