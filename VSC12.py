import wx

class MainWindow(wx.Frame):
    
    def __init__ (self, parent,id, title):
        wx.Frame.__init__(self, None ,wx.ID_ANY, title=title, size=(1200,650), pos=(100,100))
        self.Centre()

        #Defining status bar
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Welcome to OFET transfer curve analysis!")

        #These are the buttons at top of the frame for Menu Icons
        self.btn = wx.Button(self,-1,"File", pos=(20,20))
        self.btn = wx.Button(self,-1,"Edit", pos=(120,20))
        self.btn = wx.Button(self,-1,"View", pos=(220,20))
        self.btn = wx.Button(self,-1,"Help", pos=(320,20))

        #Drawing line to seperate Menu Icons area from the graphing area
        wx.StaticLine(self, pos=(1, 50), size=(1200,10))
        #Drawing line to seperate graphing area from settings icons
        wx.StaticLine(self, pos=(1, 530), size=(1200,10))
        

        #These are the buttons at bottoms of the frame for other functions
        self.btnInp = wx.Button(self,-1,"Input Values", pos=(400,560))
        self.btnCal = wx.Button(self,-1,"Calculate", pos=(500,560))
        self.btnRes = wx.Button(self,-1,"Reset", pos=(600,560))
        self.btnExi = wx.Button(self,-1,"Exit", pos=(700,560))

        #creating boundary from input graph and graph result
        self.rawgraph = wx.StaticBox(self, label='<Input Graph>', pos=(20, 70), size=(560, 460))
        self. finalgraph = wx.StaticBox(self, label='<Select graph>', pos=(610, 70), size=(560, 460))

        #binding my buttons in this section of code
        
        self.btnInp.Bind(wx.EVT_BUTTON, self.GetData)
        self.btnExi.Bind(wx.EVT_BUTTON, self.OnQuit)
        

    def GetData(self, event):
        
        wx.Dialog.__init__(self, None, wx.ID_ANY, "Input Data", size=(350,320))

        self.Lvalue = wx.StaticText(self, wx.ID_ANY, label="l", pos=(20,20))
        self.L = wx.TextCtrl(self, value="50", pos=(110,20), size=(200,-1))
        
        self.Wvalue = wx.StaticText(self, wx.ID_ANY, label="W", pos=(20,60))
        self.W = wx.TextCtrl(self, value="1000", pos=(110,60), size=(200,-1))
        
        self.Civalue = wx.StaticText(self,wx.ID_ANY , label="Ci", pos=(20,100))
        self.Ci = wx.TextCtrl(self, value="11.5e-9", pos=(110,100), size=(200,-1))

        self.Vdvalue = wx.StaticText(self,wx.ID_ANY , label="Vd", pos=(20,140))
        self.Vd = wx.TextCtrl(self, value="-20", pos=(110,140), size=(200,-1))

        self.Tvalue = wx.StaticText(self,wx.ID_ANY , label="Type", pos=(20,180))
        self.Type = wx.ComboBox(self, choices = ['p - Type', 'n - Type', 'Ambipolar'], pos=(110,180), size=(200,-1))
        
        self.saveButton =wx.Button(self,wx.ID_ANY, label="Save", pos=(55,240))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        
        self.closeButton =wx.Button(self, label="Cancel", pos=(210,240))     
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)


        
        self.Centre()
        self.Show()

    def OnQuit(self, event):
        #self.result_W = None
        self.Destroy()

    def SaveConnString(self, event):
        self.result_L = self.L.GetValue()
        self.result_W = self.W.GetValue()
        self.result_Ci = self.Ci.GetValue()
        self.result_Vd = self.Vd.GetValue()
        self.result_Type = self.Type.GetValue()

        self.Destroy()

    

 #Run Program       
class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1, "Transfer Curve Analysis using WxPYTHON")
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()