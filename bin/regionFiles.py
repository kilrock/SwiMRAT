#!/home/kilrock/anaconda2/bin/python

import sys

RA=sys.argv[1]
DEC=sys.argv[2]

begString='# Region file format: DS9 version 4.1\nglobal color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\nfk5\n'

regionFiles=[['src.reg',',5") # text={source}','circle('],
             ['bkg.reg',',40") # text={background}','annulus('],
             ['xsrc.reg',',11.7866") # text={xsource}','circle('],
             ['xbkg.reg',',23.5731",235.731") # text={xbackground}','annulus(']]

for regionFile in regionFiles:
    openFile=open('region_files/'+regionFile[0],'w')
    openFile.write(begString+regionFile[2]+RA+','+DEC+regionFile[1]+'\n')
