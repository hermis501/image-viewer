import wx
import functions
import os
from pubsub import pub
class RenameGui(wx.Frame):
	def __init__(self, parent, arg):
		self.arg=arg
		self.parent=parent
		frm=wx.Frame.__init__(self, parent=None, title="Rename file", size=(350,200))
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.label1=wx.StaticText (self.panel, wx.ID_ANY, label="TimestampTXT")
		self.edit1=wx.TextCtrl (self.panel, wx.ID_ANY)
		self.label2=wx.StaticText (self.panel, wx.ID_ANY, label="Short description")
		self.edit2=wx.TextCtrl (self.panel, wx.ID_ANY)
		self.main_box.Add(self.label1, 0, wx.ALL, 10)
		self.main_box.Add(self.edit1, 0, wx.ALL, 10)
		self.main_box.Add(self.label2, 0, wx.ALL, 10)
		self.main_box.Add(self.edit2, 0, wx.ALL, 10)
		self.ok = wx.Button(self.panel, wx.ID_OK, "&OK")
		self.ok.SetDefault()
		self.ok.Bind(wx.EVT_BUTTON, self.onOK)
		self.main_box.Add(self.ok, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
		self.timestamp=functions.get_date_from_file (self.arg)
		self.edit1.SetValue (self.timestamp)
		self.parent.Hide ()

	def onOK (self, event):
		timestamp=self.edit1.GetValue ()
		description=self.edit2.GetValue ()
		if timestamp=="" or timestamp==None: wx.MessageBox ("Fields cannot be empty", "Error"); return
		if description=="" or description==None: wx.MessageBox ("Fields cannot be empty", "Error"); return
		filename=functions.stringToFileName (timestamp+"-"+description)
		if os.path.isfile (filename): wx.MessageBox ("File with this name already exists.", "Warning"); return
		self.renameFile (self.arg, filename)
		wx.MessageBox ("File has been renamed!", "Information")
		self.OnClose ()

	def OnClose(self, event=None):
		self.parent.Show ()
		self.Destroy()

	def renameFile (self, old, newName):
		temp=os.path.split (old)
		dir=temp[0]
		ext=functions.get_extension (old)
		new=dir+"\\"+newName+"."+ext
		os.rename (old, new)
		print ("file is renamed, now we are inside of the renamegui")
		self.parent.receiveText=str(new)
		pub.sendMessage("aaa", msg=0)
