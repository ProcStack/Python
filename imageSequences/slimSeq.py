# Slim image sequence
# Written by Kevin Edzenga
#
# For movies, having a lot of frames is great for smooth video
#
# But when it comes to generating gifs, without using a color pallette map
# Every frame counts in its file size
# Ending up with a 20 meg gif to display on the web is never fun for cell phone users not on wifi
#
#
# This script will copy every other frame in a seqence to "slim_*Name*" by default
# Using --skip / -s ; where the # following the flag is the count of skipped frames
# For example, given files in a folder-
# name.1.jpg, name.2.jpg, name.3.jpg, name.4.jpg, name.5.jpg, name.6.jpg, name.7.jpg
#  python slimSeq.py -s 2 name.#.jpg
# Will give you an output will be in the same folder and of -
#  slim_name.1.jpg, slim_name.2.jpg, slim_name.3.jpg
# Where slim_name.1.jpg is name.1.jpg; slim_name.2.jpg is name.4.jpg, slim_name.3.jpg is name.7.jpg
#
# The script checks if your image sequence starts at 0 or 1
# Currently it renumbers the images based on their current number
#

import argparse
import os
import shutil
import math
from PIL import Image

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('name', metavar='cName', type=str, nargs='+',
                   help='Image sequence to slim out')
parser.add_argument('-s', '--skip', help="Skip # frames; default is 1 with no flag")
parser.add_argument('-v', action='store_true', help="Verbose only, no actual files are created")

cDir=os.getcwd()+"/"
sName=parser.parse_args().name[0]
cName=cDir+sName
verb=parser.parse_args().v
skipCount=int(1 if parser.parse_args().skip==None else parser.parse_args().skip)+1
if "#" in sName:
	if skipCount==0:
		print
		print "Skip count is set to 0"
		print "This will simply copy your sequence to-"
		print " "+cDir+"slim_"+sName
		cont=raw_input('Would you like to continue? yes/y/1 or no/n/0\n ')
		if cont not in ['yes','y','1']:
			print "Cancelling slim sequence."
			exit()
	d=cName.split("/")
	if len(d)>1:
		readDir=""
		for x in range(len(d)-1):
			readDir=readDir+"/"+d[x]
	else:
		d=cDir
	search=d[-1].split("#")[0]
	dirList=os.listdir(readDir)
	print "\nSearching - "+cName
	print "\n-------------------------\n-Finding slim-able files-\n-------------------------"
	move=0
	moveList=[]
	splitName=sName.split("#")
	fileStart=1 if os.path.exists(cDir+splitName[0]+"0"+splitName[1])==False else 0
	for x in range(len(dirList)):
		if dirList[x][:len(splitName[0])] == splitName[0]:
			to=sName.split("#") # Was running into an issue just reassigning this to splitName, too tired to look into this further for now
			val=dirList[x][(len(splitName[0])):][:-(len(splitName[1]))]
			if (int(val)-fileStart)%skipCount == 0:
				num=int((int(val)-fileStart)/skipCount)+fileStart
				to[0]="slim_"+to[0]
				to=str(num).join(to)
				print dirList[x]+" - "+to	
				if verb == False :
					shutil.copy(dirList[x], to)
else:
	print "Please indicate a sequence using '#'"	
