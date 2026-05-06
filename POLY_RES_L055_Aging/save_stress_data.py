from iccap import *
import os


#def save_stress_data(w_value, l_value, nf_value, m_value, temp, die_x, die_y, s_time, s_vgs, s_vds, s_vbs, idsat_list, vtisat_list, idlin_list, vtilin_list, vtgm_list,idoff_list, gmmax_list, ibs_list, igs_list):
def save_stress_data(w_value, l_value, nf_value, m_value, temp, die_x, die_y, s_time, s_vgs, s_vds, s_vbs, s_vsubs, idsat_list, vtisat_list, idlin_list, vtilin_list, vtgm_list,idoff_list, gmmax_list):
    write_tmp=''
    for s_time, idsat, vtisat, idlin, vtilin, vtgm, idoff, gmmax in zip(s_time, idsat_list, vtisat_list, idlin_list, vtilin_list, vtgm_list, idoff_list, gmmax_list):
        write_tmp += '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n' %(w_value, l_value, nf_value, m_value, temp, die_x, die_y, s_time, s_vgs, s_vds, s_vbs, s_vsubs, idsat, vtisat, idlin, vtilin, vtgm, idoff, gmmax)

    return write_tmp

model_name = icfuncs.who_is('../../.')
date = get_var(model_name+'/Date')
temp = float(get_var(model_name+'/Temperature'))
die_index = get_var(model_name+'/Die')
die_x = die_index.split("-Y")[0].replace("X","")
die_y = die_index.split("-Y")[1]
dev_type = get_var(model_name+'/DevPolarity') 
w_value = float(get_var(model_name+'/WF'))
l_value = float(get_var(model_name+'/L'))
nf_value = int(get_var(model_name+'/Nf'))
#m_value = int(get_var(model_name+'/M'))
m_value = 1
DeviceName_str = get_var(model_name+'/DeviceName') 
Subsite_str = get_var(model_name+'/Subsite') 
Lot_str = get_var(model_name+'/Lot') 
Wafer_str = get_var(model_name+'/Wafer') 
#print (wproapi.get_measurement_group_name())
#Device_Dir = "P5_" + "W" + str(w_value) + "L" + str(L_value)+ ""# define Device data saved dir
Device_Dir = Subsite_str + "_" + DeviceName_str



dut_name = icfuncs.who_is('../.')
aging_trend_str = get_var(dut_name+'/aging_trend_str')
vdlin = float(get_var(dut_name+'/VDLIN'))
#viw = float(get_var(dut_name+'/Viw'))
#s_time = float(get_var(dut_name+'/Stress_Time_List'))
vgs = float(get_var(dut_name+'/Vgg'))
vds = float(get_var(dut_name+'/Vdd'))
vbs = 0
s_vs = float(get_var(dut_name+'/Vs_stress'))
s_vgs = float(get_var(dut_name+'/Vg_stress'))-s_vs
s_vds = float(get_var(dut_name+'/Vd_stress'))-s_vs
s_vbs = float(get_var(dut_name+'/Vb_stress'))-s_vs
#s_viws = float(get_var(dut_name+'/Viw_stress'))-s_vs
s_vsubs = float(get_var(dut_name+'/Vsub_stress'))-s_vs
Idsat_Values = [float(i) for i in SVar("Idsat_Values").get_val().split(",")]
Idlin_Values = [float(i) for i in SVar("Idlin_Values").get_val().split(",")]
Vtilin_Values = [float(i) for i in SVar("Vtilin_Values").get_val().split(",")]
Vtisat_Values = [float(i) for i in SVar("Vtisat_Values").get_val().split(",")]
Vtgm_Values = [float(i) for i in SVar("Vtgm_Values").get_val().split(",")]
#Ibs_Values = [float(i) for i in SVar("Ibs_Values").get_val().split(",")]
#Igs_Values = [float(i) for i in SVar("Igs_Values").get_val().split(",")]
Gmmax_Values = [float(i) for i in SVar("Gmmax_Values").get_val().split(",")]
Idoff_Values = [float(i) for i in SVar("Idoff_Values").get_val().split(",")]
Stress_Time_Values = [float(i) for i in DVar("Stress_Time_List").get_val().split(",")]
keyval = SVar("keyval").get_val()
Stress_Time_Values.insert(0, 0.0)
#print Idsat_Values
#print Stress_Time_Values

s_time = Stress_Time_Values
idsat_list = Idsat_Values
idlin_list = Idlin_Values
vtilin_list = Vtilin_Values
vtisat_list = Vtisat_Values
vtgm_list = Vtgm_Values
#ibs_list = Ibs_Values
#igs_list = Igs_Values
gmmax_list = Gmmax_Values
idoff_list = Idoff_Values

# write header to file
write_tmp0 = 'condition{corner = tt,date =%s,instrument=(WaferProExpress2018),mode=forward}\n' %(date)
write_tmp0 += 'Datatype{S_target}\n'
write_tmp0 += 'Version{2.0}\n'
write_tmp0 += 'type{%s}\n' %(devType)
write_tmp0 += 'Delimiter{,}\n'
write_tmp0 += 'Instance{w,l,nf,m,t,diex,diey}\n'
write_tmp0 += 'Stress_Condition{s_time=%s,s_vgs=%s,s_vds=%s,s_vbs=%s,s_vsubs=%s,s_vs=%s}\n' %(Stress_Time_Values[-1],s_vgs*type, s_vds*type, s_vbs*type ,s_vsubs*type,s_vs*type)
write_tmp0 += 'Input{vgg=%s,vdd=%s,vbb=0,vdlin=%s,}\n' %(vgs*type, vds*type,vdlin*type)
write_tmp0 += 'Data{w,l,nf,m,t,diex,diey,s_time,s_vgs,s_vds,s_vbs,s_vsubs,idsat,vtcon_sat,idlin,vtcon_lin,vth_gm,idoff,gmmax}\n'

write_tmp1 = save_stress_data(w_value, l_value, nf_value, m_value, temp, die_x, die_y, s_time, s_vgs*type, s_vds*type, s_vbs*type, s_vsubs*type, idsat_list, vtisat_list, idlin_list, vtilin_list, vtgm_list,idoff_list, gmmax_list)

#print write_tmp0
#print write_tmp1

filePath = get_var(dut_name+'/Mea_Data_Save_Dir')+'\\'+Lot_str+'\\'+Wafer_str+'\\'+str(temp)+'c\\'+die_index+'\\'+dev_type+'\\'+Device_Dir+'\\'
#fileName = 'stress_hci'+'.mea'
fileName = '/{}_{}_w{}_{}_{}_{}x{}nf{}m{}_HCI_{}_{}C_die_{}_{}_Vd{}_Vg{}_Vb{}_Vsub{}.mea'.format(keyval,Lot_str,Wafer_str,Subsite_str, DeviceName_str, w_value, l_value, nf_value, m_value,aging_trend_str,temp,die_x, die_y, s_vds*type, s_vgs*type, s_vbs*type, s_vsubs*type)
outfilename = filePath + fileName

#Write File
if os.path.exists(outfilename):
    with open(outfilename,"a") as f:
        f.write(write_tmp1)
        f.close()
else:
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    with open(outfilename,"w") as f:
        f.write(write_tmp0)
        f.write(write_tmp1)
        f.close()

keyFile = get_var(dut_name+'/Mea_Data_Save_Dir')+'\mea_dict.csv'
#Add key element to mea_dict
if not os.path.exists(keyFile):
     with open(keyFile,"w") as f:
        f.write("Key,Dp Stress File,Meas Date\n" )
        f.close()
with open(keyFile,"a") as f:
    f.write(keyval+","+filePath+fileName+","+date+"\n")
    f.close()

print("Data files have been saved: {}".format(outfilename))



