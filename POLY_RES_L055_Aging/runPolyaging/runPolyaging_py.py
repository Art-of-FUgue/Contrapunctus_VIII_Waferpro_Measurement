# update: explicit
from iccap import *
import matplotlib.pyplot as plt
from iccap import icfuncs as f
import numpy as np
import math
from icutils import icfoms
# import secrets
import pandas as pd
import time


# from sklearn.externals.array_api_compat.cupy.fft import ihfft


# Function to add new element to Dictionary
def setNewDictElement(keydict, value):
    return keyval, keydict


Debug = MVar("Debug")  # ModelVariable, WaferPro Debug Level
Mode = MVar("Mode")  # ModelVariable, WaferPro Run Mode
bRet = MVar("bRet")  # Setup/ModelVariable, WaferPro Success(=1)/Nonsuccess(=0) Flag
ErrorMsg = MVar("ErrorMsg")  # Setup/ModelVariable, Error Message sent to WaferPro when Nonsuccess
Type = MVar("Type")  # ModelVariable, polarity factor (1, -1)

IA_stress = DVar("IA_stress")
IB_stress = DVar("IB_stress")
IC_stress = DVar("IC_stress")
Stress_Time_List = DVar("Stress_Time_List")
I_bias_density = DVar("I_bias_density")

bool_a = DVar("bool_a")
bool_b = DVar("bool_b")
bool_c = DVar("bool_c")
bool_d = DVar("bool_d")
bool_e = DVar("bool_e")
bool_f = DVar("bool_f")
bool_g = DVar("bool_g")
bool_h = DVar("bool_h")
bool_i = DVar("bool_i")
bool_j = DVar("bool_j")
s_factor = DVar("s_factor")
Tot_Stress_Time = SVar("Tot_Stress_Time")
filename = SVar("filename")
savepath = SVar("Mea_Data_Save_Dir")
keyval = SVar("keyval")

I_monitor_density = float(I_bias_density.get_val()) * float(s_factor.get_val()) * 1e-3
print("Debug with {}".format(Mode.get_val()))

Stress_Time_Values = [float(i) for i in Stress_Time_List.get_val().split(",")]
# print Stress_Time_Values
# print filename.get_val()

# print Debug.get_val(), Mode.get_val(), bRet.get_val(), Type.get_val(), Vd_stress.get_val()

# --- Define local variables for this Program
thisSetup = Setup(".")
_, mname, dname, sname = thisSetup.get_fullname().split("/")
Path2Setup = thisSetup.get_fullname()
RoutineName = dname
SetupName = sname

model_name = icfuncs.who_is('../../.')
dut_name = icfuncs.who_is('../.')

suffixes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
wl_dict = {}

print("Starting proccess WL...")
for s in suffixes:
    # 1. Access the Dvar for logic
    current_bool = globals()[f"bool_{s}"]

    if current_bool.get_val() == "1":
        # Dynamic extraction for W and L based on suffix 's'
        w_val = float(get_var(f"{model_name}/W_{s}"))
        l_val = float(get_var(f"{model_name}/L_{s}"))
        I_monitor_val = w_val * I_monitor_density * 1e6
        # Store in dictionary
        wl_dict[s] = {"W": w_val, "L": l_val, "I_monitor": I_monitor_val}
        print(f"Captured suffix {s}: W={w_val}, L={l_val}")

# Set new key for file name prefix.
mea_file_name = savepath.get_val() + "\mea_dict.csv"
if os.path.exists(mea_file_name):
    with open(savepath.get_val() + "\mea_dict.csv", 'r') as f:
        keydict = pd.read_csv(f).to_dict()
        f.close()

    new_key = 0
    while new_key == 0:
        #        new_keyval = secrets.token_hex(3)
        new_keyval = os.urandom(3).hex()
        if new_keyval not in keydict.keys():
            keyval.set_val(new_keyval)
            new_key = 1
else:
    # keyval.set_val(secrets.token_hex(3))
    keyval.set_val(os.urandom(3).hex())

# Clear data
iccap_func("../IVA", "Clear Data/Both")
iccap_func("../IVB", "Clear Data/Both")
iccap_func("../IVC", "Clear Data/Both")
iccap_func("../IVD", "Clear Data/Both")
iccap_func("../IVE", "Clear Data/Both")
iccap_func("../IVF", "Clear Data/Both")
iccap_func("../IVG", "Clear Data/Both")
iccap_func("../IVH", "Clear Data/Both")
iccap_func("../IVI", "Clear Data/Both")
iccap_func("../IVJ", "Clear Data/Both")
iccap_func("../stress", "Clear Data/Both")

# --- Measure data
va_list = []
ia_list = []
vb_list = []
ib_list = []
vc_list = []
ic_list = []
vd_list = []
id_list = []
ve_list = []
ie_list = []
vf_list = []
if_list = []
vg_list = []
ig_list = []
vh_list = []
ih_list = []
vi_list = []
ii_list = []
vj_list = []
ij_list = []

ra_dic = {}
rb_dic = {}
rc_dic = {}
rd_dic = {}
re_dic = {}
rf_dic = {}
rg_dic = {}
rh_dic = {}
ri_dic = {}
rj_dic = {}

va_dic = {}
ia_dic = {}
vb_dic = {}
ib_dic = {}
vc_dic = {}
ic_dic = {}
vd_dic = {}
id_dic = {}
ve_dic = {}
ie_dic = {}
vf_dic = {}
if_dic = {}
vg_dic = {}
ig_dic = {}
vh_dic = {}
ih_dic = {}
vi_dic = {}
ii_dic = {}
vj_dic = {}
ij_dic = {}

filename.set_val(str(keyval.get_val()) + "_0s_")
Tot_Stress_Time.set_val(0)
print("MEA FILENAME: ", filename.get_val())
# old_mdm_name = mdm_file_name.get_val()
# print("OLD MDM NAME: ",old_mdm_name)
# new_mdm_name = "0s_"+old_mdm_name
# mdm_file_name.set_val(new_mdm_name)
# print("NEW MDM NAME: ",new_mdm_name)


print("After Stressed 0 s: Measure IV for all resistors...")

# List of suffixes from a to j


# Dictionaries to store the objects and results

print("Starting measurement sequence...")

for s in suffixes:
    # 1. Access the Dvar for logic (e.g., check if this pin is active)
    start_time = time.perf_counter()
    current_bool = globals()[f"bool_{s}"]
    start_time = time.perf_counter()
    if current_bool.get_val() == "1":
        monitor_current = wl_dict[s]["I_monitor"]
        print(s + ':' + str(monitor_current))
        print(f"Processing suffix: {s}")
        # 0. Connect measurement pins
        iccap_func(f"../IV{s.upper()}/connect_measure_{s}", "Execute")
        iccap_func(f"../IV{s.upper()}/ih", "STFV", ["Start", -5 * monitor_current])

        iccap_func(f"../IV{s.upper()}/ih", "STFV", ["Stop", 5 * monitor_current])
        iccap_func(f"../IV{s.upper()}/ih", "STFV", ["Step Size", monitor_current / 10])
        iccap_func(f"../IV{s.upper()}/ih", "Redisplay")
        # 1. Execute Measurement
        print(f"Measuring IV{s.upper()}...")
        iccap_func(f"../IV{s.upper()}", "Measure")

        # 2. Link to IC-CAP Objects
        v_obj = Output(f"../IV{s.upper()}/v")
        i_obj = Input(f"../IV{s.upper()}/ih")

        globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())] = []
        globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())] = []
        globals()[f"r{s}_dic"][str(Tot_Stress_Time.get_val())] = []

        v_list_measured = v_obj.get_val()[('M', '11')]
        i_list_measured = i_obj.get_val()[('M', '11')]
        for v_meas, i_meas in zip(v_list_measured, i_list_measured):
            # We compare the real part of the measured current to our target

            # 4. Append the matched pair to your global storage lists
            globals()[f"v{s}_list"].append(v_meas.real)
            globals()[f"i{s}_list"].append(i_meas.real)

            globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())].append(v_meas.real)
            globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())].append(i_meas.real)

        #            if math.isclose(i_meas.real, monitor_current, rel_tol = 1e-9):
        #                globals()[f"r{s}_dic"][str(Tot_Stress_Time.get_val())] = v_meas.real / i_meas.real
        r_1 = globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())][-2] / \
            globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())][-2]
        r_2 = globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())][51] / \
            globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())][51]
        print(s + ':' + str(r_1), str(r_2))
        globals()[f"r{s}_dic"][str(Tot_Stress_Time.get_val())].append([r_1,r_2])
        # 6. Disconnect measurement pins
        iccap_func("disconnect", "Execute")
        # 5. Export Data
        iccap_func(f"../IV{s.upper()}/export_mea_{s}", "Execute")
<<<<<<< HEAD
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Runtime for Pin {s}: {duration:.2f} seconds")
=======
        print(globals()[f"r{s}_dic"])
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Runtime for MEA {s}: {duration:.2f} seconds")
>>>>>>> 9a83c03379b9c3912707aa849ff0a682cd52586e
# Stress - measure RA-RJ cycle


for i in range(0, len(Stress_Time_Values)):
    if i == 0:
        stresstime = Stress_Time_Values[i]
        timestep = stresstime / 10
        if timestep > 10:
            timestep = 10  # the Interval Range is [0.0001, 65.535]
    #            print"Time Step is changed to: {} [sec]".format(timestep)
    else:

        stresstime = Stress_Time_Values[i] - Stress_Time_Values[i - 1]

        timestep = stresstime / 10
        if timestep > 10:
            timestep = 10  # the Interval Range is [0.0001, 65.535]

    #            print"Time Step is changed to: {} [sec]".format(timestep)

    # --- Change the stress time input conditions
    print("Time Stop is changed to: {}, Time Step is changed to: {} [sec]".format(stresstime, timestep))
    iccap_func("../stress/time", "STFV", ["Stop", stresstime])
    iccap_func("../stress/time", "STFV", ["Step Size", timestep])
    iccap_func("../stress/time", "Redisplay")
    Tot_Stress_Time.set_val(Stress_Time_Values[i])

    # --- file name update
    #    print str(Stress_Time_Values[i])+"s_"
    filename.set_val(str(keyval.get_val()) + "_" + str(Stress_Time_Values[i]) + "s_")

    # --- Clear data
    iccap_func("../stress", "Clear Data/Both")
    # --- Run Stress measurement
    # new_mdm_name = str(stresstime)+"s_"+old_mdm_name
    # mdm_file_name.set_val(new_mdm_name)
    # print("NEW MDM NAME: ",new_mdm_name)
    print("Measure stress...")
    iccap_func("../stress/connect_stress", "Execute")
    iccap_func("../stress", "Measure")
    iccap_func("../stress/export_stress", "Execute")
    iccap_func("../stress/disconnect", "Execute")
    iccap_func("../stress", "Close All")

    # --- Clear data
    iccap_func("../IVA", "Clear Data/Both")
    iccap_func("../IVB", "Clear Data/Both")
    iccap_func("../IVC", "Clear Data/Both")
    iccap_func("../IVD", "Clear Data/Both")
    iccap_func("../IVE", "Clear Data/Both")
    iccap_func("../IVF", "Clear Data/Both")
    iccap_func("../IVG", "Clear Data/Both")
    iccap_func("../IVH", "Clear Data/Both")
    iccap_func("../IVI", "Clear Data/Both")
    iccap_func("../IVJ", "Clear Data/Both")
    # --- Measure all R

    for s in suffixes:
        # Print stress condition
        start_time = time.perf_counter()
        print("Stressed with Total_stress_time:{}".format(Tot_Stress_Time.get_val()))
        current_bool = globals()[f"bool_{s}"]
        start_time = time.perf_counter()
        if current_bool.get_val() == "1":
            monitor_current = wl_dict[s]["I_monitor"]
            print(f"Processing suffix: {s}")
            # 0. Connect measurement pins
            iccap_func(f"../IV{s.upper()}/connect_measure_{s}", "Execute")
            iccap_func(f"../IV{s.upper()}/ih", "STFV", ["Start", -5 * monitor_current])

            iccap_func(f"../IV{s.upper()}/ih", "STFV", ["Stop", 5 * monitor_current])
            iccap_func(f"../IV{s.upper()}/ih", "STFV", ["Step Size", monitor_current / 10])
            iccap_func(f"../IV{s.upper()}/ih", "Redisplay")
            # 1. Execute Measurement
            print(f"Measuring IV{s.upper()}...")
            iccap_func(f"../IV{s.upper()}", "Measure")

            # 2. Link to IC-CAP Objects
            v_obj = Output(f"../IV{s.upper()}/v")
            i_obj = Input(f"../IV{s.upper()}/ih")
            globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())] = []
            globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())] = []
            globals()[f"r{s}_dic"][str(Tot_Stress_Time.get_val())] = []

            v_list_measured = v_obj.get_val()[('M', '11')]
            i_list_measured = i_obj.get_val()[('M', '11')]
            for v_meas, i_meas in zip(v_list_measured, i_list_measured):
                # We compare the real part of the measured current to our target

                # 4. Append the matched pair to your global storage lists
                globals()[f"v{s}_list"].append(v_meas.real)
                globals()[f"i{s}_list"].append(i_meas.real)

                globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())].append(v_meas.real)
                globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())].append(i_meas.real)
            #                if math.isclose(i_meas.real, monitor_current, rel_tol = 1e-9):
            #                    globals()[f"r{s}_dic"][str(Tot_Stress_Time.get_val())] = v_meas.real / i_meas.real
            r_1 = globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())][-2] / \
                globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())][-2]
            r_2 = globals()[f"v{s}_dic"][str(Tot_Stress_Time.get_val())][51] / \
                globals()[f"i{s}_dic"][str(Tot_Stress_Time.get_val())][51]
            print(s + ':' + str(r_1), str(r_2))
            globals()[f"r{s}_dic"][str(Tot_Stress_Time.get_val())].append([r_1,r_2])
            # 5. Export Data
            iccap_func(f"../IV{s.upper()}/export_mea_{s}", "Execute")
            # 6. Disconnect measurement pins
            iccap_func("disconnect", "Execute")
<<<<<<< HEAD
            end_time = time.perf_counter()
            duration = end_time - start_time
            print(f"Runtime for Pin {s}: {duration:.2f} seconds")
    print(globals()[f"r{s}_dic"])
=======
            print(globals()[f"r{s}_dic"])
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Runtime for MEA {s}: {duration:.2f} seconds")
>>>>>>> 9a83c03379b9c3912707aa849ff0a682cd52586e
# Plots
model_name = icfuncs.who_is('../../.')
dut_name = icfuncs.who_is('../.')
date = get_var(model_name + '/Date')
temp = float(get_var(model_name + '/Temperature'))
die_index = get_var(model_name + '/Die')
# m_value = int(get_var(model_name+'/M'))
m_value = 1
DeviceName_str = get_var(model_name + '/DeviceName')
Subsite_str = get_var(model_name + '/Subsite')
Lot_str = get_var(model_name + '/Lot')
Wafer_str = get_var(model_name + '/Wafer')

# print (wproapi.get_measurement_group_name())
# Device_Dir = "P5_" + "W" + str(w_value) + "L" + str(L_value)+ ""# define Device data saved dir
Device_Dir = Subsite_str + "_" + DeviceName_str

Title_Str = DeviceName_str + ",M=" + str(m_value) + "\n" + str(Lot_str) + " wf" + str(Wafer_str)
# filePath = get_var(dut_name+'/Mea_Data_Save_Dir')+'\\'+die_index+'\\'+dev_type+'\\'+Device_Dir+'\\'
filePath = get_var(dut_name + '/Mea_Data_Save_Dir') + '\\' + Lot_str + '\\' + Wafer_str + '\\' + str(
    temp) + 'c\\' + die_index + '\\' + Device_Dir + '\\'
plt_file_name = '/' + keyval.get_val()
# Setting Plots size
# Your sample dictionary

for s in suffixes:
    # 1. Access the Dvar for logic (e.g., check if this pin is active)
    current_bool = globals()[f"bool_{s}"]
    if current_bool.get_val() == "1":
        # 1. Sort the keys numerically to ensure the line flows correctly
        # We convert the key to float/int only for the sorting logic
        sorted_keys = sorted(globals()[f"r{s}_dic"].keys(), key=lambda x: float(x))
        sorted_values_l = [globals()[f"r{s}_dic"][k][0][0] for k in sorted_keys]
        print(sorted_values_l)
        sorted_values_h = [globals()[f"r{s}_dic"][k][0][1] for k in sorted_keys]
        print(sorted_values_h)
        # 2. Create the plot
        plt.figure(figsize=(10, 5))
        plt.plot(sorted_keys, sorted_values_l, linestyle='-', color='b')
        plt.plot(sorted_keys, sorted_values_h, linestyle='-', color='r')
        # 3. Add labels and title
        plt.xlabel("Time")
        plt.ylabel("R")
        plt.title(f"r{s}_dic Data Plot")
        w = wl_dict[s]["W"]
        l = wl_dict[s]["L"]
        # 4. Save or show the plot
        plt.savefig(filePath + plt_file_name + f"_r{s}_W_{w}_L{l}_plot.png")
plt.close('all')

# Setting Plots size
# fig=plt.figure(num='Delta Stress Test',figsize=(21,16))
# #fig.canvas.manager.set_window_title('Stress Test')
#
# plt.savefig(filePath+deltafileName)
# #plt.show()
# plt.close(fig)


for s in suffixes:
    # 1. Access the Dvar for logic (e.g., check if this pin is active)
    current_bool = globals()[f"bool_{s}"]
    if current_bool.get_val() == "1":
        print(f"Saving data for suffix: {s}")
        current_filename = '/' + keyval.get_val() + 'full_I{}'.format(s.upper()) + '.csv'
        voltage_filename = '/' + keyval.get_val() + 'full_V{}'.format(s.upper()) + '.csv'
        resistance_filename = '/' + keyval.get_val() + 'full_R{}'.format(s.upper()) + '.csv'
        df_i = pd.DataFrame(globals()[f"i{s}_dic"])
        df_i.to_csv(filePath + current_filename, index=[0])
        df_v = pd.DataFrame(globals()[f"v{s}_dic"])
        df_v.to_csv(filePath + voltage_filename, index=[0])
        df_r = pd.DataFrame(globals()[f"r{s}_dic"])
        df_r.to_csv(filePath + resistance_filename, index=[0])

print('finish')
# print("Delta Plots (Hrs) have been saved: %s" %(filePath+current_filename))
# Save Stress Idsat vs Time data
# iccap_func("save_stress_data","Execute")


