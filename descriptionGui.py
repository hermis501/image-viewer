import wx
import functions
class DescriptionGui(wx.Frame):
	def __init__(self, parent, arg):
		self.arg=arg
		self.parent=parent
		frm=wx.Frame.__init__(self, parent, title="Description for this image", size=(350,200))
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.label1=wx.StaticText (self.panel, wx.ID_ANY, label="Long description")
		self.edit1=wx.TextCtrl (self.panel, wx.ID_ANY, style=wx.HSCROLL|wx.TE_RICH|wx.TE_MULTILINE)
		self.main_box.Add(self.label1, 0, wx.ALL, 10)
		self.main_box.Add(self.edit1, 0, wx.ALL, 10)
		self.ok = wx.Button(self.panel, wx.ID_OK, "Save")
		# self.ok.SetDefault()
		self.ok.Bind(wx.EVT_BUTTON, self.onOK)
		self.main_box.Add(self.ok, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
		desc=functions.getImageDescription (self.arg)
		self.edit1.SetValue (desc)
		self.parent.Hide ()

	def onOK (self, event):
		text=self.edit1.GetValue ()
		text=str (text)
		if text=="":
			question = wx.MessageDialog(self, "Would you like to remove description from image?", "Image Viewer", wx.YES_NO|wx.ICON_INFORMATION)
			status = question.ShowModal()
			question.Destroy()
			if status == wx.ID_YES: functions.delImageDescription (self.arg); wx.MessageDialog(self, "Description has been removed.", "Done", wx.OK).ShowModal(); self.OnClose ()
		else:
			functions.setImageDescription (self.arg, text)
			wx.MessageDialog(self, "Description has been saved.", "Done", wx.OK).ShowModal()
			self.OnClose ()

	def OnClose(self, event=None):
		self.parent.Show ()
		self.Destroy()
