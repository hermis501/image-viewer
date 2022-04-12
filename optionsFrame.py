# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser
import wx
import functions

class OptionsFrame(wx.Frame): 
	def __init__(self, parent):
		self.parent=parent
		self.width, self.height = wx.GetDisplaySize()
		self.optionsFrame=wx.Frame.__init__(self, parent=self.parent, id=wx.ID_ANY, title="Image Viewer Options", pos = wx.DefaultPosition, size=(self.width, self.height), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		self.panel=wx.Panel(self, wx.ID_ANY)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.checkBox1=wx.CheckBox (self.panel, id=wx.ID_ANY, label="Read file descriptions automatically")
		self.checkBox1.SetValue (self.parent.autoSpeak)
		self.sizer.Add (self.checkBox1, 0, wx.ALL, 5)
		self.buttonOK=wx.Button (self.panel, label="OK", id=1)
		self.buttonOK.Bind (wx.EVT_BUTTON, self.onOk)
		self.sizer.Add (self.buttonOK)
		self.panel.SetSizerAndFit (self.sizer)
		self.panel.Layout ()
		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.parent.Hide ()

	def onClose (self, event=None):
		self.parent.Show ()
		self.Destroy ()

	def onOk (self, event):
		self.parent.autoSpeak=self.checkBox1.GetValue ()
		self.onClose ()
