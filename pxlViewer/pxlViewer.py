############################################
## pxlViewer v0.0.5                       ##
## Image Viewer                           ##
##  Written by Kevin Edzenga; ~2017       ##
##   http://Metal-Asylum.net              ##
##                                        ##
## For aditional work, see my github-     ##
##  https://github.com/procstack          ##
############################################

"""
 Learning should be a shared experiance
"""

scriptNameText="pxlViewer"
viewVersion="v0.0.5"

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

verbose=0
if sys.argv[1] in ["-v","-verb", "-verbose"]:
	verbose=1
	
if verbose == 0:
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
		global scriptNameText
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
		
		
		self.mainLayout=QtGui.QVBoxLayout(self.mainWidget)
		pad=0
		self.mainLayout.setSpacing(pad)
		self.mainLayout.setMargin(pad)
		selfSize=self.geometry()
		#menuSize=self.menuBar.geometry()
		selfSize=[selfSize.width(), selfSize.height()]#-menuSize.height()]
		
		# Load directory text field
		self.imageDisplayBlock=QtGui.QVBoxLayout()
		self.imgField=QtGui.QLabel()
		self.imgField.setText("[: Something didn't load right :]\n[: Cause this is an error in python, not javascript... :]")
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
	def menuBarVis(self,tgl):
		if tgl == 1:
			### Menu Bar ###
			try:
				self.menuBar=self.menuBar()
				fileMenu=self.menuBar.addMenu('File')
				#saveAsItem=QtGui.QAction("Save As...",self)
				#fileMenu.addAction(saveAsItem)
				#fileMenu.addSeparator()
				#infoItem=QtGui.QAction("Info",self)
				#infoItem.triggered.connect(partial(self.menuCommand, "toggleInfoWindow"))
				#fileMenu.addAction(infoItem)
				#fileMenu.addSeparator()
				quitItem=QtGui.QAction("Exit",self)
				quitItem.triggered.connect(self.quitApp)
				fileMenu.addAction(quitItem)
				#self.infoMenu.addAction(infoItem)
				#self.infoMenu.addSeparator()
				#helpItem=QtGui.QAction("Help...",self)
				#helpItem.hovered.connect(self.setCursorPointing)
				#self.infoMenu.addAction(helpItem)
				# Status Bar
				#self.statusBar=self.statusBar()
			except:
				self.menuBar.setVisible(1);
		else:
			self.menuBar.setVisible(0);
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
		QMenuBar {color:#ffffff;background-color:#303030;border:1px solid #202020;}
		QMenuBar::item {color:#ffffff;background-color:#404040;padding:2px;border:1px solid #202020;}
		QMenu {color:#ffffff;background-color:#505050;border:1px solid #282828;}
		QMenu::item {color:#ffffff;background-color:#505050;padding:2px;}
		QMenu::item:selected {color:#ffffff;background-color:#6c6c6c;padding:2px;}
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

		### MAIN ENTRY ###
		self.clearLayout(self.curEntryBlock)
		
		### WebView Image Viwer ###
		self.editViewWindow=EntryViewer(self,obj)
		self.curEntryBlock.addWidget(self.editViewWindow)
		self.curEntryBlock.setSpacing(0)
		self.curEntryBlock.setMargin(0)
		pol=QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.editViewWindow.setSizePolicy(pol)
	def menuCommand(self, cmd):
		self.editViewWindow.runCommand(cmd)
	def updateGalleryVariables(self):
		self.galleryName=self.globalGalleryName.text()
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
		global verbose
		if verbose:
			print e
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
		self.menuVis=0
		if sys.argv[1] in ["-v","-verb", "-verbose", "-d", "-debug"]:
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
		elif message == "toggleMenuBarVis":
			self.menuVis=(self.menuVis+1)%2
			self.win.menuBarVis(self.menuVis)
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
