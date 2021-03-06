# -*- coding: utf-8 -*-
import universal_speech as unispeech
from configparser import ConfigParser
from datetime import datetime
import cloudvis
import wx
from wx import locale
import menu as m
import functions
import sys
import os
import clipboard
import _thread as thread
from threading import Thread
import playsound
import pathlib

class mainWindow(wx.Frame): 
	def __init__(self, parent, title, kwg):
		self.fileName=""
		self.width, self.height = wx.GetDisplaySize()
		self.title=title
		self.parent=parent
		self.arg = kwg
		self.mainFrame=wx.Frame.__init__(self, parent=self.parent, id=wx.ID_ANY, title=self.title, pos = wx.DefaultPosition, size=(self.width, self.height), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		self.panel=wx.Panel(self, -1)
		self.sb=self.CreateStatusBar (1)
		self.sb.Show()
		self.show_status ("Waiting for images")
		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.panel.Bind (wx.EVT_HELP, self.onAbout)
		self.menu = m.Menu(self)

		#varebles
		self.pictures=None
		self.descriptions=None
		self.currentPicture = 0
		self.totalPictures = 0

		self.photoMaxSize = self.width-20
		self.img = wx.Image(self.width, self.height)
		# self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(self.img))
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY)
		self.imageCtrl.SetFocus ()
		self.Show ()
		self.timer = wx.Timer(self)
		self.Bind (wx.EVT_TIMER, self.onTimer, self.timer)
		self.process_path ()
		#configuration checking
		self.config=ConfigParser()
		self.config_ini="konfig.ini"
		self.config.read (self.config_ini)
		try: self.capture_dir=self.config.get("configuration", "capture_to")
		except: self.capture_dir=os.path.abspath(os.getcwd()); self.capture_dir=self.capture_dir+"\captures"
		self.capture_dir=pathlib.Path (self.capture_dir)
		#configuration checking end

	def process_path (self):
		if self.arg==None: return
		path=os.path.dirname (self.arg)
		name=os.path.basename (self.arg)
		self.pictures = functions.search_photos(path)
		self.totalPictures=self.pictures[0]
		self.descriptions=None
		self.descriptions=[None]*(self.totalPictures+1)
		self.descriptions[0]=self.totalPictures
		self.currentPicture=0
		for a in self.pictures:
			self.currentPicture=self.currentPicture+1
			if a==name: break
		self.loadImage (self.pictures[self.currentPicture])

	def onOpen (self, event):
		dlg=wx.DirDialog (self, "Open folder", "", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dlg.ShowModal ()==wx.ID_OK:
			path=dlg.GetPath ()
			# temppic = glob.glob(path + "\\*.jpg")
			temppic = functions.search_photos(path)
			if not temppic: temppic=None; wx.MessageBox ("There are no pictures in this folder", "Error"); return
			self.pictures=temppic
			self.totalPictures=self.pictures[0]
			self.descriptions=None
			self.descriptions=[None]*(self.totalPictures+1)
			self.descriptions[0]=self.totalPictures
			self.currentPicture=1
			self.loadImage (self.pictures[self.currentPicture])

	def loadImage (self, image):
		imageName = os.path.basename(image)
		img = wx.Image(image, wx.BITMAP_TYPE_ANY)
		W = img.GetWidth()
		H = img.GetHeight()
		if W > H:
			NewW = self.photoMaxSize
			NewH = self.photoMaxSize * H / W
		else:
			NewH = self.photoMaxSize
			NewW = self.photoMaxSize * W / H
		img = img.Scale(NewW,NewH)
		self.imageCtrl.SetSize (NewW, NewH)
		self.imageCtrl.SetBitmap(wx.Bitmap(img))
		self.imageCtrl.Refresh ()
		self.show_status (imageName+" "+str(self.currentPicture)+" / "+str(self.totalPictures))

	def onAbout (self, event):
		wx.MessageDialog(self, "Image viewer with accessibility features\nCopyright (C) 2020 by Hermis Kasperavičius\nThis program uses cloudVision API from http://visionbot.ru/apiv2 and Universal Speech API from http://github.com/qtnc/UniversalSpeech", "Accessible Image Viewer", wx.OK).ShowModal()

	def onClose (self, event):
		self.Destroy ()

	def show_status (self, text): self.sb.SetStatusText (text)

	def onTimer (self, event): self.nextPicture ()

	def onNext (self, event): self.nextPicture ()

	def onPrevious (self, event): self.previousPicture ()

	def previousPicture(self):
		if self.totalPictures==0: return
		if self.currentPicture == 1:
			self.currentPicture = self.totalPictures
		else:
			self.currentPicture -= 1
		self.loadImage (self.pictures[self.currentPicture])

	def nextPicture(self):
		if self.totalPictures==0: return
		if self.currentPicture == self.totalPictures:
			self.currentPicture = 1
		else:
			self.currentPicture += 1
		self.loadImage (self.pictures[self.currentPicture])

	def onDescription (self, event):
		# thread.start_new_thread(self.getDescription,())
		t = Thread(self.getDescription())
		t.start()

	def getDescription (self):
		if self.menu.slideshowMenu.IsChecked (): unispeech.output ("You must turn off slideshow feature in order to get descriptions. To do it, press control + s"); return
		if self.pictures==None: return
		# nekišti api užklausos antrąkart, jei descriptionas pasirinktai nuotraukai jau gautas
		if self.descriptions[self.currentPicture]!=None: unispeech.output (self.descriptions[self.currentPicture].replace ("\n", ", ")); return
		unispeech.output ("getting description.")
		param=self.pictures[self.currentPicture]
		cloud=cloudvis.cloudvis (param)
		self.descriptions[self.currentPicture]=cloud
		unispeech.output (self.descriptions[self.currentPicture].replace ("\n", ", "))

	def onDescriptionCopy (self, event):
		self.copyDescription ()

	def copyDescription (self):
		if (self.descriptions==None) or (self.descriptions[self.currentPicture]==None): unispeech.output ("nothing to copy. Please press f4 first to get description and then copy it"); return
		clipboard.copy (str(self.descriptions[self.currentPicture]))
		unispeech.output ("Copied")

	def onSlideshow (self, event):
		if self.menu.slideshowMenu.IsChecked (): self.timer.Start (3000); unispeech.output ("SlideShow, on")
		else: self.timer.Stop (); unispeech.output ("SlideShow, off")

if __name__ == '__main__':
	workingDir=os.path.abspath(os.getcwd())
	app = wx.App()
	localeObj = wx.Locale(wx.LANGUAGE_ENGLISH) # prevent translation of wx dialogs
	if len(sys.argv) > 1:
		path=sys.argv[1]
		path=functions.valid_arg (path)
		mainWindow(None, "Image Viewer", path)
	else:
		mainWindow(None, "Image Viewer", None)
	app.MainLoop()
