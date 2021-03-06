"""
Comments to come, my apologies
This is a dump for a pixel processing test using pygame.
** Pygame is very slow for full screen pixel processing, this was made with the intention of running on a RaspberryPi, but it seems OpenGL is the better option in this situation**

Here is the kind of effects you'll see with this script-
https://www.youtube.com/watch?v=NvqFOaD-OWo
https://www.youtube.com/watch?v=-U6eKRmdEyo

After installing required modules, running without any flags will run default values and random modes-
python pixelProcessing.py

-----------------

What you'll find in this python script-
Pixel processing on a per pixel level using an array of [R1,G1,B1, R2,G2,B2, ... R#,G#,B#]
RGB to HSV;  HSV to RGB (I'm still working out a bug when Hue rolls over past 1.  0-1 should be the same Hue, but is not
Rotating values around a given postion in the screen
Transitions between modes

-----------------

Command to run- ** Hit Escape to quit **
python visualizer.py (verbosePrint) (Visual#; 0-6) (Resolution#) (ScreenShots/Windowed mode)

Resolution of 20-
python visualizer.py 20

Mode 4; resoltion of 10
python visualizer.py 4 10

Verbose printing on screen, resolution 10
python visualizer.py v 10

Windowed resolution of 20
python visualizer.py 20 w

-----------------

!! Important Python Modules & Linux apt-get commands ~~
** I'll update this list with the windows module documentation pages in time, you will need to install these modules for python manually for Windows/Mac**
GTK-
sudo apt-get install python-gtk2

CTypes-
sudo apt-get install python-ctypeslib

Pygame-
sudo apt-get install python-pygame

Xlib-
sudo apt-get install libx11-dev

Muliprocessing- (Not used as much as I'd like to be using it in this script)
sudo apt-get install python-multiprocessing

Numpy-
Just a heads up, I ran into some issues with running Numpy, finding out that I'd need to uninstall it and reinstall it, you might not need to do this
- From - http://stackoverflow.com/questions/9449309/how-to-correctly-install-python-numpy-in-ubuntu-11-10-oneiric
sudo apt-get remove python-numpy
sudo rm -r /usr/local/lib/pythonX.X/dist-packages/numpy
sudo apt-get install python-numpy

"""

import gtk

import ctypes
import pygame
import time
from multiprocessing import Pool, Queue
#import Queue
#import threading
import sys, os
import math
import random
import numpy as np
from Xlib import X, display
#execfile("particles.py")

threadCount=1
verbose=0
verbObj=[]
scale=15  

w = gtk.gdk.screen_width()/2  #  683
h = gtk.gdk.screen_height()/2  #  384
mouse=(w/2,h/2)
screen=(w,h)
runner=198
maxMode=6
curTime=time.time()
prevTime=time.time()
ssActive=0
fullScreen=1
argvMode=None
try:
	if sys.argv[1] in ("ver", "verb", "v", "verbose"):
		verbose=1
		if len(sys.argv) >= 3:
			argvMode=int(sys.argv[2])
			if len(sys.argv) == 4:
				scale=int(sys.argv[3])
	else:
		try:
			argvMode=int(sys.argv[1])
			if len(sys.argv) >= 3:
				scale=int(sys.argv[2])
		except:
			pass;
	if sys.argv[-1] in ("ss", "screen","out", "output"):
		ssActive=1
	if sys.argv[-1] in ("w", "win", "window", "windowed"):
		fullScreen=0
except:
	pass;
#scale=math.sin(float(runner/2))*5+9
surfSize=(int(w/scale/threadCount), int(h/scale))
sw=surfSize[0]
sh=surfSize[1]
mode=[0,0]
if argvMode > maxMode:
	scale=argvMode
	argvMode=None

if argvMode == None:
	mode[0]=(min(int(random.random()*(maxMode+1)),maxMode))
	mode[1]=(min(int(random.random()*(maxMode+1)),maxMode))
	run=0
	if mode[0] == mode[1]:
		while True:
			run+=1
			random.seed(run)
			val=min(int(random.random()*(maxMode+1)),maxMode)
			if val != mode[0]:
				mode[1]=val
				break

modeVal=[]
minMax=[0,0]
blendMode=0
curMode=-1
prevMode=mode[1]
modeChange=-1
setMode=-1
for x in range(maxMode+1):
	modeVal.append([])
#print "["+str(w/scale)+", "+str(h/scale)+"]"
pi=3.1415926535
trans=0
particleCap=50
def queueRun(q,imgList):
	global threadCount
	global pix
	while True:
		pxRun=q.get(True)
		pxProcess(imgList[pxRun],0)
		#pxChunk(pxRun,threadCount)

def fill(size):
	img=pygame.Surface(size)
	img.fill((55,255,55))
	img.convert()
	return img

def loadImg(imgFile, size):
	filename = "disp.jpg" 
	img=pygame.image.load(filename).convert()
	return img

def toHSV(RGB):
	r=float(RGB[0])
	g=float(RGB[1])
	b=float(RGB[2])
	minv=min(r,g,b)
	maxv=max(r,g,b)
	V=maxv
	d=max(1,maxv-minv)
	if maxv != 0:
		S=d/maxv
	else:
		S=0
		H=-1
		return (H,S,V)
	if r == maxv:
		H=(g-b)/d
	elif g == maxv:
		H=2+(b-r)/d
	else:
		H=4+(r-g)/d
	H *= 60
	if H < 0:
		H += 360
	return (H,S,V)

def toRGB(HSV):
	H=float(HSV[0])
	S=float(HSV[1])
	V=float(HSV[2])
	if S == 0 :
		R=G=B=V
		return (R,G,B)
	H/=60
	i =math.floor(H)
	f =H-i
	p =V*(1-S)
	q =V*(1-S*f)
	t =V*(1-S*(1-f))
	if i == 0:
		R=V
		G=t
		B=p
	elif i == 1:
		R=q
		G=V
		B=p
	elif i == 2:
		R=p
		G=V
		B=t
	elif i == 3:
		R=q
		G=p
		B=V
	elif i == 4:
		R=t
		G=p
		B=V
	else:
		R=V
		G=p
		B=q
	return (R,G,B)

def MM(val, mn, mx):
	val=min(mx, max(mn, val ))
	return val
	
def todeg(rad):
	rad=float(rad*(180/pi))
	return rad
	
def torad(deg):
	deg=float(deg*(pi/180))
	return deg

def updateScreen(surf, th):
	global threadCount
	global w	
	screen.blit(surf,(int((w/threadCount)*th),0))
	pygame.display.flip()

def psin(rate,mult,off,ittr):
	out=float(rate)
	#if(ittr>0):
	#		math=math+psin(math,mult,off,ittr-1)
	#else:
	#	math=(math.sin(math*mult+off)*.5+.5)*ittr
	
	for x in range(ittr):
		out=(math.sin(float(rate)*mult*ittr+float(off)+math.cos(float(ittr+float(off)) ))*.5+.5)
	return out

def kalido(arr, div, mk):
	x=arr[0]
	y=arr[1]
	if mk == 0:
		x=abs(x-w/2)/div
		y=abs(y-h/2)/div
	elif mk == 1:
		x=float(arr[0])
		y=float(arr[1])
		cx=float(arr[2])
		cy=float(arr[3])
		a=float(arr[4])
		s=math.sin(a)
		c=math.cos(a)
		editx=x-cx
		edity=y-cy
		#norm=math.sqrt((editx*editx) + (edity*edity))
		#norm = 1 if norm == 0 else norm
		#editx=editx/norm
		#edity=edity/norm
		editx=editx*c+edity*s
		edity=-editx*s+edity*c
		x=int(editx+cx)
		y=int(edity+cy)
	else:
		x=abs(x-w/2)/div
		y=abs(y-h/2)/div
	return (x,y)

def pAnimate(pmode):
    run=0
    if len(particles)>0:
		if pmode ==0:
			for p in particles:
				run+=1
				mather=p.x-w/2+1 
				if mather == 0:
					mather=1
				p.x=p.sx+int(math.sin(run/32-23)*(mather/abs(mather))*10*p.vx)
				p.y=p.sy+int(math.sin(run/2+223)*8*p.vy)
				#if (runner+run)%5 == 0:
				#    #p.scale=1-(p.age/10)
				p.radius=max(0, 5-p.age)
		elif pmode==1:
			for p in particles:
				run+=1
				mather=p.x-w/2+1 
				if mather == 0:
					mather=1
				p.x=p.sx+int(math.sin(run/32-23)*(mather/abs(mather))*10*p.vx)
				p.y=p.sy+int(math.sin(run/2+223)*8*p.vy)
				#if (runner+run)%5 == 0:
				#    #p.scale=1-(p.age/10)
				p.radius=max(0, 5-p.age)

		else:
			for p in particles:
				run+=1
				mather=p.x-w/2+1 
				if mather == 0:
					mather=1
				p.x=p.sx+int(math.sin(run/32-23)*(mather/abs(mather))*10*p.vx)
				p.y=p.sy+int(math.sin(run/2+223)*8*p.vy)
				#if (runner+run)%5 == 0:
				#    #p.scale=1-(p.age/10)
				p.radius=max(0, 5-p.age)
		pygame.display.flip()

def pxProcess(surf, th):
	global mode
	global curMode
	global verbObj
	global setMode
	global trans
	global modeChange
	global threadCount
	fr=float(runner)
	
	
	surf=pygame.transform.scale(surf, surfSize)
	pix=pygame.surfarray.pixels3d(surf)
	run=0
	hit=0
	tot=w/threadCount*h
	mode=list(mode)	
	
	if argvMode != None:
		mode=[argvMode,argvMode]
		blend=1
	
	mmCheck=[1,0]
	pp = 1
	r=g=b=0
	
	for x in range(0,len(pix),1):#maxThread):
		checkQuit()
		for y in range(len(pix[x])):
			if 1:#(run+runner)%3 == 0 :
				fx=float(x)
				fy=float(y)
				blend=1-min(1, max(0, (math.sin(fr/15.23*math.sin(fx/20.0-fr/82+13.23)*5+123+min(1,max(0,math.sin(fx/8.0+fr/40.5+fy/43.0)*7+.5))+min(1,max(0,math.sin(-fy/10.0+fx/30.0+(fr)/90.5)*15+.5)))+math.sin(fr/60+244)*7+.5)*5+.5))
				#blend=MM(math.sin(fr/20)*2+.5,0,1)
				mmCheck[0]=min(mmCheck[0], blend)
				mmCheck[1]=max(mmCheck[1], blend)


				rgb=[0,0,0]
				temprgb=[0,0,0]

				runMode=0
				if runMode in mode and ( (runMode == mode[0] and blend == 0) or (runMode == mode[1] and blend == 1) or (blend > 0 and blend < 1)):
					xy=kalido((fx,fy),6,0)
					fx=xy[0]
					fy=xy[1]
					rgb=rgbMode((0,fy,fr), 1)
					#if(x==0):
					#	rgb=rgbMode((fx,fy,fr), 1)
					#else:
					#	rgb=pix[0][y]
					rgb=list(toHSV(rgb))
					rgb[0]=(rgb[0]+fr*3.0+fy*5.0)%360
					rgb=toRGB(rgb)
					modeVal[runMode]=rgb
					hit=1
				runMode=1
				#rgb=rgb+rgbNoiseWave(rgb,(fx,fy,fr), 1, float(1-blend))
				if runMode in mode and ( (runMode == mode[0] and blend == 0) or (runMode == mode[1] and blend == 1) or (blend > 0 and blend < 1)):
					xy=kalido((float(x),float(y)), 4, 0)
					fx=xy[0]
					fy=xy[1]
					rgb=rgbNoiseWave(rgb,(fx,fy,fr), 1)
					modeVal[runMode]=rgb
					hit=1
				runMode=2
				if runMode in mode and ( (runMode == mode[0] and blend == 0) or (runMode == mode[1] and blend == 1) or (blend > 0 and blend < 1)):
					#readx=todeg(math.sin(abs(x-sw/2)))
					#ready=todeg(math.cos(abs(y-sh/2)))
					#ang=(math.sin(abs(float(x)-float(sw)/2))/math.cos(abs(float(y)-float(sh)/2)))
					ang=torad(fr/4.24)
					fx=abs(float(x)-float(sw)/2)
					fy=abs(float(y)-float(sh)/2)
					#fx=float(x)
					#fy=float(y)
					try:
						ang*=(fx-(sw/2))/abs(fx-(sw/2))
					except:
						pass;
					try:
						ang*=(fy-(sh/2))/abs(fy-(sh/2))
					except:
						pass;
					xy=kalido((fx,fy, (float(sw)), (float(sh)), ang+math.sin(fx/231.53+fy/142.3+fr/440.0)*2.3 ),2,1)
					
					scaler=35.0/float(scale)
					fx=float(xy[0])/scaler#float(x)
					fy=float(xy[1])/scaler#float(x)
					rgb=rgbKaleido((fx,fy,fr), 1)
					modeVal[runMode]=rgb
					hit=1
				runMode=3
				if runMode in mode and ( (runMode == mode[0] and blend == 0) or (runMode == mode[1] and blend == 1) or (blend > 0 and blend < 1)):
					#readx=todeg(math.sin(abs(x-sw/2)))
					#ready=todeg(math.cos(abs(y-sh/2)))
					#ang=todeg(math.sin(abs(float(x)-float(sw)/2))/math.cos(abs(float(y)-float(sh)/2)))
					ang=math.sin(fr/40+math.sin(float(x)/200)*pi-math.cos(float(y)/200)*pi)
					#fy=float(y)*(abs(float(y)-float(sh)/2)*math.sin(float(runner)/33))
					xy=kalido((float(x),float(y)+50.0, (float(sw)), (float(sh)), ang ),0,1)
					
					scaler=20.0/float(scale)
					fx=float(xy[0])/scaler#float(x)
					fy=float(xy[1])/scaler#float(x)
					gen=0
					if random.random()>.6 and (runner+run)%10==0:
						gen=1
					rgb=rgbSpray((fx,fy,fr),gen, 1)
					modeVal[runMode]=rgb
					hit=1
				runMode=4
				if runMode in mode and ( (runMode == mode[0] and blend == 0) or (runMode == mode[1] and blend == 1) or (blend > 0 and blend < 1)):
					#readx=todeg(math.sin(abs(x-sw/2)))
					#ready=todeg(math.cos(abs(y-sh/2)))
					#ang=todeg(math.sin(abs(float(x)-float(sw)/2))/math.cos(abs(float(y)-float(sh)/2)))
					
					scaler=40.0/float(scale)
					ang=math.sin(fr/130.0+math.sin(float(x)/450.0+fr/230)*pi-math.cos(float(y)/200.0)*pi)
					#fy=float(y)*(abs(float(y)-float(sh)/2)*math.sin(float(runner)/33))
					xy=kalido((float(x),float(y), (float(sw)), (float(sh)), ang ),0,1)
					fx=float(xy[0])/scaler#float(x)
					fy=float(xy[1])/scaler#float(x)
					
					"""
					ang=torad(fr/4.24)
					fx=abs(fx-float(sw)/2)
					fy=abs(fx-float(sh)/2)
					#fx=float(x)
					#fy=float(y)
					try:
						ang*=(fx-(sw/2))/abs(fx-(sw/2))
					except:
						pass;
					try:
						ang*=(fy-(sh/2))/abs(fy-(sh/2))
					except:
						pass;
					xy=kalido((fx,fy, (float(sw)), (float(sh)), ang+math.sin(fr/440.0)*2.3 ),2,1)
					fx=float(xy[0])
					fy=float(xy[1])
					"""
					
					gen=0
					if random.random()>.6 and (runner+run)%10==0:
						gen=1
					rgb=rgbRoll((fx,fy,fr),gen, 1)
					rgb=list(toHSV(rgb))
					rgb[0]=(rgb[0]+fr*5.0+fy*5.0+math.sin(fx/2.0+fr/3)*pi*2)%360
					rgb=toRGB(rgb)

					modeVal[runMode]=rgb
					hit=1
				
				runMode=5
				if runMode in mode and ( (runMode == mode[0] and blend == 0) or (runMode == mode[1] and blend == 1) or (blend > 0 and blend < 1)):

					scaler=20.0/float(scale)
					fx=fx/scaler
					fy=fy/scaler
					ang=torad(fr/20.24+math.cos(fx/7.4)*10.4)
					fx=abs(float(x)-float(sw)/2)
					fy=abs(float(y)-float(sh)/2)
					try:
						ang*=(fx-(sw/2))/abs(fx-(sw/2))*-1
					except:
						pass;
					try:
						ang*=(fy-(sh/2))/abs(fy-(sh/2))*-1
					except:
						pass;
					fx=fx/scaler
					fy=fy/scaler
					xy=kalido((fx,fy, (float(sw)), (float(sh)), ang/2),2,1)
					
					fx=float(xy[0])/scaler#float(x)
					fy=float(xy[1])/scaler#float(x)
					rgb=rgbKaleido((fx,fy,fr), 1)
					rgb=list(toHSV(rgb))
					rgb[0]=(rgb[0]-math.sin(fr/242.0+fr/5543.3)*58.0+math.cos(fy/224.0+fr/530.24)*58+fr/40.0)%360
					rgb=toRGB(rgb)
					modeVal[runMode]=rgb
					hit=1
				runMode=6
				if runMode in mode and ( (runMode == mode[0] and blend == 0) or (runMode == mode[1] and blend == 1) or (blend > 0 and blend < 1)):

					scaler=20.0/float(scale)
					fx=fx/scaler
					fy=fy/scaler
					ang=torad(fr/20.24+math.cos(fx/7.4)*10.4)
					fx=abs(float(x)-float(sw)/2)
					fy=abs(float(y)-float(sh)/2)
					#try:
					#	ang*=(fx-(sw/2))/abs(fx-(sw/2))*-1
					#except:
					#	pass;
					#try:
					#	ang*=(fy-(sh/2))/abs(fy-(sh/2))*-1
					#except:
					#	pass;
					try:
						mather=math.sin(fx/20.0+fr/5.3)/abs(math.sin(fx/20.0+fr/5.3))
					except:
						mather=1
					fx=abs((fx+math.sin(fx/35.0+fr/15)*3.3+fr)/scaler*mather)
					#fx=fx/scaler
					fy=fy/scaler
					xy=kalido((fx,fy, (float(sw)), (float(sh)), ang/2),2,1)
					
					fx=float(xy[0])/scaler#float(x)
					fy=float(xy[1])/scaler#float(x)
					rgb=rgbKaleido((fx,fy,fr), 1)
					rgb=list(toHSV(rgb))
					rgb[0]=(rgb[0]+fx-math.sin(fr/142.0+fr/553.3)*58.0+math.cos(fy/124.0+fr/530.24)*58+fr/40.0)%360
					rgb=toRGB(rgb)
					modeVal[runMode]=rgb
					hit=1

				#--------------------------------
				if hit == 0:
					if(x==0):
						rgb=rgbMode((fx,fy,fr), 1)
					else:
						rgb=(pix[0][y][0],pix[0][y][1],pix[0][y][2])
					if blend==0:
						modeVal[mode[1]]=rgb
					if blend==1:
						modeVal[mode[0]]=rgb
				if blend > 0 and blend < 1:
					#rgb=(rgb[0]*(blend)+temprgb[0]*(1-blend),rgb[1]*(blend)+temprgb[1]*(1-blend),rgb[2]*(blend)+temprgb[2]*(1-blend))
					rgb=(modeVal[mode[0]][0]*(1-blend)+modeVal[mode[1]][0]*blend,modeVal[mode[0]][1]*(1-blend)+modeVal[mode[1]][1]*blend,modeVal[mode[0]][2]*(1-blend)+modeVal[mode[1]][2]*blend)
				
				r=int(MM(rgb[0], 0, 255))
				g=int(MM(rgb[1], 0, 255))
				b=int(MM(rgb[2], 0, 255))
				pix[x][y][0]=r
				pix[x][y][1]=g
				pix[x][y][2]=b
			else:
				pix[x][y][0]=r
				pix[x][y][1]=g
				pix[x][y][2]=b
			run+=1
	if ( (mmCheck[0] == 1 and mmCheck[1] == 1) or (mmCheck[0] == 0 and mmCheck[1] == 0) ):
		trans=0
		if setMode==1 :
			if mmCheck[0] == 1:
				modeChange=0
			else:
				modeChange=1
	else:
		setMode=1
		trans=1
		modeChange=-1

	retQuit=0
	if setMode == 1 and modeChange != -1:
		setMode=0
		mode=list(mode)
		mode[modeChange]=(min(int(random.random()*(maxMode+1)),maxMode))
		if mode[modeChange] == mode[int(1-modeChange)]:
			while True:
				run+=1
				random.seed(run)
				val=min(int(random.random()*(maxMode+1)),maxMode)
				if val != mode[int(1-modeChange)]:
					mode[modeChange]=val
					break
				checkQuit()
		
	if verbose == 1:
		addVerbObj("mode", (str(mode[1])+" - "+str(mode[0])) )
		#addVerbObj("curMode", curMode)
		#addVerbObj("blend", blend)
		addVerbObj("trans", trans)
		addVerbObj("setMode", setMode)
		addVerbObj("modeChange", modeChange)
		#addVerbObj("modeVal", modeVal)

	#surf=pygame.transform.scale(surf,(w/threadCount,h))
	surf=pygame.transform.smoothscale(surf,(w/threadCount,h))
	updateScreen(surf,th)
	del [pix, r, g, b]
	return 1

def rgbMode(pos, active):
	if active == 1 :
		r=((psin(pos[2]/91.213+pos[0]/540,4,float(pos[0]/631-math.sin(pos[2]/30+pos[1])*5),4))*.5+.5)*255
		g=((psin(-pos[2]/51.213+pos[1]/140,3,float(pos[0]/431-math.sin(pos[2]/30+pos[1])*5),5))*.5+.5)*255
		b=(math.sin(math.sin(pos[0]/122)*.2+.5-pos[2]/113)*math.sin(pos[2]/31-pos[1]/22*math.sin(pos[0]/3+pos[1]/2+pos[2]/33)))*255
		r=min(255, max(1, r*((math.sin(pos[2]/213+pos[1]/24)*.7+.5) )))
		g=min(255, max(1, g*((math.sin(pos[2]/332+pos[0]/43)*.7+.5)*(math.sin(pos[2]/260)+.5) )))
		b=((psin(-pos[2]/51.213+pos[1]/240,3,float(pos[0]/231-math.sin(pos[2]/30+pos[1])*5),3))*.5+.5)*255
		return (r,g,b)
	else:
		return (0,0,0)
	
def rgbNoiseWave(rgb, pos, active):
	if active == 1 :
		fr=pos[2]
		fx=pos[0]
		fy=pos[1]
		r=rgb[0]
		g=rgb[1]
		b=rgb[2]
		tempr=(math.sin(fr/30+fx+math.cos(math.cos(fr/15.415+fy/52.5246)*3.9 ))*.5+.5)*255;
		tempg=(math.cos(fr/20+fy/tempr+math.cos(math.sin(fr/9.525+fx/51.356)/1.3 + psin(fr/31.213+fy,math.sin(fr/23+fx)*10+20,float(fx-fy/2.24),3) ))*.5+.5)*255;
		tempb=(math.cos(fr/20+fy/tempr+math.cos(math.sin(fr/9.525+fx/51.356)/1.3 + psin(fr/31.213+fy,math.sin(fr/23+fx)*10+20,float(fx-fy/2.24),3) ))*.5+.5)*255;
		
		#tempb=(psin(fr/31.213+fx/21,2,float(fx/23-fy),3)*math.cos(fr/47.142*(tempg/255)+(math.cos(-fy/10.52)*math.sin(fr*.3+tempr+tempg/2+fx)*(r/255)*math.sin(fr*.3+r)*math.sin(fx*1.235+tempg/23)*2)*1.4)+1)*127.5
		#r=min(255, max(0, r*(math.sin(fr/21)*.7+.5) ))
		#g=min(255, max(0, g*(math.sin(fr/19)*.7+.5) ))
		#b=min(255, max(0, b=g*(math.sin(fr/24+123)*.7+.5) ))
		r=min(255,max(0,tempr*(math.sin(fr/21+fx-fy/2+math.sin(fr/2-fx/10) )*.5+.5)+psin(fr/31.213,math.sin(fr/23), float(fr/10.23+123), 1)*2 ))
		g=min(255,max(0,tempg*(math.sin(-fr/19+233+fy/2+fx*1.5-math.sin(fr/2+fx)*3)*.5+.5)+psin(fr/31.213,math.sin(fr/23), float(fr/14.23), 1)*2 ))
		b=min(255,max(0,tempb*(math.sin(-fr/19+233+fy/2+fx*1.5-math.sin(fr/5+fx)*3)*.5+.5)+psin(fr/31.213,math.sin(fr/23), float(fr/14.23), 1)*2 ))
		#b=min(255, max(0,tempb*(math.sin(fr/234+123+fy/12+fx/24+math.sin(fr/22-fy+324)*5)*.5+.5)-psin(fr/31.213,math.sin(fr/20), float(fx/20.23), 1)*2 ))
		return (r,g,b)
	else:
		return (0,0,0)

def rgbKaleido( pos,active):
	if active == 1 :
		fr=pos[2]
		fx=float(pos[0])
		fy=float(pos[1])
		tempr=(math.sin(fr/30.0+234.23+fx/2.342+math.cos(math.cos(fr/15.415+fy/5.5246+234.2) ))*.5+.5)*255;
		tempg=(math.cos(fr/25.0+63.526+fy/3.32+math.cos(fx*2.0+fr/12.0)*pi+math.sin(fx/5.356+24.3)*1.3 )*.5+.5)*255;
		tempb=(math.cos(fr/20.0+43.23+fy/2.0+math.cos(math.sin(fr/19.525+fx/1.356+52.3)*1.3  ))*.5+.5)*255;

	
		blender=MM(math.sin(fr/31.3-fx/24.3+math.sin(fx/132.5+fr/542.3)*pi)*.7+.5, 0,1)
		tempr=tempr*blender+tempg*(1-blender)
		blender=MM(math.cos(fr/61.3+34.23+fy/54.3+math.cos(fy/132.5+fr/342.3-234.23)*pi)*.7+.5, 0,1)
		tempb=tempg*blender+tempb*(1-blender)

		r=tempr
		g=tempg
		b=tempb
		return (r,g,b)
	else:
		return (0,0,0)

def rgbSpray( pos, gen, active):
	if active == 1 :
		fr=pos[2]/100
		fx=float(pos[0])
		fy=float(pos[1])
		
		tempr=(math.sin(fr/30+fx/23.3+math.cos(math.sin(fr/15.415+fy/52.5246)*5.9 ))*.5+.5)*255;
		tempg=(math.cos(fr/20+fy*math.sin(fx*20+fr/2.0)+math.cos(math.sin(fx/51.356)*6.3 ))*.5+.5)*255;
		tempb=(math.cos(fr/20+fy/322+math.cos(math.sin(fr/9.525+fx/51.356)/1.3  ))*.5+.5)*255;

		r=tempr
		g=tempg
		b=tempb
		return (r,g,b)
		"""
		rgb=(tempr,tempg,tempb)
		scaler=math.sin(float(runner)*5.1442345)*(1-(fy/float(h)-.5))
		#(runner)%5==0 and 
		if  (b>100 or g>100) and random.random()*scaler>.6:
			random.seed(r)
			mr=random.random()*.5+1.5
			random.seed(g)
			mg=random.random()*.5+1.5
			random.seed(b)
			mb=random.random()*.5+1.5
			emitter(1, int(fx*scale),int(fy*scale), (tempr*mr,tempg*mg,tempb*mb), 7,1)
			#emitter(2,int(fx*scale),int(fy*scale),(r,g,b),5,1,1)
		#return (rgb[0], rgb[1], rgb[2])
		"""
	else:
		return (0,0,0)

def rgbRoll( pos, gen, active):
	if active == 1 :
		fr=pos[2]
		fx=float(pos[0])
		fy=float(pos[1])
		
		tempr=(math.sin(fr/120.0+fx/23.3+math.sin(fr/15.415+fy/52.5246)*5.9 )*.5+.5)*255;
		tempg=(math.cos(fr/330.0+fy/24.3*math.sin(fx*202.0+fr/233.3 ))*.5+.5)*255;
		tempb=(math.cos(fr/420.0+fy/322.0+math.cos(math.sin(fr/9.525+fx/51.356)/1.3  ))*.5+.5)*255;
		
		blender=MM(math.sin(fr/231.3+fx/24.3+math.cos(fx/52.5+fr/342.3)*pi)*.7+.3, 0,1)
		tempr=tempr*blender+tempg*(1-blender)

		r=tempr
		g=tempg
		b=tempb
		return (r,g,b)
	else:
		return (0,0,0)

def checkQuit():
	ret=0
	events=pygame.event.get()
	if len(events)>0:
		if events[0].type == pygame.KEYDOWN:
			if events[0].key == pygame.K_ESCAPE:
				pygame.display.quit()
				pygame.quit()
				sys.exit()

def snapshot():
	dir="/media/thumb/core-scripts/pxProcessing/imgSaves/"
	numb=str(runner-100).zfill(4)
	os.system("scrot "+dir+"snapshot"+str(numb)+".jpg")
	
def verbosePrint():
	curXY=[w,h]
	verbRev=verbObj[::-1]
	for x in verbRev:
		for obj in x.keys():
			val=x[obj]
			if("-" in obj):
				val="---------------------"
			else:
				val=str(obj)+" : "+str(val)
			text=pygame.font.SysFont("monospace", 15)
			label=text.render(val, 1, (255,255,255))
			vsize=list(pygame.Surface.get_size(label))
			pad=5
			screen.blit(label, (w-vsize[0]-pad,curXY[1]-vsize[1]-pad))
			curXY[1]=int(curXY[1]-vsize[1]-pad)
	pygame.display.flip()
	return None

def addVerbObj(title, val=None):
	global verbObj
	hit=0
	elNum=-1
	null=1 if title == "-" else 0
	for x in range(len(verbObj)):
		for key in verbObj[x].keys():
			if title in key:
				hit=1
				title=key
				elNum=x
				break;
	if hit == 0:
		elNumber=len(verbObj)
		verbObj.append({})
		title=str(title)
	verbObj[elNum][title]=str(val)

"""
def moveMouse():
	global mouse
	random.seed(mouse[0]+mouse[1])
	mpos=mouse+(random.random()*3, random.random()*3)
	theEvent = CGEventCreateMouseEvent(None, kCGEventMouseMoved, mpos, kCGMouseButtonLeft)
	CGEventPost(kCGHIDEventTap, theEvent)
	mouse=mpos
"""

try:
	x11 = ctypes.cdll.LoadLibrary('libX11.so')
	x11.XInitThreads()
except:
    pass

pygame.display.init()
pygame.font.init()
if fullScreen==0:
	screen = pygame.display.set_mode(screen, pygame.RESIZABLE)
else:
	screen = pygame.display.set_mode(screen, pygame.FULLSCREEN) 
c = pygame.time.Clock()
pygame.mouse.set_visible(0)
imgArray=[]
for t in range(threadCount):
	img=fill(screen.get_size())
	imgArray.append(img)
quitVal=0
while quitVal==0:
	runner+=1
	clock=pygame.time.Clock()
	runTime=pygame.time.get_ticks()
	##img=fill(screen.get_size())
	if threadCount>1:
		queuePool=Queue(2)
		qThreads=Pool(1,queueRun, (queuePool,imgArray,))
		for t in range(threadCount):
			queuePool.put(t)
		while not queuePool.empty():
			pass
		#for t in range(imgArray):
		#	updateScreen(imgArray[t],t)
	else:
		pxProcess(imgArray[0],0)
	#emitter()
	
	if verbose == 1:
		curTime=time.time()
		diff=str(float(int((1/(curTime-prevTime))*1000))/1000)
		prevTime=curTime
		addVerbObj("-",0)
		addVerbObj("FPS", diff)
		addVerbObj("runner", runner)
		addVerbObj("scale", scale)
		addVerbObj("screen", str(w)+", "+str(h))
		verbosePrint()
	if ssActive:
		if runner >= 800:
				pygame.quit()
				sys.exit()
		snapshot()

	clock.tick()
	#pygame.mouse.set_pos(random.random()*300,random.random()*300)
	#display.Display().screen().root.warp_pointer(300,300)
	display.Display().sync()
	checkQuit()

