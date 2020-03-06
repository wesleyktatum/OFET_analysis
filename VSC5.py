import wx

class topPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent, style = wx.BORDER_RAISED, size=(350,50))
        Test=wx.StaticText(self, -1, ("<Menu Icons>"))
        
        openFileDlgBtn = wx.Button(self,-1,"File", pos=(10,20))
        openFileDlgBtn.Bind(wx.EVT_BUTTON,self.onOpenFile)
        
    def onOpenFile(self,event):
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=self.currentDirectory, defaultFile="",wildcard=wildcard,style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
        dlg.Destroy()


        editFileDlgBtn = self.btn = wx.Button(self,-1,"Edit", pos=(110,20))
        self.btn = wx.Button(self,-1,"View", pos=(210,20))
        self.btn = wx.Button(self,-1,"Help", pos=(210,20))

class topLPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, style = wx.BORDER_RAISED, size=(350,450))
        Test=wx.StaticText(self, -1, ("<Include raw plot here>"))

class topRPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, style = wx.BORDER_RAISED,size=(350,450))
        Test=wx.StaticText(self, -1, ("<Results>")) 

class bottomPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, style = wx.BORDER_RAISED)
        Test=wx.StaticText(self, -1, ("<Buttons>"))
        self.btn = wx.Button(self,-1,"Calculate", pos=(110,20))
        self.btn = wx.Button(self,-1,"Save", pos=(210,20))
        self.btn = wx.Button(self,-1,"Reset", pos=(310,20))
        self.btn = wx.Button(self,-1,"Exit", pos=(310,20))


class MyFrame(wx.Frame):

    def __init__ (self, parent,id, title):
        wx.Frame.__init__(self, parent,id, title=title, size=(1200,650), pos=(100,100))
        
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Welcome to OFET transfer curve analysis!")

#Define a split window
        self.sp = wx.SplitterWindow(self)
        topP= topPanel(self)
        topPLeft = topLPanel(self.sp)
        topPRight = topRPanel(self.sp)
        bottomP = bottomPanel(self)
        

#split the window  
        

        self.sp.SplitVertically(topPLeft, topPRight)
        self.sp.SetMinimumPaneSize(350)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer.Add(topP, 1, wx.EXPAND)

        sizer.Add(self.sp,1,wx.EXPAND)
        
        sizer.Add(bottomP, 1, wx.EXPAND)

        self.SetSizer(sizer) 

        self.MenuBarUI()

#these are the menu bar items that can be trasffered to top menu panel

    def MenuBarUI(self):
        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()
        help = wx.Menu()

        file.Append(101, '&Open', 'Open a new document')
        file.Append(102, '&Save','Save the document')
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit','Quit the Application')
        file.AppendItem(quit)

        menubar.Append(file,'&file')
        menubar.Append(edit, '&Edit')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Transfer Curve Analysis using WxPYTHON")
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
