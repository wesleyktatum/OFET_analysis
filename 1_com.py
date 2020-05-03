import wx
import os
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
# import matplotlib
from scipy import stats

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error, r2_score


class Window(wx.Frame):

    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)

        # Defining status bar
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText("Welcome to OFET transfer curve analysis!"
                                     )

        # Drawing line to seperate Menu Icons area from the graphing area
        wx.StaticLine(self, pos=(1, 50), size=(1200, 10))

        # Drawing line to seperate graphing area from settings icons
        wx.StaticLine(self, pos=(1, 530), size=(1200, 10))

        # creating boundary from input graph and graph result
        self.rawgraph = wx.StaticBox(self, label='<Input Graph>',
                                     pos=(20, 70), size=(560, 460))
        self.finalgraph = wx.StaticBox(self, label='<Select graph>',
                                       pos=(610, 70), size=(560, 460))

        # These are the buttons at top of the frame for Menu Icons
        self.openFileDlgBtn = wx.Button(self, -1, "OPEN", pos=(20, 20))
        self.btn = wx.Button(self, -1, "EDIT", pos=(120, 20))
        self.btn = wx.Button(self, -1, "VIEW", pos=(220, 20))
        self.btn = wx.Button(self, -1, "HELP", pos=(320, 20))

        # These are the buttons at bottoms of the frame for other functions
        self.btnInp = wx.Button(self, -1, "Input Values", pos=(400, 560))
        self.btnCal = wx.Button(self, -1, "Calculate", pos=(500, 560))
        self.btnRes = wx.Button(self, -1, "Reset", pos=(600, 560))
        self.btnExi = wx.Button(self, -1, "Exit", pos=(700, 560))

        # binding my buttons in this section of code
        self.openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        self.btnInp.Bind(wx.EVT_BUTTON, self.GetData)
        self.btnExi.Bind(wx.EVT_BUTTON, self.OnClose)
        self.btnRes.Bind(wx.EVT_BUTTON, self.OnReset)

        self.params = [50, 1000, 1, -12, 'p-type']

    # function to open a file
    def onOpenFile(self, event):
        self.condition = 1
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*",
                            wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.fileName = os.path.join(self.dirname, self.filename)
            print('File Selected: ', os.path.basename(self.fileName))
        dlg.Destroy()

        data = np.loadtxt(self.fileName, delimiter='\t', skiprows=2)
        data = data[:, 0:2]

        Window.x = data[:, 0]
        Window.y = data[:, 1]

        self.root = RootPanel(self)

    # input values for L, W, Ci, Vd, Type
    def GetData(self, event):
        inputs = InputDialog(parent=self)
        self.params = inputs.report_values()

    # Function to quit the main screen
    def OnClose(self, event):
        self.Destroy()

    # resetting
    def OnReset(self, event):
        self.root.Destroy()


class RootPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        self.params = parent.params

        self.canvas_panel = CanvasPanel(self)
        self.zoom_panel = Zoom(parent=self)

        canvas_sizer = wx.BoxSizer(wx.HORIZONTAL)
        canvas_sizer.Add(self.canvas_panel, 1, wx.EXPAND)
        canvas_sizer.Add(self.zoom_panel, 1, wx.EXPAND)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(canvas_sizer)
        '''
        sizer = wx.GridSizer(1, 2, 0, 0)
        sizer.Add(self.canvas_panel, 1, wx.EXPAND)
        sizer.Add(self.zoom_panel, 1, wx.EXPAND)
        '''
        self.SetSizerAndFit(sizer)
        self.Show()


class CanvasPanel(wx.Panel):

    def __init__(self, parent, size=(200, 250)):
        super().__init__(parent)

        self.figure = Figure(figsize=(5, 4))
        self.axes = self.figure.add_subplot(111)
        self.parent = parent

        self.params = parent.params

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.canvas.Position = (50, 105)
        self.axes.set_title('Id Vg')
        self.axes.set_xlabel("Vg (Volt)")
        self.axes.set_ylabel("Id (Amps)")
        self.axes.plot(Window.x, Window.y, ".k")

        self.RS = RectangleSelector(self.axes, self.line_select_callback,
                                    drawtype='box', useblit=True,
                                    button=[1, 3], minspanx=5, minspany=5,
                                    spancoords='pixels',
                                    interactive=True,
                                    rectprops=dict(facecolor='None',
                                                   edgecolor='blue',
                                                   alpha=0.5, fill=False))

        self.canvas.draw()

    def line_select_callback(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.zoom_axes = [x1, x2, y1, y2]
        print('Selection is from', x1, y1, ' to ', x2, y2)

        self.calc_panel = CalcPanel(parent=self)

        self.parent.zoom_panel.Update(self)


class Zoom(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(600, 250))

    def Update(self, parent):
        # Load axis values of the selected rectangle
        zoom_axes = parent.zoom_axes
        x1, x2, y1, y2 = ((zoom_axes[0]), (zoom_axes[1]), (zoom_axes[2]),
                          (zoom_axes[3]))

        # print(x1, x2)
        # print(y1, y2)

        # Load all the values within the selected rectangle
        s = pd.Series(Window.x)
        zX = [x for x in Window.x if (x >= x1) & (x <= x2)]
        # print(s, zX)

        t = pd.Series(Window.y)
        zY = [x for x in Window.y if (x >= y1) & (x <= y2)]
        # print (t, zY)

        # duplicate the plot from the main panel
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)

        # Apply axis of drawn rectangle to the plot
        # self.axes.axis(zoom_axes)
        self.canvas.Position = (40, 105)
        self.axes.set_title('Id Vg')
        self.axes.set_xlabel("Vg (Volt)")
        self.axes.set_ylabel("Id (Amps)")
        self.axes.plot(s, t, ".k")
        self.axes.plot(zX, zY, ".r")

        # reshape my x data
        Zoom.zx = np.array(zX)
        zXr = Zoom.zx.reshape(-1, 1)

        # Now we have portion of the data as zX (voltage) and zY ( Current)
        # lets split 20% of the data to test and 80% to train
        x_train, x_test, y_train, y_test = train_test_split(zXr, zY,
                                                            test_size=0.20,
                                                            random_state=1)

        # create a linear regression model object
        regression_model = LinearRegression()
        # pass trhough the x_train &y_train data set to train the model
        regression_model.fit(x_train, y_train)

        # get coefficient of our model and the intercept
        intercept = regression_model.intercept_
        coefficient = regression_model.coef_

        print("the coefficient/slope of our model is:", coefficient)
        print("the intercept of our model is:", intercept)

        # testing prediction
        y_pred = regression_model.predict(zXr)

        # Plot outputs
        self.axes.plot(zXr, y_pred, color='blue', linewidth=2)

        self.canvas.draw()
        self.Refresh()

        CalcPanel.calculate_linear_output(parent.calc_panel)


class InputDialog(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, None, wx.ID_ANY, "Input Data",
                           size=(350, 320))

        self.result_L = 50
        self.result_W = 1000
        self.result_Ci = 1
        self.result_Vd = -12
        self.result_Type = 'p - type'

        # creating all the text boxes for inputting values
        self.Lvalue = wx.StaticText(self, wx.ID_ANY, label="l", pos=(20, 20))
        self.L = wx.TextCtrl(self, value=str(self.result_L), pos=(110, 20),
                             size=(200, -1))

        self.Wvalue = wx.StaticText(self, wx.ID_ANY, label="W", pos=(20, 60))
        self.W = wx.TextCtrl(self, value=str(self.result_W), pos=(110, 60),
                             size=(200, -1))

        self.Civalue = wx.StaticText(self, wx.ID_ANY, label="Ci",
                                     pos=(20, 100))
        self.Ci = wx.TextCtrl(self, value=str(self.result_Ci), pos=(110, 100),
                              size=(200, -1))

        self.Vdvalue = wx.StaticText(self, wx.ID_ANY, label="Vd",
                                     pos=(20, 140))
        self.Vd = wx.TextCtrl(self, value=str(self.result_Vd), pos=(110, 140),
                              size=(200, -1))

        self.Tvalue = wx.StaticText(self, wx.ID_ANY, label="Type",
                                    pos=(20, 180))
        self.Type = wx.ComboBox(self,
                                choices=['p - Type', 'n - Type', 'Ambipolar'],
                                pos=(110, 180), size=(200, -1))
        # creating and linking Save and Exit buttons
        self.saveButton = wx.Button(self, wx.ID_ANY, label="Save",
                                    pos=(55, 240))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)

        self.closeButton = wx.Button(self, label="Exit", pos=(210, 240))
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.Centre()
        self.Show()

    # save values
    def SaveConnString(self, event):
        self.result_L = self.L.GetValue()
        self.result_W = self.W.GetValue()
        self.result_Ci = self.Ci.GetValue()
        self.result_Vd = self.Vd.GetValue()
        self.result_Type = self.Type.GetValue()
        # print('in save:', L)

        print('L: ', self.result_L)
        print('W: ', self.result_W)
        print('Ci: ', self.result_Ci)
        print('Vd: ', self.result_Vd)
        print('Type: ', self.result_Type)

    def report_values(self):
        # print('in report:', self.result_L)
        return [self.result_L, self.result_W, self.result_Ci, self.result_Vd,
                self.result_Type]

    # close event
    def OnClose(self, e):
        self.Destroy()


class CalcPanel():
    def __init__(self, parent):
        self.parent = parent

        self.zoom_axes = parent.zoom_axes
        self.x1, self.x2, self.y1, self.y2 = ((self.zoom_axes[0]),
                                              (self.zoom_axes[1]),
                                              (self.zoom_axes[2]),
                                              (self.zoom_axes[3]))

        self.Vg_range = Window.x
        self.absId_range = Window.y

        self.params = parent.params

        self.L = self.params[0]
        self.W = self.params[1]
        self.Ci = self.params[2]
        self.Vd = self.params[3]
        self.Type = self.params[4]

        print('params:', self.params)
#         Window.SaveConnString(self.L, self.W, self.Ci, self.Vd, self.Type)

#     def idealreg_linear(self, parent):
#         Vg_range = Window.x
#         absId_range = Window.y
#         ideal_abs_slope, ideal_abs_intercept, r_value, p_value, std_err =
#           stats.linregress(Vg_range, absId_range)

#         for x in Vg_range:
#             ideal_absId.append(ideal_abs_slope * Vg_range[x] +
#                                ideal_abs_intercept)

#         return ideal_abs_slope, ideal_abs_intercept, ideal_absId

    def calculate_linear_output(self):

        # ideal_absId = []

        xRange = [x for x in Window.x if (x >= self.x1) & (x <= self.x2)]
        # Obtain first index of xRange
        xStart = np.where(xRange[0] == Window.x)
        # Obtain last index of xRange
        xEnd = np.where(xRange[-1] == Window.x)
        # Constrain yRange to xRange
        yRange = Window.y[(xStart[0])[0]:(xEnd[0])[0] + 1]

#         print(Window.x)
#         print(Window.SaveConnString)
#         print(xRange)
#         print(yRange)

        abs_slope, abs_intercept, r_value, p_value, std_err = \
            stats.linregress(xRange, yRange)

        ideal_abs_slope, ideal_abs_intercept, r_value, p_value, std_err = \
            stats.linregress(self.Vg_range, self.absId_range)

#         for x in self.Vg_range:
#             ideal_absId.append(ideal_abs_slope * self.Vg_range[x] +
#                                ideal_abs_intercept)

        mu_lin = (abs_slope * 1 * self.L) / (self.Vd * self.W * self.Ci)
        r_lin = ideal_abs_slope / abs_slope
        Id_max = yRange[0]
        Id_min = yRange[-1]

        on_off = Id_max/Id_min
        Vt = -abs_intercept/abs_slope

        values = np.array([mu_lin, r_lin, on_off, Vt])
        print(values)
        # return values


class App(wx.App):
    def OnInit(self):
        win = Window(title="Transfer Curve Analysis using WxPYTHON",
                     size=(1200, 650))
        win.Centre()
        win.Show()
        return True


if __name__ == "__main__":
    app = App()
    app.MainLoop()
