#!/home/kilrock/anaconda2/bin/python

import matplotlib.pyplot as plt
import numpy as np

xstring = "Days since first observation"
object_name = raw_input('Enter Object Name: ')
conf_string = raw_input('Enter confidence level [99%, 3sig, 4sig, or 5sig]: ')

if conf_string == '99%':
    filename = 'final_science/XRTbayes/99.txt'
elif conf_string == '3sig':
    filename = 'final_science/XRTbayes/threeSig.txt'
    conf_string = '3 $\sigma$'
elif conf_string == '4sig':
    filename = 'final_science/XRTbayes/fourSig.txt'
    conf_string = '4 $\sigma$'
else:
    filename = 'final_science/XRTbayes/fiveSig.txt'
    conf_string = '5 $\sigma$'

def bayesplot(filename):
    datafile = open(filename,'r')
    MJD = []
    lolims = []
    uplims = []
    while True:
        dataline = datafile.readline()
        if not dataline: break
        MJD.append(dataline.split(' ')[0])
        lolims.append(dataline.split(' ')[5])
        uplims.append(dataline.split(' ')[7])

    MJD = np.array(map(float, MJD))
    MJD = MJD-MJD[0]
    lolims = np.array(map(float, lolims))
    uplims = np.array(map(float, uplims))

    uplim_markers = []
    yerr_length = []

    for u in uplims:
            uplim_markers.append(True)
            yerr_length.append(u-(u/2.))

    for (day, lower, upper, marker, errLength) in zip(MJD, lolims, uplims, uplim_markers, yerr_length):
        if lower == 0:
            plt.errorbar(day, upper, yerr = errLength, uplims=marker, fmt = ',', color = 'k')
        else:
            plt.plot([day,day],[lower,upper],color='c')

    plt.yscale('log')
    plt.xlabel(xstring)
    plt.ylabel('X-Ray Luminosity (ergs/s)')
    plt.ylim([1e40,1e45])
    plt.title('Bayesian X-Ray Constraints for %s\nCL = %s' %(object_name,conf_string))
    plt.show()

bayesplot(filename)
