# OFET_analysis
Python scripts and jupyter notebooks to graphically analyze organic field effect transistor devices
OFET Analysis SOP

### Dependencies

- os
- numpy
- scipy
- pandas
- matplotlib
- wxpython


## Procedure

### Opening GUI (Windows)
1.	After cloning repo and installing all dependencies, open a command prompt window and navigate to the local version of this code. Initiate the GUI by running the command `python ofet_analysis_gui.py`

### Opening GUI (mac)
1. After cloning repo and installing all dependencies, open a terminal window and navigate to the local version of this code. Initiate the GUI by running the command `pythonw ofet_analysis_gui.py`. The pythonw is used to allow wxpython root access to screen. For more information, read wxpython documentation at https://www.wxpython.org/pages/downloads/

### Using the GUI
1. Click to open files. Select data .txt files containing raw OFET transfer curves.

2.	If you need to change any values for the channel width, channel length, dielectric layer capacitance, or any other device or testing voltage parameters, do so in the left box with 'L', 'W', 'C$_{i}$', and so on, respectively.

3. Using your cursor, click and highlight the linear regime of the OFET performance. Readjust the boundaries as necessary

4. When the projected linear fit appears optimized, click 'Calculate' to determine the charge carrier mobility, ideality coefficient (r), on/off ratio, and threshold voltage (V$_{th}$)

5. Change filename and click save to write results as a list in a .txt file. This method also appends new results to the end of existing results files.

6. After all devices are tested for a given sample point, average the devices' results together by clicking 'Average', which will append the average of each column to the end of the file.
