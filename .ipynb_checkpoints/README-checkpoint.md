# OFET_analysis
Python scripts and jupyter notebooks to graphically analyze organic field effect transistor devices
OFET Analysis SOP

## Dependencies
import wx
import os
import numpy as np
import pandas as pd
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from scipy import stats

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

- os
- numpy
- scipy
- pandas
- matplotlib
- wxpython


## SOP
1.	Click to open files. Open the .ipynb corresponding to regime of OFET analysis. This will open a different tab with the code for the FET_analysis program.


2.	If you need to change any values for the channel width, channel length, or dielectric layer capacitance, do so in the third box from the top with 'L', 'W', or 'Ci', respectively.


3.	At the top of the page, in the tool bar, select "Cell>Run All" 


4.	Scroll to the bottom of the page and click on the link that appears in the final output box. This will open the window that hosts the dash GUI for the OFET_analysis program.


5.	In the new windown, follow the prompts to interact with the program.


6.	Once done, close all browser windows used. Return to the Command Prompt window and quit it by pressing "Ctrl+C" two times
