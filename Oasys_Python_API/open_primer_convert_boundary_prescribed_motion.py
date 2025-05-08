# open_primer_convert_boundary_prescribed_motion.py
### This Python script using the Oasys.PRIMER Python module will
###   - Start Oasys PRIMER using the given executable name
###   - Read in the LS-Dyna model supplied as the first argument
###   - Take the first *BOUNDARY_PRESCRIBED_MOTION
###   - Take the vector from the first *BOUNDARY_PRESCRIBED_MOTION
###   - Calculate the xyz components from the vector
###   - Create 3 separate *BOUNDARY_PRESCRIBED_MOTION from vector components
###   - Delete the original *BOUNDARY_PRESCRIBED_MOTION
###   - Write the model (overwriting the original)
###   - Wait five seconds (to allow the model write to complete)
###   - Close PRIMER
###
### I wrote this script because while Radioss can read in Dyna models,
###   *BOUNDARY_PRESCRIBED_MOTION using a vector is improperly mapped
###   but 3 separate *BOUNDARY_PRESCRIBED_MOTIONs with x, y and z components
###   seems to work
# 
# Notes to the user:
# You need to change the executable path to match your executable
# Put your model filename on the command line as the first argument. A .key or .k file is expected, but should still work in any case
# Install the necessary python module if you have not done so: pip install Oasys.PRIMER
#
# Import necessary modules
import sys
import Oasys.PRIMER

# Start PRIMER
# Change the variable to match the location of your D3PLOT 21 executable. All backslashes must be doubled.
abspath="C:/Users/jlam/AppData/Roaming/Oasys/v21.0_x64/primer21_1_x64.exe"
#abspath="/opt/oasys/oa21/primer21_64.exe"
connection = Oasys.PRIMER.start(abspath, wait=5)
model_filename = sys.argv[1]

# Read model
m = Oasys.PRIMER.Model.Read(model_filename)

# Allocate flag
f = Oasys.PRIMER.AllocateFlag()

# Select first *BOUNDARY_PRESCRIBED_MOTION
b = Oasys.PRIMER.PrescribedMotion.First(m)
# Assume it is rigid part type
# Integer part will be the part id specified in b
part = b.typeid
# Integer vectorid will be the vector id specified in b
vectorid = b.vid
# Integer curveid will be the loadcurve id specified in b
curveid = b.lcid
# Get vector
v = Oasys.PRIMER.Vector.GetFromID(m, vectorid)
# Confirm no coordinate system defined
print("Coordinate system for vector: " + str(v.cid))
# x, y, z components
x=v.xh-v.xt
y=v.yh-v.yt
z=v.zh-v.zt
mag=(x*x+y*y+z*z)**0.5
print("Vector magnitude: " + str(mag))
print("x-component: " + str(x/mag))
print("y-component: " + str(y/mag))
print("z-component: " + str(z/mag))

# Create 3 *BOUNDARY_PRESCRIBED_MOTION from vector components (in model m, on part, same vad as original, using curveid, rigid part type)
bx = Oasys.PRIMER.PrescribedMotion(m, part, 1, b.vad, curveid, Oasys.PRIMER.PrescribedMotion.RIGID, 2)
by = Oasys.PRIMER.PrescribedMotion(m, part, 2, b.vad, curveid, Oasys.PRIMER.PrescribedMotion.RIGID, 3)
bz = Oasys.PRIMER.PrescribedMotion(m, part, 3, b.vad, curveid, Oasys.PRIMER.PrescribedMotion.RIGID, 4)
# Set scale factor to axis component
bx.sf = x/mag
by.sf = y/mag
bz.sf = z/mag
# Deactivate _ID option
bx.id = False
by.id = False
bz.id = False

# Delete original *BOUNDARY_PRESCRIBED_MOTION
Oasys.PRIMER.PrescribedMotion.UnflagAll(m, f)
b.SetFlag(f)
m.DeleteFlagged(f)

# Write model
output_obj = {
    "separator": Oasys.PRIMER.Include.UNIX,
    "version": "R12.0"
}
m.Write(model_filename, output_obj)

# Wait because we do not want to closer PRIMER while the model is still writing
Oasys.PRIMER.MilliSleep(5000)

# Close PRIMER
Oasys.PRIMER.terminate(connection)
