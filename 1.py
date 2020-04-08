import wx
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
import matplotlib

class Window(wx.Frame):
    """ Fenêtre principale de l'application """

    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)
        RootPanel(self)

class RootPanel(wx.Panel):
    """ Panel contenant tous les autres widgets de l'application """

    def __init__(self, parent):
        super().__init__(parent)

        panel_buttons = wx.Panel(self)
        panel_buttons_sizer = wx.GridSizer(1, 2, 0, 0)

        self.canvas_panel = CanvasPanel(self)
        self.zoom_panel = Zoom(parent=self)

        select_button = PickButton(
            panel_buttons,
            "Text files (txt)|*.txt|All files|*.*",
            self.canvas_panel.load_from_file,
            label="Show on this window (*.txt)",
        )
        toplevel_select_button = TopLevelPickButton(
            panel_buttons,
            "Text files (txt)|*.txt|All files|*.*",
            label="Show on separate window (txt)",
        )
        panel_buttons_sizer.Add(select_button)
        panel_buttons_sizer.Add(toplevel_select_button)
        panel_buttons.SetSizer(panel_buttons_sizer)

        canvas_sizer = wx.BoxSizer(wx.HORIZONTAL)
        canvas_sizer.Add(self.canvas_panel,1,wx.EXPAND)
        canvas_sizer.Add(self.zoom_panel,1,wx.EXPAND)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel_buttons)
        sizer.Add(canvas_sizer)
        self.SetSizerAndFit(sizer)
        self.Show()

class PickButton(wx.Button):
    """ Bouton permettant de choisir un fichier """

    def __init__(self, parent, wildcard, func, **kwargs):
        # func est la méthode à laquelle devra être foruni le fichier sélectionné
        super().__init__(parent, **kwargs)
        self.wildcard = wildcard
        self.func = func
        self.Bind(wx.EVT_BUTTON, self.pick_file)

    def pick_file(self, evt):
        style = style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        with wx.FileDialog(
            self, "Pick files", wildcard=self.wildcard, style=style
        ) as fileDialog:
            if fileDialog.ShowModal() != wx.ID_CANCEL:
                chosen_file = fileDialog.GetPath()
                self.func(chosen_file)

class TopLevelPickButton(PickButton):
    """ Permet de choisir un fichier et d'ouvrir une toplevel """

    def __init__(self, parent, wildcard, **kwargs):
        super().__init__(parent, wildcard, self.create_toplevel, **kwargs)

    def create_toplevel(self, file_name):
        """ Ouvre une toplevel et affiche le graphique """
        self.win = TopLevelCanvas(self.Parent)
        self.win.canvas_panel.load_from_file(file_name)
        self.win.Show()

class CanvasPanel(wx.Panel):
    """ Panel du graphique matplotlib """
    def __init__(self, parent , size=(200,250)):
        super().__init__(parent)
        self.figure = Figure(figsize =(4,3))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.Size = self.canvas.Size
        self.parent = parent

    def load_from_file(self, file_name):
        """
        Méthode effectuant l'intermédiaire pour charger le fichier selon
        son type
        """
        self.axes = self.figure.add_subplot(111)
        if file_name.endswith(".txt"):
            self._load_nc(file_name)
        else:
            self._load_txt(file_name)
        self.canvas.draw()

    def _load_txt(self, file_name):
        self._load_nc(file_name)

    def _load_nc(self, file_name):
        """ Simule le chargement et affichage à partir d'un fichier nc """
        
        self.axes.plot((1, 11), lw=3.5, c='b', alpha=.7)
      

        self.RS = RectangleSelector(self.axes,self.line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True,
                                       rectprops = dict(facecolor='None',edgecolor='red',alpha=0.5,fill=False))


    def line_select_callback(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.zoom_axes=[x1,x2,y1,y2]
        self.parent.zoom_panel.Update(self)


class Zoom(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(200,250))
        self.Show()

    def Update(self,parent):
        #Load axis values of the selected rectangle
        zoom_axes=parent.zoom_axes

        #duplicate the plot from the main panel
        self.figure = Figure(figsize =(4,3))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.axes = self.figure.add_subplot(111)

        #Apply axis of drawn rectangle to the plot
        self.axes.axis(zoom_axes)

        
        self.axes.plot((1, 10), lw=3.5, c='b', alpha=.7)
        self.canvas.draw()
        self.Refresh()

class TopLevelCanvas(wx.Frame):
    """ Fenêtre affichant uniquement un graph matplotlib """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas_panel = CanvasPanel(self)
        self.zoom_panel = Zoom(parent=self)
        self.Size = self.canvas_panel.Size
        canvas_sizer = wx.BoxSizer(wx.HORIZONTAL)
        canvas_sizer.Add(self.canvas_panel,1,wx.EXPAND)
        canvas_sizer.Add(self.zoom_panel,1,wx.EXPAND)
        self.SetSizerAndFit(canvas_sizer)
        self.Show()

class App(wx.App):
    def OnInit(self):
        win = Window(title="A test dialog", size=(1000, 800))
        win.Show()
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()