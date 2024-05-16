import json
import time
import steering_servo
import trip_dist_calculator
import breadcrumb_calculator

#Variables for steering control
tof_straight = 60
tof_toler = 5
tof_range = 40
steer_toler = 10

#Variables for route phase selections
#GPS_navi_selected = None
config = None
route = None
waypoints_list = None
route_points = None
wp_num = None
bc_num = None
trip_dist = 0
closest_plus = 0
breadcrumb_coordinates = None

#cur_stage = "Waiting for stages..."

#Keskeisten variablien muuttaminen, jonka kutsuu GUI
def update_vars(gui_input):
    global tof_toler
    global tof_range
    global steer_toler
    global closest_plus #Tämä on käynnistystä varten update_calc -funktiossa ja myöhempiä muutoksia varten update_vars funktiossa

    #Variablien määrittäminen GUI:n lähettämien tietojen pohjalta
    tof_range = gui_input["tof_range"]
    steer_toler = gui_input["steer_toler"]
    closest_plus = gui_input["closest_plus"]

    #Tähän funktio joka päivittää config-tiedostossa olevat tiedot GUI:ssä määritetyillä arvoilla
    of = open("config.txt", "r")
    jou = of.read()
    config_dict = json.loads(jou)
    print(config_dict)
    of.close()

    config_dict["aim_ahead"] = gui_input["closest_plus"]
    config_dict["steer_toler"] = gui_input["steer_toler"]
    config_dict["tof_range"] = gui_input["tof_range"]

    config_json = json.dumps(config_dict)
    wf = open("config.txt", "w")
    wf.write(config_json)
    wf.close()
    print("Config updated")


#Function to update the initial calculations when prompted from UI
def update_calc():

    global config
    global waypoints_list
    global wp_num
    global bc_num
    global trip_dist
    global route_points
    global closest_plus #Tämä on käynnistystä varten update_calc -funktiossa ja myöhempiä muutoksia varten update_vars funktiossa
    global breadcrumb_coordinates

    try:
        sc = open("config.txt", "r") #Open file
        config = json.loads(sc.read()) #Read the contents of the opened file and assign it to the variable config
        sc.close()
        print("config read")
        #Number of waypoints in route

        of = open("routes.txt", "r") #Open file determined in the config file
        routes_dict = json.loads(of.read()) #Read the contents of the opened file and assign it to the variable "waypoints_list"
        of.close()
        waypoints_list = routes_dict[route]
        print("Route:", waypoints_list)

        trip_dist = round(trip_dist_calculator.trip_dist_calculator(waypoints_list),1)
        wp_num = str(len(waypoints_list))

        breadcrumb_coordinates = breadcrumb_calculator.breadcrumb(waypoints_list)
        bc_num = len(breadcrumb_coordinates)

        print("Trip configured | Trip dist:", trip_dist, "m | Waypoints:", wp_num)


    except:
        print("No saved config found")
        pass


#Käynnistyessä laskee ensimmäisen kerran matkan speksit
#update_calc()