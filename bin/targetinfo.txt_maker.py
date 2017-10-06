#!/home/kilrock/anaconda2/bin/python

import sys

def infoMaker(TargetName):
    objType = raw_input('Type: ')
    objCoor = raw_input('Coordinates: ')
    galacNh = raw_input('Galactic Nh (Weighted, Dickey & Lockman /cm/cm): ')
    fluxConv = raw_input('Flux Conversion (ergs/cm/cm/s): ' )
    weightedFluxConv = raw_input('Unabsorbed Flux Conversion (ergs/cm/cm/s): ' )
    redShift = raw_input('z = ')
    lumDist = raw_input('Luminosity Distance (Mpc): ')

    infoFile = open('targetinfo.txt','w')

    infoFile.write('Target Name: %s\n' % TargetName)
    infoFile.write('Type: %s\nCoordinates: %s\n' %(objType,objCoor))
    infoFile.write('Galactic Nh (Weighted, Dickey & Lockman /cm/cm): %s\n' %galacNh)
    infoFile.write('Flux Conversion (ergs/cm/cm/s): %s\n' %fluxConv)
    infoFile.write('Unabsorbed Flux Conversion (ergs/cm/cm/s): %s\n' %weightedFluxConv)
    infoFile.write('redShift: %s\nLuminosity Distance: %s Mpc\n' %(redShift,lumDist))

infoMaker(sys.argv[1])
