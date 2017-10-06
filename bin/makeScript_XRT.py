#!/home/kilrock/anaconda2/bin/python

import glob

xselect =  'lightcurveX'

def XRTwrite():
                  allImageFiles = sorted(glob.glob('swift_data/*/0*/x*/e*/*xpcw3po_cl*'))
                  scriptFile = open('x.bash', 'w')

                  count = 0

                  for imageFile in allImageFiles:
                                    srcFile= 'x' + str(count).zfill(3) + 'src'
                                    bkgFile= 'x' + str(count).zfill(3) + 'bkg'
                                    scriptFile.write(xselect + ' ' + imageFile + ' ')
                                    scriptFile.write(srcFile + ' ' + bkgFile + '\n')
                                    count += 1  

XRTwrite()
