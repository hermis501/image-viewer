import wx
class Menu():
	def __init__(self, parent):
		menu_file = wx.Menu()
		self.openMenu = menu_file.Append(-1, "Open folder with images\tCTRL+O", "Open folder with images")
		self.quitMenu = menu_file.Append(-1, "Quit the program", "Quit the program")
		parent.Bind (wx.EVT_MENU, parent.onOpen, self.openMenu)
		parent.Bind (wx.EVT_MENU, parent.onClose, self.quitMenu)

		menu_commands = wx.Menu()
		self.nextMenu = menu_commands.Append(-1, "Next image\tRIGHT", "Next image")
		parent.Bind (wx.EVT_MENU, parent.onNext, self.nextMenu)
		self.prevMenu = menu_commands.Append(-1, "Previous image\tLEFT", "Previous image")
		parent.Bind (wx.EVT_MENU, parent.onPrevious, self.prevMenu)
		self.descriptionMenu = menu_commands.Append(-1, "Get image description\tF4", "Get image description")
		parent.Bind (wx.EVT_MENU, parent.onDescription, self.descriptionMenu)
		self.descriptionCopyMenu = menu_commands.Append(-1, "Copy image description\tF5", "Copy image description")
		parent.Bind (wx.EVT_MENU, parent.onDescriptionCopy, self.descriptionCopyMenu)

		menu_options = wx.Menu()
		self.slideshowMenu = menu_options.Append(-1, "Slide show\tCTRL+S", "Slide show", kind=wx.ITEM_CHECK)
		self.slideshowMenu.Check (False)
		parent.Bind (wx.EVT_MENU, parent.onSlideshow, self.slideshowMenu)

		menu_help = wx.Menu()
		self.aboutMenu = menu_help.Append(-1, "About", "About the program")
		parent.Bind (wx.EVT_MENU, parent.onAbout, self.aboutMenu)
		menu_bar = wx.MenuBar()
		menu_bar.Append(menu_file, "&File")
		menu_bar.Append(menu_commands, "&Commands")
		menu_bar.Append(menu_options, "&Options")
		menu_bar.Append(menu_help, "&Help")
		parent.SetMenuBar(menu_bar)