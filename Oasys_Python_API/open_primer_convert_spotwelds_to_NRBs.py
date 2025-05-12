# open_primer_convert_spotwelds_to_NRBs.py
### This Python script using the Oasys.PRIMER Python module will
###   - Start Oasys PRIMER using the given executable name
###   - Read in the LS-Dyna model supplied as the first argument
###   - Find the last node set to allocate the node set id
###   - Find the last nodal rigid body set to allocate the nrb id
###   - For every SPOTWELD, create a nodal rigid body using the two nodes of the spotweld
###   - Once complete, the user can check, delete spotwelds and write out the model
###
# Notes to the user:
# This script creates a nodal rigid body at every SPOTWELD.
# The purpose of this script is to allow LS-Dyna models using SPOTWELDs to run in Radioss Implicit
# The script does not delete the SPOTWELDs nor write out the model. That is left to the user.
# You need to change the executable path to match your executable
# Put your model filename on the command line as the first argument.
# Install the necessary python module if you have not done so: pip install Oasys.PRIMER
# Import necessary modules
import sys
import Oasys.PRIMER

# Start PRIMER
# Change the variable to match the location of your D3PLOT 21 executable. All backslashes must be doubled.
abspath="C:/Users/jlam/AppData/Roaming/Oasys/v21.0_x64/primer21_1_x64.exe"
#abspath="/opt/oasys/oa21/primer21_64.exe"
connection = Oasys.PRIMER.start(abspath, wait=5)
model_filename = sys.argv[1]

# Open model
m = Oasys.PRIMER.Model.Read(model_filename)

# First *SET_NODE id
lastnodeset = Oasys.PRIMER.Set.Last(m, Oasys.PRIMER.Set.NODE)
setid = lastnodeset.sid + 1
# First *CONSTRAINED_NODAL_RIGID_BODY
lastNRB = Oasys.PRIMER.NodalRigidBody.Last(m)
NRBid = lastNRB.pid + 1

# Select first spotweld
s = Oasys.PRIMER.Spotweld.First(m)
#s.n1 is first node of spotweld
#s.n2 is second node of spotweld
# Create *SET_NODE first
setnode = Oasys.PRIMER.Set(m, setid, Oasys.PRIMER.Set.NODE)
# Add two nodes to *SET_NODE
setnode.Add(s.n1)
setnode.Add(s.n2)
# Create NRB in model m with label NRBid, using new setnode
NRB = Oasys.PRIMER.NodalRigidBody(m, setnode.sid, NRBid)
setid += 1
NRBid += 1

while s is not None:
# Create NRB with two nodes of spotweld
# Create *SET_NODE first
    setnode = Oasys.PRIMER.Set(m, setid, Oasys.PRIMER.Set.NODE)
# Add two nodes to *SET_NODE
    setnode.Add(s.n1)
    setnode.Add(s.n2)
# Create NRB in model m with label NRBid, using new setnode
    NRB = Oasys.PRIMER.NodalRigidBody(m, setnode.sid, NRBid)
    setid += 1
    NRBid += 1
    s = s.Next()
