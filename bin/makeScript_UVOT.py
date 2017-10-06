#!/home/kilrock/anaconda2/bin/python

import glob

uvotimsum = 'photometrySum'
uvotmaghist = 'photometryMag'
uvotBandList = ['uuu','uvv','ubb','um2','uw1','uw2']
allUVOT = open('allUVOT.bash', 'w')

def UVOTwrite(imageType):
                  allImageString = 'swift_data/*/0*/u*/i*/sw*' + imageType + '_sk.img*'
                  allImageFiles = sorted(glob.glob(allImageString))
                  scriptString = imageType + '.bash'
                  scriptFile = open(scriptString, 'w')
                  lightcurveFits = 'final_science/UVOT/photometry_' + imageType + '.fits\n'

                  count = 0

                  for imageFile in allImageFiles:
                                    fileName= 'UVOT_fits/' + imageType + str(count).zfill(3) + 'sum.fits'
                                    scriptFile.write(uvotimsum)
                                    scriptFile.write(' ' + imageFile + ' ')
                                    scriptFile.write(fileName + '\n')
                                    scriptFile.write(uvotmaghist)
                                    scriptFile.write(' ' + fileName + ' ')
                                    scriptFile.write(lightcurveFits)
                                    count += 1

allUVOT.write('rm -f UVOT_fits/*.fits final_science/UVOT/*.fits\n')

for uvotBand in uvotBandList:
                  UVOTwrite(uvotBand)                  
                  allUVOT.write('bash -e ' + uvotBand + '.bash\n')
