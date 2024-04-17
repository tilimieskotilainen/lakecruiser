#This is the backbone of the code, initiating the various stages of the journey based on trigger events
#import asyncio
#import websockets
#import shoot_and_calculate
#import trip_dist_calculator
#import breadcrumb_calculator
#import Approach
#import webbrowser

#For threads to start:
import read_gps
import steering_servo
import compass_reader
import Specs


#For actions in backbone:
import json
import threading
import time
import gps_cruise
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import offset_calculator

gps_cruise_thread = threading.Thread(target=gps_cruise.captain, args=(), daemon=True) #Define GUI thread

read_gps_thread = threading.Thread(target=read_gps.read_gps, args=(), daemon=True) #Define GPS thread
read_gps_thread.start() # Start GPS thread
#time.sleep(1)
read_compass_thread = threading.Thread(target=compass_reader.read_compass, args=(), daemon=True) #Define compass thread
read_compass_thread.start() # Start compass thread
#time.sleep(1)
steering_thread = threading.Thread(target=steering_servo.steer, args=(), daemon=True) #Define compass thread
steering_thread.start() # Start steering servo thread
#time.sleep(1)

#Funktio joka lähtee pyörimään, kun UI:ssa valitaan statukseksi "run"
def run():
    gps_cruise_thread.start() # Start GPS cruise thread


######## GUI-RELATED CODE BELOW #########

#Open available routes
ro = open("routes.txt", "r") #Open file
rou = ro.read()
routes = json.loads(rou) #Read the contents of the opened file and assign it to the variable config
ro.close()
routes_list = list(routes.keys())

#Open previously saved default values
sc = open("config.txt", "r") #Open file
jou = sc.read()
config_dict = json.loads(jou) #Read the contents of the opened file and assign it to the variable config
sc.close()

#Default values tos how in GUI:
def_aim_ahead = config_dict["aim_ahead"]
def_steer_toler = config_dict["steer_toler"]
def_tof_range = config_dict["tof_range"]



layout = [
    [sg.OptionMenu(values=(routes_list), default_value = "Select route", expand_x=True, key="route_selection")],
    [sg.Text("Direction"), sg.Radio("Forward", group_id="direction", default=True),sg.Radio("Backward", group_id="direction", default=False)],
    [sg.Button("Calculate route", expand_x=True, key="Calculate")],
    [[sg.Text("Route distance:"), sg.Text("0", key="dist")],[sg.Text("Waypoints:"), sg.Text("0", key="wp_num")]],
    [[sg.Text("Aim")],
     [sg.Slider(range=(1, 10), expand_x=True, default_value=def_aim_ahead, resolution=1, tick_interval=1, orientation="horizontal", key="closest_plus")]],
    [[sg.Text("Steer range (mm)")],
     [sg.Slider(range=(10, 30), expand_x=True, default_value=def_tof_range, resolution=1, tick_interval=5, orientation="horizontal", key="tof_range")]],    
    [[sg.Text("Steer tolerance (deg)")],
     [sg.Slider(range=(0, 20), expand_x=True, default_value=def_steer_toler, resolution=1, tick_interval=5, orientation="horizontal", key="steer_toler")]],
    [sg.Button("Update", expand_x=True, key="Update")],
    [sg.Button("Start", button_color="Green", expand_x=True, key="Start")],
    [sg.Button("Stop", button_color="Red", expand_x=True, key="Stop")],
    [sg.Text("Selected route"), sg.Text()],
    [sg.Text("Closest crumb"), sg.Text()],
    [sg.Text("Turn status"), sg.Text()],
    [sg.Text("Heading"), sg.Text()],
    [sg.Text("Battery voltage"), sg.Text()]
    ]

#Generate plot of the route
def plot_route():
    coord_met = offset_calculator.coord_to_met(Specs.waypoints_list)
    y_list = []
    x_list = []
    for jau in coord_met:
        y_list.append(jau[0])
        x_list.append(jau[1])
    y_min = min(y_list)
    x_min = min(x_list)
    y_cut_list = []
    x_cut_list = []
    yx_cut_list = []
    for jia in y_list:
        y_cut = jia - y_min
        y_cut_list.append(y_cut)
        yx_cut_list.append(y_cut)
    for jea in x_list:
        x_cut = jea - x_min
        x_cut_list.append(x_cut)
        yx_cut_list.append(x_cut)
    range_min = min(yx_cut_list)
    range_max = max(yx_cut_list)

    plt.xlim([range_min - 100, range_max + 100])
    plt.ylim([range_min - 100, range_max + 100])
    plt.plot(x_cut_list, y_cut_list)
    plt.show()

# Create the GUI window
window = sg.Window("Lautta GUI", layout)

#Define responses to GUI actions
def gui_loop():
    while True:
        event, values = window.read()
        if event == "Calculate":
            print("Calculated")
            Specs.route = values["route_selection"]
            Specs.update_calc()
            window["dist"].update(Specs.trip_dist)
            window["wp_num"].update(Specs.wp_num)
            plot_route()

            #Make start available
            #Make update available

        if event == "Update":

            #Tähän koodi jolla tehdään gui_input, joka sisältää kaikki GUI:ssa muutetut variablet
            closest_plus = int(values["closest_plus"])
            turn_range = int(values["tof_range"])
            turn_toler = int(values["steer_toler"])
            gui_input = {"closest_plus":int(values["closest_plus"]), "tof_range":int(values["tof_range"]), "steer_toler":int(values["steer_toler"])} 
            Specs.update_vars(gui_input)

            print(closest_plus, turn_range, turn_toler)


        if event == "Start":

            print("Started")
            gps_cruise_thread.start()
            #Make stop available

        if event == "Stop":
            print("Stopped")
            #Return to initial state
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
    window.close()

gui_loop()

#run()
