# open_t-his_compare_two_curves_L384_IHI.py
### This Python script using the Oasys.THIS Python module will
###   - Start Oasys T-HIS using the given executable name
###   - Read in two IHI head acceleration curves: one from each of two models
###   - Overlay the two curves with injury values: curves are different colours
###   - Set graph properties: legend, axes, number formats and colours
###
# Notes to the user:
# If you have T-HIS 21 (or higher) and python 3.8 (or higher) installed, then you can use this script to open T-HIS, read in two curves and compare the 3ms clip values
# You need to change the T-HIS executable path to match your executable
# You also need to change the file paths to match your curve files
# If you have never done so, you will need to execute this command to install the necessary python module at the command prompt: pip install Oasys.THIS
import Oasys.THIS
# The sys module allows reading of command line arguments
import sys

# User-defined variables here
# Set "executable" to the path to your T-HIS 21 executable. Make sure all backslashes are doubled
executable = "C:\\Users\\jlam\\AppData\\Roaming\\Oasys\\v21.0_x64\\this21_0_x64.exe"
# Set "curve1file" to the global path to your first .cur file. Make sure all backslashes are doubled
curve1file = sys.argv[1]
curve2file = sys.argv[2]

# Start THIS
connection = Oasys.THIS.start(abspath= executable )
Oasys.THIS.Options.auto_confirm = 1

# Read curves
# Set variables to .cur files. All backslashes must be doubled
# Read model1 curve into curve ID 1
model1options = {}
model1options["outputOpt"] = 1
# Read model2 curve into curve ID 2
model2options = {}
model2options["outputOpt"] = 2
Oasys.THIS.Read.Cur(curve1file)
Oasys.THIS.Read.Cur(curve2file)

# Calculate 3ms clip for both curves and set colour
model1cur = Oasys.THIS.Curve.GetFromID(1)
model2cur = Oasys.THIS.Curve.GetFromID(2)
model13ms = Oasys.THIS.Operate.Tms(model1cur,0.003)
model23ms = Oasys.THIS.Operate.Tms(model2cur,0.003)
model1cur.colour = Oasys.THIS.Colour.BLUE
model2cur.colour = Oasys.THIS.Colour.MAGENTA
# Set injury marker colour to curve colour? Not yet available in Python API
# Set curve property number format to general? Not yet available in Python API

# Graph properties: legend auto layout, 1 column, x-axis general number format with 3 decimal places, y-axis general number format with 0 decimal places
num = Oasys.THIS.Graph.Total()
graph = Oasys.THIS.Graph.GetFromID(num)
graph.x_unit_decimals = 3
graph.y_unit_decimals = 0
graph.legend_layout = Oasys.THIS.Graph.LEGEND_AUTO
graph.num_legend_columns = Oasys.THIS.Graph.LEGEND_1_COLUMN
graph.background_colour = Oasys.THIS.Colour.WHITE
graph.foreground_colour = Oasys.THIS.Colour.BLACK
# Graph.AXIS_UNITS_GENERAL constant does not exist
# 2 seems to be general
graph.x_unit_format = 2
graph.y_unit_format = 2
