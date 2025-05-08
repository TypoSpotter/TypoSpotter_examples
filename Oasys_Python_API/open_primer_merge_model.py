# open_primer_merge_model.py
### This Python script using the Oasys.PRIMER Python module will
###   - Start Oasys PRIMER using the given executable name
###   - Read in the LS-Dyna model supplied as the first argument
###   - Write the model as a merged model (i.e. all includes merged into the master)
###   - Wait five seconds (to allow the model write to complete)
###   - Close PRIMER
###
# Notes to the user:
# This python script will open Primer, read in a model and write it out merged into a single master
# You need to change the executable path to match your executable
# Put your model filename on the command line as the first argument. A .key or .k file is expected, but should still work in any case
# Install the necessary python module if you have not done so: pip install Oasys.PRIMER
# Import necessary modules
import sys
import Oasys.PRIMER
import time

# Start PRIMER
# Change the variable to match the location of your D3PLOT 21 executable. All backslashes must be doubled.
abspath="C:/Users/jlam/AppData/Roaming/Oasys/v21.0_x64/primer21_1_x64.exe"
#abspath="/opt/oasys/oa21/primer21_64.exe"
connection = Oasys.PRIMER.start(abspath, wait=5)
model_filename = sys.argv[1]
merged_model = f"{model_filename.split('.k')[0]}_merged.key"

# Read model
m = Oasys.PRIMER.Model.Read(model_filename)

# Write model as merged
output_obj = {
    "method": Oasys.PRIMER.Include.MERGE,
    "separator": Oasys.PRIMER.Include.UNIX,
    "version": "R12.0"
}
m.Write(merged_model, output_obj)

# Wait because we do not want to closer PRIMER while the model is still writing
time.sleep(5)

# Close PRIMER
Oasys.PRIMER.terminate(connection)
