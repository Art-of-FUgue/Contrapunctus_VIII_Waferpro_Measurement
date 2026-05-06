# update: explicit
from iccap import *
import matplotlib.pyplot as plt
from iccap import icfuncs as f
import numpy as np

# called by WPE Routine
Debug         = MVar("Debug")         #ModelVariable, WaferPro Debug Level
Mode          = MVar("Mode")          #ModelVariable, WaferPro Run Mode
bRet          = MVar("bRet")          #Setup/ModelVariable, WaferPro Success(=1)/Nonsuccess(=0) Flag
ErrorMsg      = MVar("ErrorMsg")      #Setup/ModelVariable, Error Message sent to WaferPro when Nonsuccess
Type          = MVar("Type")          #ModelVariable, polarity factor (1, -1)
Vd_stress     = DVar("Vd_stress")
Vg_stress     = DVar("Vg_stress")
Vb_stress     = DVar("Vb_stress")
Stress_Time_List = DVar("Stress_Time_List")
Idsat_Values = SVar("Idsat_Values")
Ibs_Values = SVar("Ibs_Values")
Igs_Values = SVar("Igs_Values")
filename = SVar("filename") 

print("Debug with {}".format(Mode.get_val()))

Stress_Time_Values = [float(i) for i in Stress_Time_List.get_val().split(",")]
#print Stress_Time_Values
#print filename.get_val()

#print Debug.get_val(), Mode.get_val(), bRet.get_val(), Type.get_val(), Vd_stress.get_val()

#--- Define local variables for this Program
thisSetup = Setup(".")
_, mname, dname, sname = thisSetup.get_fullname().split("/")
Path2Setup  = thisSetup.get_fullname()
RoutineName = dname
SetupName   = sname
#print Path2Setup
#print RoutineName
#print SetupName

# Clear data
iccap_func("../Idsat","Clear Data/Both")
iccap_func("../Ibs","Clear Data/Both")
iccap_func("../Igs","Clear Data/Both")
#--- Measure Idsat
Idsat_Values_List = []
Ibs_Values_List = []
Igs_Values_List = []
print("After Stressd 0 s: Simulating Idsat...")
iccap_func("../Idsat","Simulate")
id = Output("../Idsat/id")
#print id.get_val()[('S','11')][0]
Idsat_Values_List.append(id.get_val()[('S','11')][0].real)
print("After Stressd 0 s: Simulating Ibs...")
iccap_func("../Ibs","Simulate")
ibs = Output("../Ibs/ibs")
#print id.get_val()[('S','11')][0]
Ibs_Values_List.append(ibs.get_val()[('S','11')][0].real)
print("After Stressd 0 s: Simulating Igs...")
iccap_func("../Igs","Simulate")
igs = Output("../Igs/igs")
#print id.get_val()[('S','11')][0]
Igs_Values_List.append(igs.get_val()[('S','11')][0].real)
filename.set_val("0s_")
print(filename.get_val())
print("After Stressd 0 s: Simulate IdVd ...")
iccap_func("../IdVd","Simulate")
iccap_func("../IdVd/export_mea_simulation","Execute")
print("IdVd mea file is saved!")
print("After Stressd 0 s: Simulate IdVg ...")
iccap_func("../IdVg","Simulate")
iccap_func("../IdVg/export_mea_simulation","Execute")
print("IdVg mea file is saved!")
print("After Stressd 0 s: Simulate IbVg ...")
iccap_func("../IbVg","Simulate")
iccap_func("../IbVg/export_mea_simulation","Execute")
print("IbVg mea file is saved!")
print("After Stressd 0 s: Simulate IgVg ...")
iccap_func("../IgVg","Simulate")
iccap_func("../IgVg/export_mea_simulation","Execute")
print("IgVg mea file is saved!")


# --- Time = 0 data output ---
print("Time = 0s, idsat: {}".format(Idsat_Values_List[0].real))
print("Time = 0s, ibs: {}".format(Ibs_Values_List[0].real))
print("Time = 0s, igs: {}".format(Igs_Values_List[0].real))
#print range(0, len(Stress_Time_Values))

for i in range(0, len(Stress_Time_Values)):
    if i==0:
        stresstime = Stress_Time_Values[i]
        timestep = stresstime/10
        if timestep > 65:
            timestep = 65 # the Interval Range is [0.0001, 65.535]
#            print"Time Step is changed to: {} [sec]".format(timestep)        
    else:
        stresstime = Stress_Time_Values[i] - Stress_Time_Values[i-1]
        timestep = stresstime/10
        if timestep > 65:
            timestep = 50 # the Interval Range is [0.0001, 65.535]
#            print"Time Step is changed to: {} [sec]".format(timestep)

    #--- Change the stress time input conditions
    print("Time Stop is changed to: {}, Time Step is changed to: {} [sec]".format(stresstime, timestep))
    iccap_func("../stress/time","STFV",["Stop",stresstime])
    iccap_func("../stress/time","STFV",["Step Size",timestep])
    iccap_func("../stress/time","Redisplay")

    #--- Clear data
    iccap_func("../stress","Clear Data/Both")
    #--- Run Stress measurement
    print("Simulating stress...")
    iccap_func("../stress","Simulate")

    #--- Clear data
    iccap_func("../Idsat","Clear Data/Both")
    #--- file name update
#    print str(Stress_Time_Values[i])+"s_"
    filename.set_val(str(Stress_Time_Values[i])+"s_")

    #--- Measure Idsat
    print("After Stressd {} s: Simulating Idsat...".format(stresstime))
    iccap_func("../Idsat","Simulate")
    iccap_func("../Ibs","Simulate")
    iccap_func("../Igs","Simulate")
    print("After Stressd {} s: Simulate IdVd ...".format(stresstime))
    iccap_func("../IdVd","Simulate")
    iccap_func("../IdVd/export_mea_simulation","Execute")
    print("IdVd mea file is saved!")
    print("After Stressd {} s: Simulate IdVg ...".format(stresstime))
    iccap_func("../IdVg","Simulate")
    iccap_func("../IdVg/export_mea_simulation","Execute")
    print("IdVg mea file is saved!")
    print("After Stressd {} s: Simulate IbVg ...".format(stresstime))
    iccap_func("../IbVg","Simulate")
    iccap_func("../IbVg/export_mea_simulation","Execute")
    print("IbVg mea file is saved!")
    print("After Stressd {} s: Simulate IgVg ...".format(stresstime))
    iccap_func("../IgVg","Simulate")
    iccap_func("../IgVg/export_mea_simulation","Execute")
    print("IgVg mea file is saved!")

    #Store data in the Routine
    id = Output("../Idsat/id")
    Idsat_Values_List.append(id.get_val()[('S','11')][0].real)
    print("Time = {} s, idsat: {}".format(Stress_Time_Values[i],Idsat_Values_List[i+1]))
    ibs = Output("../Ibs/ibs")
    Ibs_Values_List.append(ibs.get_val()[('S','11')][0].real)
    print("Time = {} s, ibs: {}".format(Stress_Time_Values[i],Ibs_Values_List[i+1]))
    igs = Output("../Igs/igs")
    Igs_Values_List.append(igs.get_val()[('S','11')][0].real)
    print("Time = {} s, igs: {}".format(Stress_Time_Values[i],Igs_Values_List[i+1]))

    iccap_func("../stress","Close All")

Idsat_Values_str = ','.join([str(i) for i in Idsat_Values_List])
#print Idsat_Values_str
Idsat_Values.set_val(Idsat_Values_str)
Ibs_Values_str = ','.join([str(i) for i in Ibs_Values_List])
#print Ibs_Values_str
Ibs_Values.set_val(Ibs_Values_str)
Igs_Values_str = ','.join([str(i) for i in Igs_Values_List])
#print Idsat_Values_str
Igs_Values.set_val(Igs_Values_str)
Stress_Time_Values.insert(0, 0.0)

# Plots
model_name = icfuncs.who_is('../../.')
dut_name = icfuncs.who_is('../.')
date = get_var(model_name+'/Date')
temp = float(get_var(model_name+'/Temperature'))
die_index = get_var(model_name+'/Die')
dev_type = get_var(model_name+'/DevPolarity') 
w_value = round(float(get_var(model_name+'/W'))*1e6,5)
l_value = round(float(get_var(model_name+'/L'))*1e6,5)
DeviceName_str = get_var(model_name+'/DeviceName') 
Subsite_str = get_var(model_name+'/Subsite') 
#print (wproapi.get_measurement_group_name())
#Device_Dir = "P5_" + "W" + str(w_value) + "L" + str(L_value)+ ""# define Device data saved dir
Device_Dir = Subsite_str + "_" + DeviceName_str
filePath = get_var(dut_name+'/Mea_Data_Save_Dir')+'\\'+die_index+'\\'+dev_type+'\\'+Device_Dir+'\\'
fileName = '/Stress_Test_W{}_L{}.png'.format(w_value, l_value)

# Setting Plots size
fig=plt.figure(num='Stress Test',figsize=(21,8))
#fig.canvas.manager.set_window_title('Stress Test')
# rect can set plot site. [L, D, W, H]
rect1 = [0.10, 0.10, 0.25, 0.80] 
rect2 = [0.40, 0.10, 0.25, 0.80]
rect3 = [0.70, 0.10, 0.25, 0.80]

# Plots Idsat vs Time
ax1 = plt.axes(rect1)
x = Stress_Time_Values
#print x
y = Idsat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time")
plt.ylabel("Idsat")
plt.title("Idsat vs Time")
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Ibs vs Time
ax2 = plt.axes(rect2)
x = Stress_Time_Values
#print x
y = Ibs_Values_List
#print y
plt.plot(x, y, color='r',marker='o',linestyle='dashed')
plt.xlabel("Time")
plt.ylabel("Ibs")
plt.title("Ibs vs Time")
#plt.savefig(filePath+'/Ibs_vs_Time.png')
#plt.show()
#plt.close()

# Plots Igs vs Time
ax3 = plt.axes(rect3)
x = Stress_Time_Values
#print x
y = Igs_Values_List
#print y
plt.plot(x, y, color='g',marker='o',linestyle='dashed')
plt.xlabel("Time")
plt.ylabel("Igs")
plt.title("Igs vs Time")
#plt.savefig(filePath+'/Igs_vs_Time.png')
#plt.show()
#plt.close()

plt.savefig(filePath+fileName)
#plt.show()
plt.close()
print("Plots have been saved: %s" %(filePath+fileName))

# Save Stress Idsat vs Time data
iccap_func("save_stress_data","Execute")

print("Idsat Simulation with stress were done.")
