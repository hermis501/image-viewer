# -*- coding: utf-8 -*-
import wx
import os
import _thread as thread
import urllib
import time
from urllib import request
import subprocess
import tempfile
tempDir=tempfile.gettempdir ()
app_path=os.getcwd() 

class updater (wx.Frame):
	def __init__(self):
		self.title="Image Viewer update"
		self.width, self.height = wx.GetDisplaySize()
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=self.title, pos = wx.DefaultPosition, size=(self.width, self.height), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		self.panel=wx.Panel(self, wx.ID_ANY)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.progress_e=wx.TextCtrl (self.panel, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_RICH|wx.TE_MULTILINE)
		# neccessary to use multiline in order to get focus on it
		self.progress_e.SetValue ("Downloading")
		self.sizer.Add (self.progress_e, flag=wx.EXPAND|wx.ALL)
		self.progress = wx.Gauge(self.panel, id=wx.ID_ANY, range=100, style=wx.GA_HORIZONTAL)
		self.sizer.Add (self.progress)
		self.panel.SetSizerAndFit (self.sizer)
		self.panel.Layout ()
		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.Show ()
		self.updating=True
		thread.start_new_thread(self.download,())

	def download (self):
		uplink="http://hermisk.eu/software/image_viewer-setup.exe"
		try: req=urllib.request.urlopen(uplink)
		except: return
		if 'Content-Length' not in req.headers: return
		fSize=int (req.headers['Content-Length'])
		outFile=open (os.path.join (tempDir, "image_viewer-setup.exe"), "wb")
		loop=fSize/1024
		loop=int (loop)
		loopMod=fSize % 1024
		percentage=0
		times=0
		for i in range (1, loop-1):
			if self.updating==False: 
				self.Destroy ()
				try: outFile.close (); os.remove (os.path.join (tempDir, "image_viewer-setup.exe")); self.Destroy (); return
				except: self.Destroy (); return
			temp=req.read (1024)
			if temp==None: wx.MessageBox (self, "Error", "Error downloading update"); self.Destroy (); return
			times=times+1024
			outFile.write (temp)
			percentage=times*100/fSize
			percentage=int(percentage)
			if percentage<0: percentage=0
			wx.CallAfter (self.progress.SetValue, percentage)
			wx.CallAfter (self.progress_e.SetValue, str(percentage)+"% "+"downloading")
		percentage=100
		wx.CallAfter (self.progress.SetValue, percentage)
		wx.CallAfter (self.progress_e.SetValue, str(percentage)+"% "+"downloading")
		if times!=fSize:
			temp=req.read ()
			outFile.write (temp)
		outFile.close ()
		subprocess.Popen ('imageviewerup.exe')
		self.Destroy ()

	def onClose (self, event=None): self.updating=False; self.Destroy ()

#function outside of the class
def get_versionSTR ():
	link="http://hermisk.eu/software/updates/imageviewer/upver.dat"
	content=urllib.request.urlopen(link, timeout=5).read ().decode ()
	if "<" in content: content=""
	return content
