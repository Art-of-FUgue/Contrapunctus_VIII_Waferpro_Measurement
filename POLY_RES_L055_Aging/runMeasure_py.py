# update: explicit
from iccap import *
import matplotlib.pyplot as plt
from iccap import icfuncs as f
import numpy as np
from icutils import icfoms
#import secrets
import pandas as pd

# Function to add new element to Dictionary
def setNewDictElement(keydict,value):
    
    return keyval, keydict

# called by WPE Routine
Debug         = MVar("Debug")         #ModelVariable, WaferPro Debug Level
Mode          = MVar("Mode")          #ModelVariable, WaferPro Run Mode
bRet          = MVar("bRet")          #Setup/ModelVariable, WaferPro Success(=1)/Nonsuccess(=0) Flag
ErrorMsg      = MVar("ErrorMsg")      #Setup/ModelVariable, Error Message sent to WaferPro when Nonsuccess

Vs1     = DVar("Vs1")
Vd1     = DVar("Vd1")
Vs2     = DVar("Vs1")
Vd2     = DVar("Vd1")
Vs3     = DVar("Vs1")
Vd3     = DVar("Vd1")
I_stress1     = DVar("I_stress1")
I_stress2     = DVar("I_stress2")
I_stress3     = DVar("I_stress3")
#Viw_stress     = DVar("Viw_stress")
Vsub_stress     = DVar("Vsub_stress")
SweepType     = DVar("sweeptype")
Stress_Time_List = DVar("Stress_Time_List")
Vtisat_Values = SVar("Vtisat_Values")
Vtilin_Values = SVar("Vtilin_Values")
Vtgm_Values = SVar("Vtgm_Values")
Idsat_Values = SVar("Idsat_Values")
Idlin_Values = SVar("Idlin_Values")
#Ibs_Values = SVar("Ibs_Values")
#Igs_Values = SVar("Igs_Values")
Gmmax_Values = SVar("Gmmax_Values")
Idoff_Values = SVar("Idoff_Values")
Tot_Stress_Time = SVar("Tot_Stress_Time")
filename = SVar("filename") 
savepath = SVar("Mea_Data_Save_Dir")
keyval = SVar("keyval")
vb_value = 0
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
model_name = icfuncs.who_is('../../.')
dut_name = icfuncs.who_is('../.')
w_value = round(float(get_var(model_name+'/WF'))*1e6,5)
l_value = float(get_var(model_name+'/L'))*1e6
nf_value = int(get_var(model_name+'/Nf'))


#Set new key for file name prefix. 
mea_file_name= savepath.get_val()+"\mea_dict.csv"
if os.path.exists(mea_file_name):
    with open(savepath.get_val()+"\mea_dict.csv",'r') as f:
        keydict =  pd.read_csv(f).to_dict()
        f.close()

    new_key = 0
    while new_key == 0:
#        new_keyval = secrets.token_hex(3)
        new_keyval=os.urandom(3).hex()
        if new_keyval not in keydict.keys():
            keyval.set_val(new_keyval)
            new_key = 1
else:
    #keyval.set_val(secrets.token_hex(3))
    keyval.set_val(os.urandom(3).hex())

# Clear data
iccap_func("../IdVgVdsat","Clear Data/Both")
iccap_func("../IdVgVdlin","Clear Data/Both")
#iccap_func("../Ibs","Clear Data/Both")
#iccap_func("../Igs","Clear Data/Both")
iccap_func("../Idoff","Clear Data/Both")

#--- Measure Idsat
Vtisat_Values_List = []
Vtilin_Values_List = []
Vtgm_Values_List = []
Idsat_Values_List = []
Idlin_Values_List = []
#Ibs_Values_List = []
#Igs_Values_List = []
gm_Values_List = []
Idoff_Values_List = []


filename.set_val(str(keyval.get_val())+"_0s_")
Tot_Stress_Time.set_val(0)
print("MEA FILENAME: ",filename.get_val())
#old_mdm_name = mdm_file_name.get_val()
#print("OLD MDM NAME: ",old_mdm_name)
#new_mdm_name = "0s_"+old_mdm_name
#mdm_file_name.set_val(new_mdm_name)
#print("NEW MDM NAME: ",new_mdm_name)


print("After Stressed 0 s: Measure IdVgVdsat...")
iccap_func("../IdVgVdsat","Measure")
id_sat = Output("../IdVgVdsat/id")
vg_sat = Input("../IdVgVdsat/vg")
#print id.get_val()[('M','11')][0]
Idsat_Values_List.append(id_sat.get_val()[('M','11')][-1].real)
#Idoff_Values_List.append(id_sat.get_val()[('M','11')][0].real)
#iccap_func("../IdVgVdsat/CalcVth","Execute")
vtisat = get_vthi(iForVti, vg_sat, id_sat, vb_value, w_value, l_value, nf_value, m_value, type)
#vtisat = FET.vti(id_sat,vg_sat,vb_value,len(vg_lin),len(vb_value),[iForVti,w_value*nf_value*m_value,l_value,type,Debug.get_val()])
Vtisat_Values_List.append(vtisat)
iccap_func("../IdVgVdsat/export_mea","Execute")

print("After Stressed 0 s: Measure IdVgVdlin...")
iccap_func("../IdVgVdlin","Measure")
id_lin = Output("../IdVgVdlin/id")
vg_lin = Input("../IdVgVdlin/vg")

Idlin_Values_List.append(id_lin.get_val()[('M','11')][-1].real)
#iccap_func("../IdVgVdlin/CalcVth","Execute")
vtilin = get_vthi(iForVti, vg_lin, id_lin, vb_value, w_value, l_value, nf_value, m_value, type)
#vtilin = FET.vti(id_lin,vg_lin,vb_value,len(vg_lin),len(vb_value),[iForVti,w_value*nf_value*m_value,l_value,type,Debug.get_val()])
Vtilin_Values_List.append(vtilin)
[vtgm,gmmax] = get_vthgm(vg_lin, id_lin, vdlin, type)
#vtgm=FET.vth_gmmax("M",{"setup_name":"../IdVgVdlin"},Debug.get_val())
#gmmax= FET.gmmax("M",{"setup_name":"../IdVgVdlin"},Debug.get_val())
Vtgm_Values_List.append(vtgm)
gm_Values_List.append(gmmax)
iccap_func("../IdVgVdlin/export_mea","Execute")

print("After Stressed 0 s: Measure Idoff...")
iccap_func("../Idoff","Measure")
id_off = Output("../Idoff/id")
#print id.get_val()[('M','11')][0]
Idoff_Values_List.append(id_off.get_val()[('M','11')][0].real)

print("After Stressed 0 s: Measure IdVd ...")
iccap_func("../IdVd","Measure")
iccap_func("../IdVd/export_mea","Execute")
print("IdVd mea file is saved!")

#print("After Stressed 0 s: Measure Ibs...")
#iccap_func("../Ibs","Measure")
#ibs = Output("../Ibs/ib")
#print id.get_val()[('M','11')][0]
#Ibs_Values_List.append(ibs.get_val()[('M','11')][0].real)
#print("After Stressed 0 s: Measure Igs...")
#iccap_func("../Igs","Measure")
#igs = Output("../Igs/ig")
#print id.get_val()[('M','11')][0]
#Igs_Values_List.append(igs.get_val()[('M','11')][0].real)




# --- Time = 0 data output ---
print("Time = 0s, vtilin: {}".format(Vtilin_Values_List[0]))
print("Time = 0s, vtgm: {}".format(Vtgm_Values_List[0]))
print("Time = 0s, idlin: {}".format(Idlin_Values_List[0].real))
print("Time = 0s, vtisat: {}".format(Vtisat_Values_List[0]))
print("Time = 0s, idsat: {}".format(Idsat_Values_List[0].real))
#print("Time = 0s, ibs: {}".format(Ibs_Values_List[0].real))
#print("Time = 0s, igs: {}".format(Igs_Values_List[0].real))
print("Time = 0s, idoff: {}".format(Idoff_Values_List[0]))
print("Time = 0s, gmmax: {}".format(gm_Values_List[0]))
#print range(0, len(Stress_Time_Values))

for i in range(0, len(Stress_Time_Values)):
    if i==0:
        stresstime = Stress_Time_Values[i]
        timestep = stresstime/10
        if timestep > 10:
            timestep = 10 # the Interval Range is [0.0001, 65.535]
#            print"Time Step is changed to: {} [sec]".format(timestep)        
    else:
    
        stresstime = Stress_Time_Values[i] - Stress_Time_Values[i-1]
        
        timestep = stresstime/10
        if timestep > 10:
            timestep = 10 # the Interval Range is [0.0001, 65.535]
            
#            print"Time Step is changed to: {} [sec]".format(timestep)
    
    #--- Change the stress time input conditions
    print("Time Stop is changed to: {}, Time Step is changed to: {} [sec]".format(stresstime, timestep))
    iccap_func("../stress/time","STFV",["Stop",stresstime])
    iccap_func("../stress/time","STFV",["Step Size",timestep])
    iccap_func("../stress/time","Redisplay")
    Tot_Stress_Time.set_val(Stress_Time_Values[i])

    #--- file name update
#    print str(Stress_Time_Values[i])+"s_"
    filename.set_val(str(keyval.get_val())+"_"+str(Stress_Time_Values[i])+"s_")

    #--- Clear data
    iccap_func("../stress","Clear Data/Both")
    #--- Run Stress measurement
    #new_mdm_name = str(stresstime)+"s_"+old_mdm_name
    #mdm_file_name.set_val(new_mdm_name)
    #print("NEW MDM NAME: ",new_mdm_name)    
    print("Measure stress...")
    iccap_func("../stress","Measure")
    iccap_func("../stress/export_mea","Execute")
    iccap_func("../stress","Close All")

    #--- Clear data
    iccap_func("../IdVgVdsat","Clear Data/Both")
    iccap_func("../IdVgVdlin","Clear Data/Both")
    iccap_func("../Ibs","Clear Data/Both")
    iccap_func("../Igs","Clear Data/Both")
    

    
    
    #--- Measure Idsat
    print("After Stressed {} s: Measure IdVgVdsat...".format(stresstime))
    iccap_func("../IdVgVdsat","Measure")
    #print id.get_val()[('M','11')][0]
    #iccap_func("../IdVgVdsat/CalcVth","Execute")
    iccap_func("../IdVgVdsat/export_mea","Execute") 

    #--- Measure Idlin
    print("After Stressed {} s: Measure IdVgVdlin...".format(stresstime))
    iccap_func("../IdVgVdlin","Measure")
    id_lin = Output("../IdVgVdlin/id")
   
    Idlin_Values_List.append(id_lin.get_val()[('M','11')][-1].real)
    print("Time = {} s, idlin: {}".format(Stress_Time_Values[i],Idlin_Values_List[i+1]))    
    #print id.get_val()[('M','11')][0]
    #iccap_func("../IdVgVdlin/CalcVth","Execute")
    iccap_func("../IdVgVdlin/export_mea","Execute")    
       
    print("After Stressed {} s: Measure Idoff ...".format(stresstime))
    iccap_func("../Idoff","Measure")

    print("After Stressed {} s: Measure IdVd ...".format(stresstime))
    iccap_func("../IdVd","Measure")
    iccap_func("../IdVd/export_mea","Execute")
    print("IdVd mea file is saved!")

    #iccap_func("../Ibs","Measure")
    #iccap_func("../Igs","Measure")
    

    #Store data in the Routine
   
    vg_lin = Input("../IdVgVdlin/vg")
    vtilin = get_vthi(iForVti, vg_lin, id_lin, vb_value, w_value, l_value, nf_value, m_value, type)
    #vtilin = FET.vti(id_lin,vg_lin,vb_value,len(vg_lin),len(vb_value),[iForVti,w_value*nf_value*m_value,l_value,type,Debug.get_val()])
    Vtilin_Values_List.append(vtilin)
    print("Time = {} s, vtilin: {}".format(Stress_Time_Values[i],Vtilin_Values_List[i+1]))
    [vtgm,gmmax] = get_vthgm(vg_lin, id_lin, vdlin, type)
    #vtgm=FET.vth_gmmax("M",{"setup_name":"../IdVgVdlin"},Debug.get_val())
    #gmmax= FET.gmmax("M",{"setup_name":"../IdVgVdlin"},Debug.get_val())
    Vtgm_Values_List.append(vtgm)
    gm_Values_List.append(gmmax)
    print("Time = {} s, vtgm: {}".format(Stress_Time_Values[i],Vtgm_Values_List[i+1]))
    print("Time = {} s, gmmax: {}".format(Stress_Time_Values[i],gm_Values_List[i+1]))

    id_sat = Output("../IdVgVdsat/id")
    vg_sat = Input("../IdVgVdsat/vg")
    vtisat = get_vthi(iForVti, vg_sat, id_sat, vb_value, w_value, l_value, nf_value, m_value, type)
    #vtisat = FET.vti(id_sat,vg_sat,vb_value,len(vg_lin),len(vb_value),[iForVti,w_value*nf_value*m_value,l_value,type,Debug.get_val()])
    Vtisat_Values_List.append(vtisat)  
    print("Time = {} s, vtisat: {}".format(Stress_Time_Values[i],Vtisat_Values_List[i+1]))
    Idsat_Values_List.append(id_sat.get_val()[('M','11')][-1].real)
    print("Time = {} s, idsat: {}".format(Stress_Time_Values[i],Idsat_Values_List[i+1]))
    id_off = Output("../Idoff/id")
    Idoff_Values_List.append(id_off.get_val()[('M','11')][0].real)
    print("Time = {} s, idoff: {}".format(Stress_Time_Values[i],Idoff_Values_List[i+1]))
    #ibs = Output("../Ibs/ib")
    #Ibs_Values_List.append(ibs.get_val()[('M','11')][0].real)
    #print("Time = {} s, ibs: {}".format(Stress_Time_Values[i],Ibs_Values_List[i+1]))
    #igs = Output("../Igs/ig")
    #Igs_Values_List.append(igs.get_val()[('M','11')][0].real)
    #print("Time = {} s, igs: {}".format(Stress_Time_Values[i],Igs_Values_List[i+1]))
    


Vtisat_Values_str = ','.join([str(i) for i in Vtisat_Values_List])
#print Idsat_Values_str
Vtisat_Values.set_val(Vtisat_Values_str)

Vtilin_Values_str = ','.join([str(i) for i in Vtilin_Values_List])
#print Idsat_Values_str
Vtilin_Values.set_val(Vtilin_Values_str)

Vtgm_Values_str = ','.join([str(i) for i in Vtgm_Values_List])
#print Idsat_Values_str
Vtgm_Values.set_val(Vtgm_Values_str)

Idlin_Values_str = ','.join([str(i) for i in Idlin_Values_List])
#print Idsat_Values_str
Idlin_Values.set_val(Idlin_Values_str)

Idsat_Values_str = ','.join([str(i) for i in Idsat_Values_List])
#print Idsat_Values_str
Idsat_Values.set_val(Idsat_Values_str)
#Ibs_Values_str = ','.join([str(i) for i in Ibs_Values_List])
#print Ibs_Values_str
#Ibs_Values.set_val(Ibs_Values_str)
#Igs_Values_str = ','.join([str(i) for i in Igs_Values_List])
#print Idsat_Values_str
#Igs_Values.set_val(Igs_Values_str)

Idoff_Values_str = ','.join([str(i) for i in Idoff_Values_List])
Idoff_Values.set_val(Idoff_Values_str)

gm_Values_str = ','.join([str(i) for i in gm_Values_List])
Gmmax_Values.set_val(gm_Values_str)
Stress_Time_Values.insert(0, 0.0)

# Plots
model_name = icfuncs.who_is('../../.')
dut_name = icfuncs.who_is('../.')
date = get_var(model_name+'/Date')
temp = float(get_var(model_name+'/Temperature'))
die_index = get_var(model_name+'/Die')
dev_type = get_var(model_name+'/DevPolarity') 
w_value = float(get_var(model_name+'/WF'))
l_value = float(get_var(model_name+'/L'))
nf_value = int(get_var(model_name+'/Nf'))
#m_value = int(get_var(model_name+'/M'))
m_value=1
DeviceName_str = get_var(model_name+'/DeviceName') 
Subsite_str = get_var(model_name+'/Subsite') 
Lot_str = get_var(model_name+'/Lot') 
Wafer_str = get_var(model_name+'/Wafer') 
s_vs = float(get_var(dut_name+'/Vs_stress'))
s_vgs = float(get_var(dut_name+'/Vg_stress'))-s_vs
s_vds = float(get_var(dut_name+'/Vd_stress'))-s_vs
s_vbs = float(get_var(dut_name+'/Vb_stress'))-s_vs
#s_viw = float(get_var(dut_name+'/Viw_stress'))-s_vs
s_vsub = float(get_var(dut_name+'/Vsub_stress'))-s_vs
#print (wproapi.get_measurement_group_name())
#Device_Dir = "P5_" + "W" + str(w_value) + "L" + str(L_value)+ ""# define Device data saved dir
Device_Dir = Subsite_str + "_" + DeviceName_str

Title_Str=DeviceName_str+",W="+str(w_value)+",L="+str(l_value)+",NF="+str(nf_value)+",M="+str(m_value)+",T="+str(temp)+"\nVdstress="+str(s_vds*type)+",Vgstress="+str(s_vgs*type)+",Vbstress="+str(s_vbs*type)+",Vsubstress="+str(s_vsub*type)+"\n"+str(Lot_str)+" wf"+str(Wafer_str)
#filePath = get_var(dut_name+'/Mea_Data_Save_Dir')+'\\'+die_index+'\\'+dev_type+'\\'+Device_Dir+'\\'
filePath = get_var(dut_name+'/Mea_Data_Save_Dir')+'\\'+Lot_str+'\\'+Wafer_str+'\\'+str(temp)+'c\\'+die_index+'\\'+dev_type+'\\'+Device_Dir+'\\'
fileName = '/'+keyval.get_val()+'_Raw_Stress_Test_Secs_W{}_L{}.png'.format(w_value, l_value)
# Setting Plots size
fig=plt.figure(num='Raw Stress Test',figsize=(21,16))
#fig.canvas.manager.set_window_title('Stress Test')
# rect can set plot site. [L, D, W, H]
rect1 = [0.10, 0.5, 0.25, 0.3] 
rect2 = [0.40, 0.5, 0.25, 0.3]
rect3 = [0.70, 0.5, 0.25, 0.3]
rect4 = [0.10, 0.1, 0.25, 0.3] 
rect5 = [0.40, 0.1, 0.25, 0.3]
rect6 = [0.70, 0.1, 0.25, 0.3]



# Plots Idlin vs Time
ax1 = plt.axes(rect1)
ax1.set_xscale('log')
x = Stress_Time_Values
#print x
y = Idlin_Values_List
Idlin_t0 = Idlin_Values_List[0]
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("Idlin[A]")
plt.title("Idlin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtilin vs Time
ax2 = plt.axes(rect2)
ax2.set_xscale('log')
x = Stress_Time_Values
#print x
y = Vtilin_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("Vtilin[V]")
plt.title("Vtilin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Idsat vs Time
ax3 = plt.axes(rect3)
ax3.set_xscale('log')
x = Stress_Time_Values
#print x
y = Idsat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("Idsat[A]")
plt.title("Idsat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtisat vs Time
ax4 = plt.axes(rect4)
ax4.set_xscale('log')
x = Stress_Time_Values
#print x
y = Vtisat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("Vtisat[V]")
plt.title("Vtisat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots gm vs Time
ax5 = plt.axes(rect5)
ax5.set_xscale('log')
x = Stress_Time_Values
#print x
y = gm_Values_List
#print y
plt.plot(x, y, color='r',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("Gmmax[S]")
plt.title("Gmmax vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Ibs_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtgm vs Time
ax6 = plt.axes(rect6)
ax6.set_xscale('log')
x = Stress_Time_Values
#print x
y = Vtgm_Values_List
#print y
plt.plot(x, y, color='g',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("Vtgm[V]")
plt.title("Vtgm vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Igs_vs_Time.png')
#plt.show()
#plt.close()

plt.savefig(filePath+fileName)
#plt.show()
plt.close(fig)
print("Raw Plots (seconds) have been saved: %s" %(filePath+fileName))

fileName = '/'+keyval.get_val()+'_Raw_Stress_Test_Hrs_W{}_L{}.png'.format(w_value, l_value)
# Setting Plots size
fig=plt.figure(num='Raw Stress Test Hours',figsize=(21,16))
# Plots Idlin vs Time
ax1 = plt.axes(rect1)
ax1.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
y = Idlin_Values_List
Idlin_t0 = Idlin_Values_List[0]
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("Idlin[A]")
plt.title("Idlin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtilin vs Time
ax2 = plt.axes(rect2)
ax2.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
y = Vtilin_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("Vtilin[V]")
plt.title("Vtilin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Idsat vs Time
ax3 = plt.axes(rect3)
ax3.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
y = Idsat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("Idsat[A]")
plt.title("Idsat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtisat vs Time
ax4 = plt.axes(rect4)
ax4.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
y = Vtisat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("Vtisat[V]")
plt.title("Vtisat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots gm vs Time
ax5 = plt.axes(rect5)
ax5.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
y = gm_Values_List
#print y
plt.plot(x, y, color='r',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("Gmmax[S]")
plt.title("Gmmax vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Ibs_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtgm vs Time
ax6 = plt.axes(rect6)
ax6.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
y = Vtgm_Values_List
#print y
plt.plot(x, y, color='g',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("Vtgm[V]")
plt.title("Vtgm vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Igs_vs_Time.png')
#plt.show()
#plt.close()

plt.savefig(filePath+fileName)
#plt.show()
plt.close(fig)
print("Raw Plots (hours) have been saved: %s" %(filePath+fileName))


deltafileName = '/'+keyval.get_val()+'_Delta_Stress_Test_Secs_W{}_L{}.png'.format(w_value, l_value)
# Setting Plots size
fig=plt.figure(num='Delta Stress Test',figsize=(21,16))
#fig.canvas.manager.set_window_title('Stress Test')

# Plots Idlin vs Time
ax1 = plt.axes(rect1)
ax1.set_xscale('log')
x = Stress_Time_Values
#print x
dIdlin_Values_List = []
for val in Idlin_Values_List:
    dIdlin_Values_List.append((val-Idlin_Values_List[0])/Idlin_Values_List[0]*100)
y = dIdlin_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("dIdlin[%]")
plt.title("dIdlin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtilin vs Time
ax2 = plt.axes(rect2)
ax2.set_xscale('log')
x = Stress_Time_Values
#print x
dVthlin_Values_List = []
for val in Vtilin_Values_List:
    dVthlin_Values_List.append((val-Vtilin_Values_List[0])*1e3)
y = dVthlin_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("dVtilin[mV]")
plt.title("dVtilin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Idsat vs Time
ax3 = plt.axes(rect3)
ax3.set_xscale('log')
x = Stress_Time_Values
#print x
dIdsat_Values_List = []
for val in Idsat_Values_List:
    dIdsat_Values_List.append((val-Idsat_Values_List[0])/Idsat_Values_List[0]*100)
y = dIdsat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("dIdsat[%]")
plt.title("dIdsat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtisat vs Time
ax4 = plt.axes(rect4)
ax4.set_xscale('log')
x = Stress_Time_Values
#print x
dVthsat_Values_List = []
for val in Vtisat_Values_List:
    dVthsat_Values_List.append((val-Vtisat_Values_List[0])*1e3)
y = dVthsat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("dVtisat[mV]")
plt.title("dVtisat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots gm vs Time
ax5 = plt.axes(rect5)
ax5.set_xscale('log')
x = Stress_Time_Values
#print x
dGmmax_Values_List = []
for val in gm_Values_List:
    dGmmax_Values_List.append(val-gm_Values_List[0])
y = dGmmax_Values_List
#print y
plt.plot(x, y, color='r',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("dGmmax[S]")
plt.title("dGmmax vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Ibs_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtgm vs Time
ax6 = plt.axes(rect6)
ax6.set_xscale('log')
x = Stress_Time_Values
#print x
dVtgm_Values_List = []
for val in Vtgm_Values_List:
    dVtgm_Values_List.append((val-Vtgm_Values_List[0])*1e3)
y = dVtgm_Values_List
#print y
plt.plot(x, y, color='g',marker='o',linestyle='dashed')
plt.xlabel("Time[s]")
plt.ylabel("dVtgm[mV]")
plt.title("dVtgm vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Igs_vs_Time.png')
#plt.show()
#plt.close()

plt.savefig(filePath+deltafileName)
#plt.show()
plt.close(fig)
print("Delta Plots (seconds) have been saved: %s" %(filePath+deltafileName))

deltafileName = '/'+keyval.get_val()+'_Delta_Stress_Test_Hrs_W{}_L{}.png'.format(w_value, l_value)
# Setting Plots size
fig=plt.figure(num='Delta Stress Test Hours',figsize=(21,16))
#fig.canvas.manager.set_window_title('Stress Test')

# Plots Idlin vs Time
ax1 = plt.axes(rect1)
ax1.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
dIdlin_Values_List = []
for val in Idlin_Values_List:
    dIdlin_Values_List.append((val-Idlin_Values_List[0])/Idlin_Values_List[0]*100)
y = dIdlin_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("dIdlin[%]")
plt.title("dIdlin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtilin vs Time
ax2 = plt.axes(rect2)
ax2.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
dVthlin_Values_List = []
for val in Vtilin_Values_List:
    dVthlin_Values_List.append((val-Vtilin_Values_List[0])*1e3)
y = dVthlin_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("dVtilin[mV]")
plt.title("dVtilin vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Idsat vs Time
ax3 = plt.axes(rect3)
ax3.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
dIdsat_Values_List = []
for val in Idsat_Values_List:
    dIdsat_Values_List.append((val-Idsat_Values_List[0])/Idsat_Values_List[0]*100)
y = dIdsat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("dIdsat[%]")
plt.title("dIdsat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtisat vs Time
ax4 = plt.axes(rect4)
ax4.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
dVthsat_Values_List = []
for val in Vtisat_Values_List:
    dVthsat_Values_List.append((val-Vtisat_Values_List[0])*1e3)
y = dVthsat_Values_List
#print y
plt.plot(x, y, color='b',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("dVtisat[mV]")
plt.title("dVtisat vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Idsat_vs_Time.png')
#plt.show()
#plt.close()

# Plots gm vs Time
ax5 = plt.axes(rect5)
ax5.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
dGmmax_Values_List = []
for val in gm_Values_List:
    dGmmax_Values_List.append(val-gm_Values_List[0])
y = dGmmax_Values_List
#print y
plt.plot(x, y, color='r',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("dGmmax[S]")
plt.title("dGmmax vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Ibs_vs_Time.png')
#plt.show()
#plt.close()

# Plots Vtgm vs Time
ax6 = plt.axes(rect6)
ax6.set_xscale('log')
x = [ i/3600 for i in Stress_Time_Values]
#print x
dVtgm_Values_List = []
for val in Vtgm_Values_List:
    dVtgm_Values_List.append((val-Vtgm_Values_List[0])*1e3)
y = dVtgm_Values_List
#print y
plt.plot(x, y, color='g',marker='o',linestyle='dashed')
plt.xlabel("Time[Hr]")
plt.ylabel("dVtgm[mV]")
plt.title("dVtgm vs Time\n"+Title_Str)
#plt.savefig(filePath+'/Igs_vs_Time.png')
#plt.show()
#plt.close()

plt.savefig(filePath+deltafileName)
#plt.show()
plt.close(fig)
print("Delta Plots (Hrs) have been saved: %s" %(filePath+deltafileName))
# Save Stress Idsat vs Time data
iccap_func("save_stress_data","Execute")

print("Idsat/Idlin/Vtsat/Vtlin/Vtgm/Idoff Measurement with stress were done.")
