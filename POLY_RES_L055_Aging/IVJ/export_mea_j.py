from iccap import *
import os
import time
indicator = 'J'
def genMEA1(write_tmp, setup_name, x_name, y1_name,y2_name,y3_name):
    import iccap
#    print(0)
    x_data = iccap.get_dataset(setup_name +'/'+ x_name, True)[('M','11')]
#    print(1)
    y1_data = iccap.get_dataset(setup_name +'/'+ y1_name, True)[('M','11')]
#    print(2)
    y2_data = iccap.get_dataset(setup_name +'/'+ y2_name, True)[('M','11')]
#    print(3)
    y3_data = iccap.get_dataset(setup_name +'/'+ y3_name, True)[('M','11')]

    for x, y1,y2,y3 in zip(x_data, y1_data, y2_data, y3_data):
            write_tmp += '%s\t%s\t%s\t%s\n' %(x.real, y1.real, y2.real, y3.real)
    return write_tmp

model_name = icfuncs.who_is('../../.')
#date = get_var(model_name+'/Date')
date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
temp = float(get_var(model_name+'/Temperature'))
die_index = get_var(model_name+'/Die')
# w_value = float(get_var(model_name+'/W_ab'))
# l_value = float(get_var(model_name+'/L_ab'))
DeviceName_str = get_var(model_name+'/DeviceName')
Subsite_str = get_var(model_name+'/Subsite')
#print (wproapi.get_measurement_group_name())
#Device_Dir = "P5_" + "W" + str(w_value) + "L" + str(L_value)+ ""# define Device data saved dir
Device_Dir = Subsite_str + "_" + DeviceName_str
Lot_str = get_var(model_name+'/Lot')
Wafer_str = get_var(model_name+'/Wafer')

dut_name = icfuncs.who_is('../.')


stresstime = float(get_var('../runPolyaging/Tot_Stress_Time'))

write_tmp = 'condition{corner = tt,date =%s,instrument=(WaferProExpress2018),mode=forward}\n' %(date)
#export IdlinVgsVbs
#write_tmp += 'Page (name=IVA, x=I, y=V) {W=%s,L=%s,T=%s} stress(time= %s)\n' %(w_value,l_value,temp,stresstime)
write_tmp += 'Page (name=IV{}'.format(indicator)+ 'x=I, y=V) {T=%s}\n' %(temp)
setup_name = dut_name + '/IV{}'.format(indicator)
write_tmp = genMEA1(write_tmp, setup_name, 'ih', 'v','inwell','ipwell')

filePath = get_var(dut_name+'/Mea_Data_Save_Dir')+'\\'+Lot_str+'\\'+Wafer_str+'\\'+str(temp)+'c\\'+die_index+'\\'+Device_Dir+'\\'
instanceInfo = indicator
fileName = get_var('../runPolyaging/filename')+instanceInfo+'stress_{}'.format(stresstime)+'_IV'+'.mea'
#print get_var('../test_flow/filename')
#print fileName
outfilename = filePath + fileName

if not os.path.exists(filePath):
    os.makedirs(filePath)
    with open(outfilename,"w") as f:
        f.write(write_tmp)
        f.close()
else:
    with open(outfilename,"w") as f:
        f.write(write_tmp)
        f.close()

print("file saved: {}".format(outfilename))
