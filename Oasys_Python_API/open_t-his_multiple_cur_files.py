# open_t-his_multiple_cur_files.py
### This Python script using the Oasys.THIS Python module will
###   - Start Oasys T-HIS using the given executable name
###   - Read in all the .cur curve files listed in the array cur_list
###   - Calculate the 3ms clip injury value for each curve and set the colour
###
# Notes to the user:
# If you have T-HIS 21 (or higher) and python 3.8 (or higher) installed, then you can use this script to open T-HIS, read in two curves and compare the 3ms clip values
# You need to change the T-HIS executable path to match your executable
# You also need to populate the cur_list with a list of .cur files
#   using the format: "P:/W12345_Client_Project/path/to/cur/file/curfile.cur",
#   i.e. quote mark at beginning, quote mark and comma at the end
#   the final file does not need a comma
# If you have never done so, you will need to execute this command to install the necessary python module at the command prompt: pip install Oasys.THIS
import Oasys.THIS
# The sys module allows reading of command line arguments
import sys
# The tqdm module gives a progress bar as it loops
from tqdm import tqdm
# The os module is required to interact with the Operating System, specifically some file operations
import os

# User-defined variables here
# Set "executable" to the path to your T-HIS 21 executable. Make sure all backslashes are doubled (or change to single forward slashes)
executable = "C:\\Users\\jlam\\AppData\\Roaming\\Oasys\\v21.0_x64\\this21_0_x64.exe"
# List of .cur files
cur_list=[
"P:/Project_1/Head_Impact/IHI/Phase_1/000/Project_1_Phase_1_n000_Pos01/Project_1_Phase_1_n000_Pos01_19071/_Reporter_Output/Project_1_Phase_1_n000_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/010/Project_1_Phase_1_n010_Pos01/Project_1_Phase_1_n010_Pos01_21206/_Reporter_Output/Project_1_Phase_1_n010_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/011/Project_1_Phase_1_n011_Pos01/Project_1_Phase_1_n011_Pos01_19313/_Reporter_Output/Project_1_Phase_1_n011_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/012/Project_1_Phase_1_n012_Pos01/Project_1_Phase_1_n012_Pos01_19386/_Reporter_Output/Project_1_Phase_1_n012_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/012a/Project_1_Phase_1_n012a_Pos01/Project_1_Phase_1_n012a_Pos01_21243/_Reporter_Output/Project_1_Phase_1_n012a_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/012b/Project_1_Phase_1_n012b_Pos01/Project_1_Phase_1_n012b_Pos01_20964/_Reporter_Output/Project_1_Phase_1_n012b_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/012c/Project_1_Phase_1_n012c_Pos01/Project_1_Phase_1_n012c_Pos01_20934/_Reporter_Output/Project_1_Phase_1_n012c_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/013/Project_1_Phase_1_n013_Pos01/Project_1_Phase_1_n013_Pos01_19510/_Reporter_Output/Project_1_Phase_1_n013_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/014/Project_1_Phase_1_n014_Pos01/Project_1_Phase_1_n014_Pos01_19930/_Reporter_Output/Project_1_Phase_1_n014_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/030/Project_1_Phase_1_n030_Pos01/Project_1_Phase_1_n030_Pos01_21278/_Reporter_Output/Project_1_Phase_1_n030_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/030a/Project_1_Phase_1_n030a_Pos01/Project_1_Phase_1_n030a_Pos01_21957/_Reporter_Output/Project_1_Phase_1_n030a_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/031/Project_1_Phase_1_n031_Pos01/Project_1_Phase_1_n031_Pos01_21341/_Reporter_Output/Project_1_Phase_1_n031_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
"P:/Project_1/Head_Impact/IHI/Phase_1/032/Project_1_Phase_1_n032_Pos01/Project_1_Phase_1_n032_Pos01_21927/_Reporter_Output/Project_1_Phase_1_n032_Pos01_A0_HEAD_ACCEL_MAG_g_s.cur",
]

# Start THIS
connection = Oasys.THIS.start(abspath= executable )
Oasys.THIS.Options.auto_confirm = 1

# Read curves
# Set variables to .cur files. All backslashes must be doubled
for curfile in tqdm(cur_list):
    if not os.path.isfile(curfile):
        print(str(curfile) + " does not exist")
        sys.exit()
    else:
        Oasys.THIS.Read.Cur(curfile)
            
# Graph properties: legend auto layout, 1 column, x-axis general number format with 3 decimal places, y-axis general number format with 0 decimal places
num = Oasys.THIS.Graph.Total()
graph = Oasys.THIS.Graph.GetFromID(num)
graph.x_unit_decimals = 3
graph.y_unit_decimals = 0
graph.legend_layout = Oasys.THIS.Graph.LEGEND_AUTO
#graph.num_legend_columns = Oasys.THIS.Graph.LEGEND_1_COLUMN
graph.background_colour = Oasys.THIS.Colour.WHITE
graph.foreground_colour = Oasys.THIS.Colour.BLACK
# Graph.AXIS_UNITS_GENERAL constant does not exist
# 2 seems to be general
graph.x_unit_format = 2
graph.y_unit_format = 2
# Calculate 3ms clip for all curves
curve = Oasys.THIS.Curve.First()
val = Oasys.THIS.Operate.Tms(curve,0.003)
setcolour=1
curve.colour = setcolour
setcolour += 1
curve = curve.Next()
while curve:
    val = Oasys.THIS.Operate.Tms(curve,0.003)
    curve.colour = setcolour
    setcolour += 1
    if setcolour > 30:
        setcolour = 1
    curve = curve.Next()
