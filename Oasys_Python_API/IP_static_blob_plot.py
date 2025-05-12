# IP_static_blob_plot.py
### This Python script using the Oasys.D3PLOT Python module will
###   - Start Oasys D3PLOT using the given executable name
###   - Read in an LS-Dyna model
###   - Zoom all on selected parts (YZ View), then display everything
###   - Turn off header and clock, change fonts, turn off 1d elements
###   - Output as PNG image
###
# Notes to the user:
# The example model doesn't have any 1d elements, so some errors appear in the dialogue window, but they can be ignored
# There is currently no way to change the blob value number format except manually in D3PLOT
# You need to change the executable path to match your executable
# Install the necessary python module if you have not done so: pip install Oasys.D3PLOT
# Import necessary modules
import Oasys.D3PLOT
# Start D3PLOT
connection = Oasys.D3PLOT.start(abspath="C:\\Users\\jlam\\AppData\\Roaming\\Oasys\\v21.0_x64\\d3plot21_0_x64.exe")

# Open model
m = Oasys.D3PLOT.Model("IP_dummy.ptf")
# Graphics Window object for the first graphics window
gw = Oasys.D3PLOT.GraphicsWindow.First()

# We want to read in external data
Oasys.D3PLOT.DialogueInput("UTILITIES", "EXTERNAL", "READ_FILE", "blob_out_example.blob")
# We want to zoom in selected parts only: blank everything else, zoom all, unblank everything
# XY View, then rotate to landscape orientation
Oasys.D3PLOT.View.Show(Oasys.D3PLOT.View.XY)
Oasys.D3PLOT.DialogueInput("RS", "0 0 270")
# Blank everything
Oasys.D3PLOT.Part.BlankAll(gw, m)
# Unblank the following parts
p700212 = Oasys.D3PLOT.Part.GetFromID(m, 700212)
p700016 = Oasys.D3PLOT.Part.GetFromID(m, 700016)
p700212.Unblank(gw)
p700016.Unblank(gw)
# Zoom all
Oasys.D3PLOT.View.Ac()
# Unblank all
Oasys.D3PLOT.Part.UnblankAll(gw, m)

# Switch off the header and clock, set fonts, turn off 1D entities
Oasys.D3PLOT.DialogueInput("DISPLAY_OPTION", "HEADER_SWITCH", "OFF")
Oasys.D3PLOT.DialogueInput("DISPLAY_OPTION", "CLOCK_SWITCH", "OFF")
Oasys.D3PLOT.DialogueInput("DISPLAY_OPTION", "FONT", "LABELS", "SIZE", "EIGHT_POINT")
Oasys.D3PLOT.DialogueInput("DISPLAY_OPTION", "FONT", "CONTOUR_BAR", "SIZE", "TWENTYFOUR_POINT")
Oasys.D3PLOT.DialogueInput("DISPLAY_OPTION", "ENTITY_SWITCH", "BEAMS", "OFF")
Oasys.D3PLOT.DialogueInput("DISPLAY_OPTION", "ENTITY_SWITCH", "SPOTWELD", "OFF")
Oasys.D3PLOT.DialogueInput("DISPLAY_OPTION", "ENTITY_SWITCH", "NRBs", "OFF")

# Write out PNG image
#Oasys.D3PLOT.Image.WriteImage("image.png")
