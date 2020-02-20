import wx

class topPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent, style = wx.BORDER_RAISED, size=(350,50))
        Test=wx.StaticText(self, -1, ("<Menu Icons>"))
        self.btn = wx.Button(self,-1,"File", pos=(10,20))
        self.btn = wx.Button(self,-1,"Edit", pos=(110,20))
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
       
        self.btnInp = wx.Button(self,-1,"Input Values", pos=(110,20))
        self.btnInp.Bind(wx.EVT_BUTTON, self.OnButton)
       
        self.btnCal = wx.Button(self,-1,"Calculate", pos=(210,20))
       
        self.btnRes = wx.Button(self,-1,"Reset", pos=(310,20))
       
        self.btnExi = wx.Button(self,-1,"Exit", pos=(310,20))

    def OnButton(self,event):
        dlg = GetData(self)
        dlg.ShowModal()
        #if dlg.result_A:
         #   self.AppendText("A: "+dlg.result_A+"\n")
          #  self.AppendText("B: "+dlg.result_B+"\n")
           # self.AppendText("C: "+dlg.result_C+"\n")
        #else:
         #   self.AppendText("No Input found\n")
        dlg.EndModal(wx.ID_OK)

class GetData(wx.Dialog):
    def __init__(self, settings):
        wx.Dialog.__init__(self, settings, wx.ID_ANY, "Input Data", size=(650,220))
        
        self.settings = settings

        self.panel2=wx.Panel(self, wx.ID_ANY)

        self.Avalue = wx.StaticText(self.panel2, label="A value", pos=(20,20))
        self.A = wx.TextCtrl(self.panel2, value="", pos=(110,20), size=(500,-1))
        
        self.Bvalue = wx.StaticText(self.panel2, label="B value", pos=(20,60))
        self.B = wx.TextCtrl(self.panel2, value="", pos=(110,60), size=(500,-1))
        
        self.Cvalue = wx.StaticText(self.panel2, label="C value", pos=(20,100))
        self.C = wx.TextCtrl(self.panel2, value="", pos=(110,100), size=(500,-1))
        
        self.saveButton =wx.Button(self.panel2, label="Save", pos=(110,160))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        
        self.closeButton =wx.Button(self.panel2, label="Cancel", pos=(210,160))     
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        
        self.Show()

    def OnQuit(self, event):
        self.result_A = None
        self.EndModal(wx.ID_CANCEL)

    def SaveConnString(self, event):
        self.result_A = self.A.GetValue()
        self.result_B = self.B.GetValue()
        self.result_C = self.C.GetValue()

        self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings

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
        file.Append(quit)

        menubar.Append(file,'&file')
        menubar.Append(edit, '&Edit')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)


    def onSettings(self, e):
        settings_dialog = GetData(self.settings, self)
        res = settings_dialog.ShowModal()
        if res == wx.ID_OK:
            self.settings = settings_dialog.GetSettings()
        settings_dialog.Destroy()
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "Transfer Curve Analysis using WxPYTHON")
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
