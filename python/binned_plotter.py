import pyfits
import matplotlib.pyplot as plt
import numpy as np
import glob
import time
from scipy.stats import poisson
from scipy.stats import norm

xstring = "Time in days before %r" % time.ctime()
object_name = raw_input('Enter Object Name: ')
txt = open(raw_input('Enter data file name: '))

lines = txt.readlines()
src = []
bkg = []
three_sig_uplims = []
five_sig_uplims = []
corrected_times = []

for line in lines:
    current_data = line.split()
    src.append(float(current_data[3]))
    bkg.append(float(current_data[4]))
    three_sig_uplims.append(float(current_data[5]))
    five_sig_uplims.append(float(current_data[6]))
    corrected_times.append(float(current_data[7]))

uplim_markers = []

for u in three_sig_uplims:
    uplim_markers.append(True)

three_sig_uplims = np.array(three_sig_uplims)
five_sig_uplims = np.array(five_sig_uplims)

errorbar_length = []
errorbar_length = five_sig_uplims - three_sig_uplims

plt.errorbar(corrected_times, five_sig_uplims, yerr = errorbar_length, uplims=uplim_markers, fmt = ',', color = 'c')

for (days_ago, counts, three_sig, five_sig) in zip(corrected_times, src, three_sig_uplims, five_sig_uplims):
    if counts == 0:
        plt.plot(days_ago, counts, 'co')
    elif counts < three_sig:
        plt.plot(days_ago, counts, 'co')
    elif counts > five_sig:
        plt.plot(days_ago, counts, 'ro')
    else:
        plt.plot(days_ago, counts, 'go')

plt.gca().invert_xaxis()
plt.xlabel(xstring)
plt.ylabel('Counts')
Xtitle = object_name + ' X-photometry'
plt.title(Xtitle) 
