#!/home/kilrock/anaconda2/bin/python

import pyfits
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import glob
import time
import math

#default behavior is to plot all UVOT bands

MET_zero = 51910 #in MJD
object_name = raw_input('Enter Object Name: ')

bandInfo = [['uvv','V','gold'],
            ['ubb','B','lawngreen'],
            ['uuu','U','cyan'],
            ['uw1','UW1','blue'],
            ['um2','M','indigo'],
            ['uw2','UW2','violet']]

def plot(obsBand):
    maghistFile = 'final_science/UVOT/photometry_' + obsBand[0] + '.fits'

    HDUlist = pyfits.open(maghistFile)
    data1 = HDUlist[1].data
    MET = data1['met']
    MJD = MET_zero + MET/3600/24
    MJD = MJD - MJD[0]
    mag = data1['ab_mag']
    err = data1['ab_mag_err']

    for (day, magnitude, mag_err) in zip(MJD, mag, err):
        if mag_err < 1.5:
            plt.errorbar(day, magnitude, fmt = 'o', yerr = mag_err, color = obsBand[2])
        else:
            plt.errorbar(day, magnitude-mag_err, yerr = -0.3, uplims=True, fmt = ',', color = obsBand[2])

    plt.xlabel('Days since first observation')
    plt.ylabel('AB Magnitude')
    title = object_name + obsBand[1] + '-photometry'
    plt.title(title)

def allPlot():

    for obsBand in bandInfo:
        plot(obsBand)

    plt.gca().invert_yaxis()
    UVOTtitle = object_name + ' UVOT Photometry'

    Vband = mlines.Line2D([],[],color='gold', marker='o', label='V-band')
    Bband = mlines.Line2D([],[],color='lawngreen', marker='o', label='B-band')
    Uband = mlines.Line2D([],[],color='cyan', marker='o', label='U-band')
    UW1band = mlines.Line2D([],[],color='blue', marker='o', label='UW1-band')
    Mband = mlines.Line2D([],[],color='indigo', marker='o', label='M-band')
    UW2band = mlines.Line2D([],[],color='violet', marker='o', label='UW2-band')

    plt.legend(handles=[Vband, Uband, Bband, UW1band, Mband, UW2band], fontsize='10', labelspacing=0.25, loc='lower left')
    plt.title(UVOTtitle)

    #############################HELPFUL EDITS#########################
    # plt.ylim([25,16])  -->    then zoom to fit                      #
    # plt.legend(fontsize='12', labelspacing=0.25, loc='upper right') #
    ###################################################################

allPlot()
plt.show()
