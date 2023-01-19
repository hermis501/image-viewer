# -*- coding: utf-8 -*-
import subprocess
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
from configparser import ConfigParser
import cloudvis
import wx
import renameGui
import descriptionGui
import updaterFrame
import optionsFrame
from wx import locale
import menu as m
import functions
import sys
import os
import os.path
import clipboard
import _thread as thread
from threading import Thread
import playsound
import pathlib

class mainWindow(wx.Frame): 
	def __init__(self, parent, title, kwg):
		#configuration checking
		self.config=ConfigParser()
		self.config_ini=os.path.join (settings_path, "config.ini")
		self.config.read (self.config_ini)
		try: self.autoSpeak=self.config.getboolean("configuration", "autospeak")
		except: self.autoSpeak=False
		#configuration checking end
		self.fileName=""
		self.width, self.height = wx.GetDisplaySize()
		self.title=title
		self.parent=parent
		self.arg = kwg
		self.mainFrame=wx.Frame.__init__(self, parent=self.parent, id=wx.ID_ANY, title=self.title, pos = wx.DefaultPosition, size=(self.width, self.height), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		self.panel=wx.Panel(self, -1)
		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.panel.Bind (wx.EVT_HELP, self.onAbout)
		self.menu = m.Menu(self)

		#varebles
		self.pictures=None
		self.descriptions=None
		self.descripting=False
		self.currentPicture = 0
		self.totalPictures = 0
		self.receiveText=""

		self.photoMaxSize = self.width-20
		self.img = wx.Image(self.width, self.height)
		# self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(self.img))
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY)
		self.imageCtrl.SetFocus ()
		self.Show ()
		self.timer = wx.Timer(self)
		self.Bind (wx.EVT_TIMER, self.onTimer, self.timer)
		self.status=""
		self.process_path ()

	def onSayStatus (self, event):
		if self.status!="": functions.speak (self.status)

	def process_path (self):
		if self.arg==None: return
		path=os.path.dirname (self.arg)
		name=os.path.basename (self.arg)
		self.pictures = functions.search_photos(path)
		self.totalPictures=self.pictures[0]
		self.descriptions=None
		self.descriptions=[None]*(self.totalPictures+1)
		self.descriptions[0]=self.totalPictures
		self.currentPicture=-1
		for a in self.pictures:
			self.currentPicture=self.currentPicture+1
			if a==self.arg: break
		self.loadImage (self.pictures[self.currentPicture])

	def onOpenFile (self, event):
		pass

	def onOpenFolder (self, event):
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
		self.img = wx.Image(image, wx.BITMAP_TYPE_ANY)
		W = self.img.GetWidth()
		H = self.img.GetHeight()
		if W > H:
			NewW = self.photoMaxSize
			NewH = self.photoMaxSize * H / W
		else:
			NewH = self.photoMaxSize
			NewW = self.photoMaxSize * W / H
		self.img = self.img.Scale(NewW,NewH)
		self.imageCtrl.SetSize (NewW, NewH)
		self.imageCtrl.SetBitmap(wx.Bitmap(self.img))
		self.imageCtrl.Refresh ()
		self.status= imageName+" "+str(self.currentPicture)+" / "+str(self.totalPictures)
		self.status=str(self.status)
		self.SetTitle ("%s - Image Viewer" %(self.status))

	def onAbout (self, event):
		wx.MessageDialog(self, program_nameAndVersion+"\n"+program_copyright+".\n"+program_description, "About Image Viewer", wx.OK).ShowModal()

	def onClose (self, event):
		# set proper configuration values and write to ini file
		if not self.config.has_section("configuration"): self.config.add_section ("configuration")
		self.config.set("configuration", "autospeak", str(self.autoSpeak))
		with open(self.config_ini, 'w') as config_file: self.config.write(config_file)
		self.Destroy ()

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
		if self.autoSpeak: 
			param=self.pictures[self.currentPicture]
			desc=functions.getImageDescription (param)
			if desc!="": functions.speak (desc)

	def nextPicture(self):
		if self.totalPictures==0: return
		if self.currentPicture == self.totalPictures:
			self.currentPicture = 1
		else:
			self.currentPicture += 1
		self.loadImage (self.pictures[self.currentPicture])
		if self.autoSpeak: 
			param=self.pictures[self.currentPicture]
			desc=functions.getImageDescription (param)
			if desc!="": functions.speak (desc)

	def onDescription (self, event):
		if self.descripting==True: functions.speak ("Please wait until the current process has finished"); return
		thread.start_new_thread(self.getDescription,())
		# t = Thread(self.getDescription())
		# t.start()

	def getDescription (self):
		if self.menu.slideshowMenu.IsChecked (): functions.speak ("You must turn off slideshow feature first to avoid possible conflicts"); return
		if self.pictures==None: return
		# nekišti api užklausos antrąkart, jei descriptionas pasirinktai nuotraukai jau gautas
		if self.descriptions[self.currentPicture]!=None: functions.speak (self.descriptions[self.currentPicture].replace ("\n", ", ")); return
		functions.speak ("getting description.")
		self.descripting=True
		cur=self.currentPicture
		param=self.pictures[cur]
		cloud=cloudvis.cloudvis (param)
		if cloud=="": functions.speak ("error while describing image"); self.descripting=False; return
		self.descriptions[cur]=cloud
		functions.speak (self.descriptions[self.currentPicture].replace ("\n", ", "))
		self.descripting=False

	def onDescriptionCopy (self, event):
		self.copyDescription ()

	def copyDescription (self):
		if (self.descriptions==None) or (self.descriptions[self.currentPicture]==None): functions.speak ("nothing to copy. Please press f4 first to get description and then copy it"); return
		clipboard.copy (str(self.descriptions[self.currentPicture]))
		functions.speak ("Copied")

	def onSlideshow (self, event):
		if self.menu.slideshowMenu.IsChecked (): self.timer.Start (3000); functions.speak ("SlideShow, on")
		else: self.timer.Stop (); functions.speak ("SlideShow, off")

	def onRename (self, event):
		if self.menu.slideshowMenu.IsChecked (): functions.speak ("You must turn off slideshow feature first to avoid possible conflicts"); return
		if self.pictures==None: functions.speak ("Nothing to rename"); return
		param=self.pictures[self.currentPicture]
		renameGui.RenameGui (self, param).Show ()

	def onWriteLongDescription (self, event):
		if self.menu.slideshowMenu.IsChecked (): functions.speak ("You must turn off slideshow feature first to avoid possible conflicts"); return
		if self.pictures==None: functions.speak ("No picture"); return
		param=self.pictures[self.currentPicture]
		descriptionGui.DescriptionGui (self, param).Show ()

	def onFileDescription (self, event):
		if self.menu.slideshowMenu.IsChecked (): functions.speak ("You must turn off slideshow feature first to avoid possible conflicts"); return
		if self.pictures==None: return
		param=self.pictures[self.currentPicture]
		desc=functions.getImageDescription (param)
		if desc=="": return
		functions.speak (desc)

	def onOptions (self, event):
		optionsFrame.OptionsFrame (self).Show ()

	def runProcess (name, args):
		subprocess.Popen (name, args, startupinfo=startupinfo)

	def onRenameMessage (self):
		if os.path.isfile (self.receiveText): self.pictures[self.currentPicture]=self.receiveText
		self.receiveText=""
		self.loadImage (self.pictures[self.currentPicture])

if __name__ == '__main__':
	# f=open("errors.log","w")
	# sys.stderr=f
	if getattr(sys, 'frozen', False):
		app_path = os.path.dirname(sys.executable)
	elif __file__:
		app_path = os.path.dirname(os.path.abspath(__file__))
	settings_path=functions.get_config_path()
	if not os.path.isdir (settings_path): os.mkdir (settings_path)
	program_name=os.path.basename(sys.executable)
	program_version="1.0.6"
	program_nameAndVersion="Image Viewer, Version %s" %(program_version)
	program_copyright="Copyright © 2020-2022 by Hermis Kasperavičius"
	program_description="Image Viewer for the blind.\nThis program uses Cloud Vision API from http://visionbot.ru/"
	app = wx.App(redirect=False)
	localeObj = wx.Locale(wx.LANGUAGE_ENGLISH) # prevent translation of wx dialogs
	up_version=""
	try: up_version=updaterFrame.get_versionSTR ()
	except Exception: up_version=""
	if "<" in up_version: up_version=""
	if up_version!="" and program_version!=up_version:
		question = wx.MessageDialog(None, "New version is available. Do you want to update now?", "Image Viewer", wx.YES_NO|wx.ICON_INFORMATION)
		status = question.ShowModal()
		if status == wx.ID_YES: updaterFrame.updater ()
		else: up_version=""
		question.Destroy()
	if program_version==up_version or up_version=="":
		if len(sys.argv) > 1:
			path=sys.argv[1]
			path=functions.valid_arg (path)
			mainWindow(None, "Image Viewer", path)
		else:
			mainWindow(None, "Image Viewer", None)
	app.MainLoop()