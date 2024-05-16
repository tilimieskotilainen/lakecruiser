import PySimpleGUI as sg
import Specs
import json
import matplotlib.pyplot as plt
import read_voltage
#import backbone

#Open and present available routes
ro = open("routes.txt", "r") #Open file
rou = ro.read()
routes = json.loads(rou) #Read the contents of the opened file and assign it to the variable config
ro.close()
routes_list = list(routes.keys())

#Open and present previously saved default values
sc = open("config.txt", "r") #Open file
jou = sc.read()
config_dict = json.loads(jou) #Read the contents of the opened file and assign it to the variable config
sc.close()

#Default values:
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
    [sg.Text("Battery voltage"), sg.Text("0", key="volts")]

    ]


#Generate plot of the route
y_list = []
x_list = []

def plot_route():
    print(Specs.waypoints_list)
    for jau in Specs.waypoints_list:
        y_list.append(jau[0])
        x_list.append(jau[1])

    plt.plot(y_list, x_list)
    plt.show()



# Create the window
window = sg.Window("Lautta GUI", layout)

def gui_loop():
    # Create an event loop
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
            backbone.run()
            #Make stop available

        if event == "Stop":
            print("Stopped")
            #Return to initial state
        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break
    window.close()