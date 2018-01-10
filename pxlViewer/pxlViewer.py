############################################
## pxlViewer v0.0.4                       ##
## Image Viewer                           ##
##  Written by Kevin Edzenga; ~2017       ##
##   http://Metal-Asylum.net              ##
##                                        ##
## For aditional work, see my github-     ##
##  https://github.com/procstack          ##
############################################
"""
 
 Stay awesome and open source for life!
 
"""

import zlib
import bz2

import sys, os
from cv2 import *
import numpy as np
from PIL import Image
from PyQt4 import QtGui, QtCore, QtWebKit
from functools import partial
import binascii
import math

frozen=0
if getattr(sys, 'frozen', False):
	frozen=1
	bundleDir=sys._MEIPASS
else:
	bundleDir=os.path.dirname(os.path.abspath(__file__))

curDir=os.getcwd()

viewVersion="v0.0.4"

# Fork the python session and close the parent session
# Keep terminal active for later usage
pid=os.fork()
if pid == 0:
	os.setsid()
else:
	exit()

class ImageProcessor(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(ImageProcessor,self).__init__(parent)
		global viewVersion
		global sW
		global sH
		scriptNameText="pxlViewer"
		versionText=scriptNameText+" - "+str(viewVersion)
		self.setWindowTitle(versionText)
		self.winSize=[720,405]
		self.setMinimumSize(self.winSize[0],self.winSize[1])
		self.resize(self.winSize[0],self.winSize[1])
		#self.setStyleSheet("padding:0px;")	
		
		self.move((sW-self.winSize[0])/2,(sH-self.winSize[1])/2);
		
		self.websiteName=""
		self.websiteSettingsFile=""
		self.galleryName=""
		self.galleryPath=""
		self.curEntryObj=-1
		self.dirImageList={}
		self.loadIndexList=[]
		self.loadScrollList=[]
		self.scrollIndexVal=0
		self.scrollIndexHeight=-1
		self.mainWidget=QtGui.QWidget(self)
		
		
		self.imgFullPerc=50
		self.imgFullTilePerc=5
		self.imgMedPerc=25
		self.imgThumbPerc=10
		self.imgQualityPerc=50
		
		
		#roles
		# Disabled, Active, Inactive, Normal
		
		self.setWindowStyleSheet()
		"""
		### Menu Bar ###
		self.menuBar=self.menuBar()
		fileMenu=self.menuBar.addMenu('File')
		loadItem=QtGui.QAction("Load Optimized Site",self)
		fileMenu.addAction(loadItem)
		fileMenu.addSeparator()
		saveItem=QtGui.QAction("Save",self)
		fileMenu.addAction(saveItem)
		saveAsItem=QtGui.QAction("Save As...",self)
		fileMenu.addAction(saveAsItem)
		fileMenu.addSeparator()
		quitItem=QtGui.QAction("Exit",self)
		quitItem.triggered.connect(self.quitApp)
		fileMenu.addAction(quitItem)
		self.infoMenu=self.menuBar.addMenu('Info')
		infoItem=QtGui.QAction(scriptNameText+" Info",self)
		self.infoMenu.addAction(infoItem)
		self.infoMenu.addSeparator()
		helpItem=QtGui.QAction("Help...",self)
		#helpItem.hovered.connect(self.setCursorPointing)
		self.infoMenu.addAction(helpItem)
		# Status Bar
		#self.statusBar=self.statusBar()
		"""
		self.mainLayout=QtGui.QVBoxLayout(self.mainWidget)
		pad=0
		self.mainLayout.setSpacing(pad)
		self.mainLayout.setMargin(pad)
		selfSize=self.geometry()
		#menuSize=self.menuBar.geometry()
		selfSize=[selfSize.width(), selfSize.height()]#-menuSize.height()]

		#tabBlock=QtGui.QTabWidget()
		#tabBlock.resize(selfSize[0], selfSize[1])
		#tab0=QtGui.QWidget()
		#tab1=QtGui.QWidget()
		#tab2=QtGui.QWidget()
		#tabBlock.addTab(tab0,"Site Images")
		#tabBlock.addTab(tab1,"Site Code")
		#tabBlock.addTab(tab2,"Image Gallery")
		#self.mainLayout.addWidget(tabBlock)
		
		# Load directory text field
		self.imageDisplayBlock=QtGui.QVBoxLayout()
		self.imgField=QtGui.QLabel()
		self.imgField.setText("Please select the folder containing\n your full sized images.")
		self.imgField.setAlignment(QtCore.Qt.AlignCenter)
		self.imageDisplayBlock.addWidget(self.imgField)
		self.imgSpacer=QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.imageDisplayBlock.addItem(self.imgSpacer)
		#tab0.addLayout(self.imageDisplayBlock)
		self.mainLayout.addLayout(self.imageDisplayBlock)
		

		self.setCentralWidget(self.mainWidget)

		## GUI COMPLETE ##

		# Load image
		self.loadAndScanDir(curDir+"/"+sys.argv[-1])
	def setCursorPointing(self):
		QtGui.QWidget.setCursor(self.infoMenu,QtCore.Qt.PointingHandCursor)
	def setCursorArrow(self):
		QtGui.QWidget.setCursor(self.infoMenu,QtCore.Qt.ArrowCursor)
	def setWindowStyleSheet(self):
		self.winPalette=QtGui.QPalette()
		self.winPalette.setColor(QtGui.QPalette().Window, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Base, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Background, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Button, QtGui.QColor(60,60,60))
		self.winPalette.setColor(QtGui.QPalette().ToolTipBase, QtGui.QColor(20,20,20))
		self.winPalette.setColor(QtGui.QPalette().AlternateBase, QtGui.QColor(50,50,50))
		self.winPalette.setColor(QtGui.QPalette().Highlight, QtGui.QColor(80,80,80))
		self.winPalette.setColor(QtGui.QPalette().WindowText, QtGui.QColor(200,200,200))
		self.winPalette.setColor(QtGui.QPalette().ButtonText, QtGui.QColor(200,200,200))
		self.winPalette.setColor(QtGui.QPalette().ToolTipText, QtGui.QColor(200,200,200))
		self.winPalette.setColor(QtGui.QPalette().BrightText, QtGui.QColor(255,255,255))
		self.winPalette.setColor(QtGui.QPalette().HighlightedText, QtGui.QColor(80,80,80))
		self.winPalette.setColor(QtGui.QPalette().Link, QtGui.QColor(100,100,200))
		self.winPalette.setColor(QtGui.QPalette().Dark, QtGui.QColor(32,32,32))
		self.winPalette.setColor(QtGui.QPalette().Light, QtGui.QColor(32,32,32))
		#self.winPalette.setCurrentColorGroup(QtGui.QPalette.Normal)
		
		self.setPalette(self.winPalette)
		QtGui.QApplication.setPalette(self.winPalette)
		styleSheetCss="""
		QToolTip {color:#ffffff;background-color:#202020;border: 1px solid #ffffff;}
		QPushButton {color:#ffffff;background-color:#202020;padding:4px;border:1px solid #303030;}
		QLineEdit {color:#ffffff;background-color:#909090;padding:2px;border:1px solid #202020;}
		QScrollArea {color:#ffffff;background-color:#808080;border:1px solid #202020;}
		QAction {color:#ffffff;background-color:#808080;border:1px solid #202020;}
		QMenuBar {color:#ffffff;background-color:#606060;border:1px solid #202020;}
		QMenuBar::item {color:#ffffff;background-color:#707070;padding:2px;border:1px solid #505050;}
		QMenu {color:#ffffff;background-color:#707070;border:1px solid #404040;}
		QMenu::item {color:#ffffff;background-color:#707070;padding:2px;}
		QMenu::item:selected {color:#ffffff;background-color:#9c9c9c;padding:2px;}
		QSlider {background-color:#323232;}
		QScrollBar:vertical {width:10px;color:#ffffff;background-color:#808080;border:1px solid #202020;}
		QStatusBar {color:#ffffff;background-color:#606060;border:1px solid #202020;}"""
		self.setStyleSheet(styleSheetCss)
	def loadAndScanDir(self, imagePath):
		if imagePath != "":
			extList=["jpg","jpeg","gif","png"]
			activeList=[]
			if os.path.isdir(imagePath):
				#Don't think this is working
				
				imageName=imagePath.split("/")[-1]
				imagePath="/".join(imagePath.split("/")[:-1])
				#self.galleryName=imagePath.split("/")[-1]
				#self.galleryPath=imagePath
				imgList=os.listdir(imagePath)
				for x in imgList:
					curExt=x.split(".")[-1]
					if curExt.lower() in extList:
						activeList.append(x)
			else:
				curExt=imagePath.split(".")[-1]
				imageName=imagePath.split("/")[-1]
				imagePath="/".join(imagePath.split("/")[:-1])
				if curExt.lower() in extList:
					activeList.append(imageName)
					
			self.clearLayout(self.imageDisplayBlock)
			
			if len(activeList) == 0:
				extListStr=""
				for x in extList:
					extListStr+=str(x)+", "
				extListStr=extListStr[0:-2]
				fBold=QtGui.QFont()
				fBold.setBold(True)
				
				tmpBlock=QtGui.QVBoxLayout()
				tmpText=QtGui.QLabel()
				tmpText.setText("No usable images found in-")
				tmpBlock.addWidget(tmpText)
				tmpText=QtGui.QLabel()
				tmpText.setText(imagePath)
				tmpText.setAlignment(QtCore.Qt.AlignCenter)
				tmpText.setFont(fBold)
				tmpBlock.addWidget(tmpText)
				self.imageDisplayBlock.addWidget(self.imgField)
				self.imgSpacer=QtGui.QSpacerItem(20,10,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
				tmpBlock.addItem(self.imgSpacer)
				tmpText=QtGui.QLabel()
				tmpText.setText("Please use a folder containing images using extentions-")
				tmpBlock.addWidget(tmpText)
				tmpText=QtGui.QLabel()
				tmpText.setText(extListStr)
				tmpText.setAlignment(QtCore.Qt.AlignCenter)
				tmpText.setFont(fBold)
				tmpBlock.addWidget(tmpText)
				imgSpacer=QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
				tmpBlock.addItem(imgSpacer)
				#self.imageDisplayBlock.addLayout(tmpBlock)
				"""
				imagePath=QtGui.QFileDialog(self,"Full Image Directory", "directory", filter)
				imagePath.setFileMode(QtGui.QFileDialog.DirectoryOnly)
				#imagePath.setSidebarUrls([QtCore.QUrl.fromLocalFile(place)])
				if imagePath.exec_() == QtGui.QDialog.Accepted:
					self.fullDir=imagePath.selectedFiles()[0]
					print self.fullDir
				
				
				dialog = QtGui.QFileDialog(self, 'Audio Files', directory, filter)
				dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
				dialog.setSidebarUrls([QtCore.QUrl.fromLocalFile(place)])
				if dialog.exec_() == QtGui.QDialog.Accepted:
					self._audio_file = dialog.selectedFiles()[0]
				"""
			else:
				
				sizeSub=100
				pad=5
				
				entryBlock=QtGui.QHBoxLayout()
				entryEditBlock=QtGui.QVBoxLayout()
				
				##### ENTRY EDITED IMAGE DISPLAY #####
				
				curEntryEditScrollBlock=QtGui.QScrollArea()
				curEntryEditScrollBlock.setWidgetResizable(True)
				curEntryEditScrollBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				curEntryEditScrollInner=QtGui.QWidget(curEntryEditScrollBlock)

				self.curEntryBlock=QtGui.QVBoxLayout()
				self.curEntryBlock.setAlignment(QtCore.Qt.AlignCenter)
				curEntryEditScrollInner.setLayout(self.curEntryBlock)
				self.curEntryBlock.setSpacing(pad)
				self.curEntryBlock.setMargin(pad)
				tmpEntry=QtGui.QLabel()
				tmpEntry.setText("Placeholder")
				tmpEntry.setAlignment(QtCore.Qt.AlignCenter)
				self.curEntryBlock.addWidget(tmpEntry)
				
				
				curEntryEditScrollBlock.setWidget(curEntryEditScrollInner)
				entryEditBlock.addWidget(curEntryEditScrollBlock)
				
				
				
				#curEntryEditScrollInner.addLayout(self.curEntryBlock)
				#curEntryEditScrollBlock.setWidget(curEntryEditScrollInner)
				#entryEditBlock.addWidget(curEntryEditScrollBlock)
				
				
				##### ENTRY EDIT PARAMETERS #####
				self.curImageSettings=QtGui.QVBoxLayout()
				
				entryEditBlock.addLayout(self.curImageSettings)
				entryBlock.addLayout(entryEditBlock)
				
				##### ENTRY INDEX LIST ######
				
				self.scrollIndexBlock=QtGui.QScrollArea()
				self.scrollIndexBlock.setWidgetResizable(True)
				self.scrollIndexBlock.setMaximumWidth(150)
				self.scrollIndexBlock.verticalScrollBar().valueChanged.connect(self.updateScrollIndex)
				self.scrollIndexBlock.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				scrollInner=QtGui.QWidget(self.scrollIndexBlock)
				
				
				self.curImgListBlock=QtGui.QVBoxLayout(scrollInner)
				self.curImgListBlock.setAlignment(QtCore.Qt.AlignCenter)
				scrollInner.setLayout(self.curImgListBlock)
				self.curImgListBlock.setSpacing(pad)
				self.curImgListBlock.setMargin(pad)
				size=self.scrollIndexBlock.frameGeometry()
				#size=[size.width()-sizeSub, size.height()]
				size=[100, size.height()]
				scrollOffset=0
				scrollAdd=0
				self.loadIndexList=[]
				self.loadScrollList=[]
				loadObj=-1
				for x,p in enumerate(activeList):
					scrollOffset+=scrollAdd+pad
					
					#IndexImageEntry(parent, index, name, path, scaleSize)
					curImg=IndexImageEntry(self,x,p,imagePath+"/",size)
					self.curImgListBlock.addWidget(curImg)
					curImg.offset=scrollOffset
					self.loadIndexList.append(curImg)
					self.loadScrollList.append([])
					self.loadScrollList[-1].append(scrollOffset)
					self.loadScrollList[-1].append(scrollOffset+curImg.imgSizeIndexList[1])
					scrollAdd=curImg.imgSizeIndexList[1]
					if loadObj==-1:
						loadObj=curImg
				self.scrollIndexBlock.setWidget(scrollInner)
				#entryBlock.addWidget(self.scrollIndexBlock)
				self.imageDisplayBlock.addLayout(entryBlock)
				self.updateScrollIndex()
				self.loadImageEntry(loadObj)
	def setOutputDir(self):
		folderPicker=QtGui.QFileDialog.getExistingDirectory(self,"Set Output Directory")
		if folderPicker != "":
			self.outDirField.setText(folderPicker)
	def updateScrollIndex(self):
		self.scrollIndexVal=self.scrollIndexBlock.verticalScrollBar().value()
		self.scrollIndexHeight=self.scrollIndexBlock.size().height()
		if len(self.loadScrollList) > 0:
			minCheck=self.scrollIndexVal-self.scrollIndexHeight*.5
			maxCheck=self.scrollIndexVal+self.scrollIndexHeight*1.5
			popList=[]
			for x,i in enumerate(self.loadScrollList):
				if i[0] < maxCheck and i[1] > minCheck:
					self.loadIndexList[x].loadImage()
					popList.append(x)
			if len(popList) > 0:
				for p in range(len(popList)): # Delete backwards to no delete the wrong index, since everything falls back 1 on delete
					rp=len(popList)-1-p
					del self.loadIndexList[rp]
					del self.loadScrollList[rp]
	def loadImageEntry(self,obj):
		self.clearLayout(self.curImageSettings)
		
		### SETTINGS ###
		self.curEntryObj=obj # Still don't know if this dupelicates the object in memory, hahah
		imgFull=obj.imgSizeFull
		#self.imgFullPerc=obj.imgSizeFull
		#self.imgFullTilePerc=obj.imgSizeFullTile
		#self.imgMedPerc=obj.imgSizeMed
		#self.imgThumbPerc=obj.imgSizeThumb

		### MAIN ENTRY ###
		self.clearLayout(self.curEntryBlock)
		
		### WebView Image Viwer ###
		self.editViewWindow=EntryViewer(self,obj)
		self.curEntryBlock.addWidget(self.editViewWindow)
		self.curEntryBlock.setSpacing(0)
		self.curEntryBlock.setMargin(0)
		pol=QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.editViewWindow.setSizePolicy(pol)
		"""
		### Sliders and Jazz ###
		### Full ###
		curImageFullSettings=QtGui.QHBoxLayout()
		fullSizeText=QtGui.QLabel()
		fullSizeText.setText("Full Size -")
		fullSizeText.setMinimumWidth(150)
		#fullSizeText.setAlignment(QtCore.Qt.AlignCenter)
		curImageFullSettings.addWidget(fullSizeText)
		
		self.sliderFull=QtGui.QSlider()
		self.sliderFull.setOrientation(QtCore.Qt.Horizontal)
		self.sliderFull.setMinimum(.01)
		self.sliderFull.setMaximum(100)
		curVal=self.imgFullPerc
		self.sliderFull.setValue(curVal)
		curImageFullSettings.addWidget(self.sliderFull)
		# Tile value
		# self.imgFullTilePerc
		
		self.fullSizeVal=QtGui.QLabel()
		self.fullSizeVal.setText(str(imgFull[0]*curVal/100)+"x"+str(imgFull[1]*curVal/100))
		self.fullSizeVal.setMinimumWidth(90)
		self.fullSizeVal.setAlignment(QtCore.Qt.AlignRight)
		curImageFullSettings.addWidget(self.fullSizeVal)
		
		self.curImageSettings.addLayout(curImageFullSettings)
		self.sliderFull.valueChanged.connect(partial(self.sliderPercChange,0))
		# 1 will be full sized tile scales
		#self.sliderFull.valueChanged.connect(self.sliderPercChange(1))
		
		### Medium ###
		curImageMedSettings=QtGui.QHBoxLayout()
		medSizeText=QtGui.QLabel()
		medSizeText.setText("Medium Size -")
		medSizeText.setMinimumWidth(150)
		#medSizeText.setAlignment(QtCore.Qt.AlignRight)
		curImageMedSettings.addWidget(medSizeText)
		
		self.sliderMed=QtGui.QSlider()
		self.sliderMed.setOrientation(QtCore.Qt.Horizontal)
		self.sliderMed.setMinimum(.01)
		self.sliderMed.setMaximum(100)
		curVal=self.imgMedPerc
		self.sliderMed.setValue(curVal)
		curImageMedSettings.addWidget(self.sliderMed)
		
		self.medSizeVal=QtGui.QLabel()
		self.medSizeVal.setText(str(imgFull[0]*curVal/100)+"x"+str(imgFull[1]*curVal/100))
		self.medSizeVal.setMinimumWidth(90)
		self.medSizeVal.setAlignment(QtCore.Qt.AlignRight)
		curImageMedSettings.addWidget(self.medSizeVal)
		self.curImageSettings.addLayout(curImageMedSettings)
		self.sliderMed.valueChanged.connect(partial(self.sliderPercChange,2))
		
		curImageThumbSettings=QtGui.QHBoxLayout()
		thumbSizeText=QtGui.QLabel()
		thumbSizeText.setText("Thumbnail Size -")
		thumbSizeText.setMinimumWidth(150)
		#thumbSizeText.setAlignment(QtCore.Qt.AlignCenter)
		curImageThumbSettings.addWidget(thumbSizeText)
		
		self.sliderThumb=QtGui.QSlider()
		self.sliderThumb.setOrientation(QtCore.Qt.Horizontal)
		self.sliderThumb.setMinimum(.01)
		self.sliderThumb.setMaximum(100)
		curVal=self.imgThumbPerc
		self.sliderThumb.setValue(curVal)
		curImageThumbSettings.addWidget(self.sliderThumb)
		
		self.thumbSizeVal=QtGui.QLabel()
		self.thumbSizeVal.setText(str(imgFull[0]*curVal/100)+"x"+str(imgFull[1]*curVal/100))	
		self.thumbSizeVal.setMinimumWidth(90)
		self.thumbSizeVal.setAlignment(QtCore.Qt.AlignRight)
		curImageThumbSettings.addWidget(self.thumbSizeVal)
		self.curImageSettings.addLayout(curImageThumbSettings)
		self.sliderThumb.valueChanged.connect(partial(self.sliderPercChange,3))
		
		### Compression Settings ###
		
		curQualitySettings=QtGui.QHBoxLayout()
		qualityText=QtGui.QLabel()
		qualityText.setText("Quality -")
		qualityText.setMinimumWidth(100)
		#thumbSizeText.setAlignment(QtCore.Qt.AlignCenter)
		curQualitySettings.addWidget(qualityText)
		
		self.sliderQuality=QtGui.QSlider()
		self.sliderQuality.setOrientation(QtCore.Qt.Horizontal)
		self.sliderQuality.setMinimum(1)
		self.sliderQuality.setMaximum(100)
		curVal=50
		self.sliderQuality.setValue(curVal)
		curQualitySettings.addWidget(self.sliderQuality)
		
		self.qualityVal=QtGui.QLabel()
		self.qualityVal.setText(str(curVal)+"%")	
		self.qualityVal.setMinimumWidth(90)
		self.qualityVal.setAlignment(QtCore.Qt.AlignRight)
		curQualitySettings.addWidget(self.qualityVal)
		self.curImageSettings.addLayout(curQualitySettings)
		self.sliderQuality.valueChanged.connect(partial(self.sliderPercChange,4))
		###
		"""
	def updateGalleryVariables(self):
		self.galleryName=self.globalGalleryName.text()
	def sliderPercChange(self, updateSlider):
		imgSize=self.curEntryObj.imgSizeFull
		if updateSlider==4:
			val=self.sliderQuality.value()
			self.imgQualityPerc=val
			sliderValText=self.qualityVal
			sliderValText.setText(str(val)+"%")
		else:
			if updateSlider==0: # Full size image
				val=self.sliderFull.value()
				self.imgFullPerc=val
				sliderValText=self.fullSizeVal
			elif updateSlider==1: # Full Tile size
				self.imgFullTilePerc
				return None
			elif updateSlider==2: # Medium size
				val=self.sliderMed.value()
				self.imgMedPerc=val
				sliderValText=self.medSizeVal
			elif updateSlider==3: # Thumb size
				val=self.sliderThumb.value()
				self.imgThumbPerc=val
				sliderValText=self.thumbSizeVal
			sliderValText.setText(str(imgSize[0]*val/100)+"x"+str(imgSize[1]*val/100))
	def clearLayout(self, layout):
		children=[]
		postRemoveItem=[]
		for l in range(layout.count()):
			if type(layout.itemAt(l)) in [QtGui.QHBoxLayout, QtGui.QVBoxLayout]:
				self.clearLayout(layout.itemAt(l)) # Recurse through sub layouts
				children.append(layout.itemAt(l))
			else:
				typ=type(layout.itemAt(l))
				if typ == QtGui.QWidgetItem:
					layout.itemAt(l).widget().close()
				if typ == QtGui.QSpacerItem: # Spacers, I need to find a better way to remove
					postRemoveItem.append(layout.itemAt(l))
		if len(postRemoveItem) > 0: # Removing spacers in the loop will skip widgets after that point in the array
			for i in postRemoveItem: # So delete them after the fact
				layout.removeItem(i)
	"""
	def mousePressEvent(self, e):
		print "click"
	def mouseReleaseEvent(self, e):
		print "release"
	def mouseMoveEvent(self, e):
		print "move"
	"""
	def keyPressEvent(self, e):
		if e.key()==QtCore.Qt.Key_Escape:
			self.quitApp()
	def progressBar(self,init):
		if init == -1:
			val=0
		elif init == -2:
			val=0
		elif init >= 0:
			val=0
		return None
			
	def processImage(self):
		compressorPath= bundleDir+"/compressor.py"
		with open(compressorPath, 'r') as f:
			fread=f.read()
		exec(fread)
		patternRecognition(self,self.curEntryObj,self.editViewWindow)

	def processSite(self):
		self.writeGalleryIndexFile(self)
	def writeGalleryIndexFile(self):
		maxEntryListPerVar=300
		outDir=self.galleryName
		outFile="galIndex.php"
		curImgCount=0
		curVarCount=0
		out="""
		<?php
		$dispGalTitle=1;
		"""
		for x,i in enumerate(self.loadIndexList):
			curImgCount=x
			if curImgCount%maxEntryListPerVar == 0:
				curVarCount+=1
				out+="$imageGalleryData"+str(curVarCount)+"=array( \n"
			#$imageGalleryData1=array( 
			#'thumbs/IMAG1028_BURST011_th.jpg' => array('full/IMAG1028_BURST011.jpg','mid/IMAG1028_BURST011_mid.jpg','5197753','5376','3024','2','width="5376" height="3024"','width:5376;height:3024', 'IMAG1028_BURST011.jpg'),
			with open(outFile, 'w') as f:
				f.write(out)
				
	def resizeEvent(self, e):
		return None
	def quitApp(self):
		QtGui.qApp.quit()
class IndexImageEntry(QtGui.QWidget): #Individual indexList image entries
	def __init__(self, parent, index, name, path, scaleSize):
		super(IndexImageEntry,self).__init__(parent)
		self.parent=parent
		self.offset=0 # Offset from 0 scroll in indexList side bar
		self.imgName=name
		self.imgFolder=path
		self.imgPath=path+name # Path to image on disk
		self.loaded=0 # Current state, reading from disk, keeps ram usage and load time lower
		
		self.imgSize=[-1,-1] # Disk image size
		self.imgSizeFull=[-1,-1] # Full size image for web
		self.imgSizeFullTile=[-1,-1] # Tile array sizes for web, [x1,y1, x2,y2, x3,y3, ... xn,yn]
		self.imgSizeMed=[-1,-1] # Medium size image for web
		self.imgSizeThumb=[-1,-1] # Thumb size for web
		self.imgSizeIndexList=[-1,-1] # Size of indexList image in qt window
		
		curImgBlock=QtGui.QVBoxLayout()
		curImgBlock.setSpacing(0) # Spacing & Margin was giving me trouble calculating dynamic loading in window
		curImgBlock.setMargin(0) # ||
		self.img=QtGui.QLabel()
		
		# Using PyQt's Pixmap is great for displaying image, but really slow just for reading basic info
		# Since loading an image into a Pixmap loads the image into memory.
		# Using PIL.Image reads the fist 16 characters of the image to retrieve size info
		# TLDR; SO MUCH FASTER THROUGH PIL!!1!
		imageStats=Image.open(str(self.imgPath)) # PIL.Image
		
		self.imgSize=[imageStats.size[0], imageStats.size[1]] # Disk image size
		self.imgSizeFull=self.imgSize # Full size image for web
		
		self.imgSizeIndexList=[imageStats.size[0],imageStats.size[1]]
		ratio=1
		if scaleSize[0] < imageStats.size[0]: # If the full image is larger than scrollArea
			ratio=float(scaleSize[0])/float(imageStats.size[0])
			ymath=float(imageStats.size[1])*ratio
			self.imgSizeIndexList=[int(scaleSize[0]), int(ymath)] # Store indexThumbnail scale for scroll offset math & placeholder
			
		self.img.setText("Loading - "+str(self.imgPath.split("/")[-1])+"\n"+str(ratio)[0:5]+"% - [ "+str(self.imgSizeIndexList[0])+" x "+str(self.imgSizeIndexList[1])+" ]") # Stand-in for image, pre load
		self.img.setAlignment(QtCore.Qt.AlignCenter)
		self.img.setGeometry(0,0,self.imgSizeIndexList[0],self.imgSizeIndexList[1]) # Placeholder
		curImgBlock.addWidget(self.img)
		# Child QWidgets don't set parent size, must set parent size for correct scroll bar
		self.setFixedSize(self.imgSizeIndexList[0],self.imgSizeIndexList[1]) # Layout size for Placeholder
		self.setLayout(curImgBlock) # Layout to display in parent window

	def loadImage(self):
		pmap=QtGui.QPixmap()
		pmap.load(self.imgPath) #Load image, currently disk path only
		# I feel this is too limiting, encase I change how height is calculated in the future
		#pmap=pmap.scaledToWidth(scaleSize[0])
		pmap=pmap.scaled(self.imgSizeIndexList[0],self.imgSizeIndexList[1])
		self.img.setPixmap(pmap)
	"""
	def mousePressEvent(self, e):
		#print self.imgPath
		return None
	"""
	def mouseReleaseEvent(self, e):
		self.parent.loadImageEntry(self)
	"""def mouseMoveEvent(self, e):
		#print self.imgPath
		return None
	"""
class EntryViewer(QtWebKit.QWebView):	
	def __init__(self, win, entryObj):
		QtWebKit.QWebView.__init__(self)
		global bundleDir
		self.entry=entryObj
		self.win=win
		self.offset=[]
		self.mouseDown=0
		self.mouseDrag=0
		self.verbose=0
		if sys.argv[1] in ["-s", "-sandbox","-sand","-v","-verb", "-verbose", "-d", "-debug"]:
			self.verbose=1
		self.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
		self.settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(bundleDir+"/style.css"))
		if self.verbose:
			self.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
		entryText=self.entry.imgName+" - "+str(self.entry.imgSize[0])+"x"+str(self.entry.imgSize[1])
		
		with open(bundleDir+'/index.htm', 'r') as htmlOpen:
			editEntryHtml=htmlOpen.read()
		self.src=editEntryHtml.format(bdir=bundleDir,relPath=self.entry.imgName,bltext=entryText,imgWidth=str(self.entry.imgSize[0]),imgHeight=str(self.entry.imgSize[1]))
		self.setHtml(self.src,baseUrl=QtCore.QUrl().fromLocalFile(self.entry.imgFolder))

		self.page().mainFrame().addToJavaScriptWindowObject("opWin",self)
        
	def setImage(self,img,w,h):
		super(EntryViewer,self).page().mainFrame().evaluateJavaScript("setEntryImage('"+str(img)+"',"+str(w)+","+str(h)+");");
	def setText(self,text):
		super(EntryViewer,self).page().mainFrame().evaluateJavaScript("setEntryText('"+str(text)+"');");
	def updateVariable(self,var,val):
		super(EntryViewer,self).page().mainFrame().evaluateJavaScript(str(var)+"="+str(val)+";");
	def runCommand(self,cmd):
		super(EntryViewer,self).page().mainFrame().evaluateJavaScript(cmd+";");
	def keyPressEvent(self, e):
		if e.key()==QtCore.Qt.Key_Escape:
			self.win.quitApp()
		elif e.key()==QtCore.Qt.Key_Backspace:	
			#self.back()
			return None
		elif e.key()==QtCore.Qt.Key_Return:	
			#frame=self.page().currentFrame()
			#frame.evaluateJavaScript("launchURL()");
			return None
		else:
			return None
		#self.mouseDown=0
		#self.mouseUp=0
		#self.mouseDrag=0
		
	def mousePressEvent(self, e):
		self.offset=e.pos()
		self.mouseDown=e.button()
		self.updateVariable("mouseX",self.offset.x())
		self.updateVariable("mouseY",self.offset.y())
		self.updateVariable("origMouseX",self.offset.x())
		self.updateVariable("origMouseY",self.offset.y())
		#super(EntryViewer,self).page().mainFrame().evaluateJavaScript("writeEntryText('[ "+str(self.offset.x())+", "+str(self.offset.y())+" ]');");
	def mouseReleaseEvent(self, e):
		self.mouseDown=0
		super(EntryViewer,self).page().mainFrame().evaluateJavaScript("endDrag();dragging=0;");
		self.updateVariable("dragCount",0)
		self.updateVariable("mButton",-1)
	def mouseMoveEvent(self, e):
		if type(self.offset)!=QtCore.QPoint:
			self.offset=e.pos();
		if self.mouseDown>0:
			self.offset=e.pos();
			self.updateVariable("mouseX",self.offset.x())
			self.updateVariable("mouseY",self.offset.y())
			self.updateVariable("dragging",1)
			self.updateVariable("mButton",self.mouseDown)
			if self.mouseDrag==0:
				super(EntryViewer,self).page().mainFrame().evaluateJavaScript("startDrag();");
			super(EntryViewer,self).page().mainFrame().evaluateJavaScript("doDrag(0);");
			self.mouseDrag+=1
		else:
			self.mouseDrag=0
	@QtCore.pyqtSlot(str)
	def varValue(self, varArray):
		print varArray
	@QtCore.pyqtSlot(str)
	def showMessage(self, message):
		if message == "loaded":
			if self.verbose==0:
				self.runCommand("noContextMenu()")
		else:
			print message
if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	screen=app.desktop().screenGeometry()
	sW=screen.width()
	sH=screen.height()
	galGen=ImageProcessor()
	galGen.show()
	try:
		sys.exit(app.exec_())
	except:
		pass;
