from iccap import *
import matplotlib.pyplot as plt
import numpy as np
from icutils import *
#-- [WPRO_INIT]

# for Setup Initialization.

# This program loads Instrument Options table for this Setup.

# MVar calls Model Variables defined at Routine level
# All the Routines share these variables
# Note that we are not creating these variables, since they exist
# and they are managed by WaferPro
# DVar are for local Routine variables defined in the RCV table
# SVar are for local Setup variables defined in this Routine

Debug         = MVar("Debug")         #ModelVariable, WaferPro Debug Level
Mode          = MVar("Mode")          #ModelVariable, WaferPro Run Mode
bRet          = MVar("bRet")          #Setup/ModelVariable, WaferPro Success(=1)/Nonsuccess(=0) Flag
ErrorMsg      = MVar("ErrorMsg")      #Setup/ModelVariable, Error Message sent to WaferPro when Nonsuccess
IotFileName   = MVar("IotFileName")   #ModelVariable, instrument options file name
Type          = MVar("Type")          #ModelVariable, polarity factor (1, -1)

# Note that get_val() returns a string
if int(Debug.get_val()) >= 1:
    print(">>> exec. Xfm '" + icfuncs.whoami() + "' ...")
#---------------------------------------------------------------------
# RETURN_VALUE 1 : for success
# RETURN_VALUE 0 : for fail/error
#---------------------------------

#--- Initialize Variables
bRet.set_val(1)
ErrorMsg.set_val("")
indicator = 'f'
#--- Define local variables for this Program
thisSetup = Setup(".")
_, mname, dname, sname = thisSetup.get_fullname().split("/")
Path2Setup  = thisSetup.get_fullname()
RoutineName = dname
SetupName   = sname
#--- Load corresponding .iot file (InstrumentOptions) into actual Setup
#dummy = icfuncs.WPro_LoadInstrOptions(RoutineName, SetupName)

##===== Action *Execute* =====
##--- Run either measurement, or simulation, or data import
#dummy = icfuncs.WPro_RunDAQExe(RoutineName, SetupName)
if Mode.get_val() == "Simulation":
    iccap_func("matrix_init","Execute")
    iccap_func("connect","Execute")
    iccap_func("runMeasure_py_simulation","Execute")
    iccap_func("disconnect","Execute")
elif Mode.get_val() == "Measure":
#else:
    iccap_func("matrix_init","Execute")
    iccap_func("connect_measure_{}".format(indicator),"Execute")
    iccap_func(".", "Measure")
#    iccap_func("runMeasure_{}_py".format(indicator),"Execute")
    iccap_func("disconnect","Execute")
# Need to set up future program to load from .mea!
# elif Mode.get_val() = "Load From Record"

#-------------------------
iccap_func("export_mea_{}".format(indicator),"Execute")



set_return_value(1)

