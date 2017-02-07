# Crop an image sequence
# Written by Kevin Edzenga
#
# Run this within a folder with a dedicated sequence of images you'd like to crop
# Folders are bypassed
#
# Output files will prepend "crop_" to the file by default
# Change the output prefix by changing the prefix variable below
# I left this out of the argparser because I haven't cared enough for my uses of this script
#
# Wand installation and documentation-
# http://docs.wand-py.org/en/0.4.1/guide/install.html

import os
from wand.image import Image
import argparse

prepend="crop"

parser = argparse.ArgumentParser(description='Process min/max array.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('mmVals', metavar='mmVals', type=str, nargs='+',
                   help="[minX,minY,maxX,maxY] From upper left; "+__file__.split('/')[-1]+" [0,0,500,250]")
                   
minMaxCrop=eval(parser.parse_args().mmVals[0]) # Parse Min Max arguments
readDir=os.getcwd() # Current folder location
dirList=os.listdir(readDir) # Read folder contents
for x in dirList:
	if os.path.isfile(readDir+'/'+x) :
		image = Image(filename=readDir+'/'+x) # Read image
		image.crop(minMaxCrop[0], minMaxCrop[1], minMaxCrop[2], minMaxCrop[3]) # Crop image
		image.save(filename=readDir+'/'+prepend+'_'+x) # Save image
		print "Cropped - "+x+" to crop_"+x
