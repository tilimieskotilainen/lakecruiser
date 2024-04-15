import serial
from pynmea import nmea
import time
import math
import json
import compass_reader


#Waypoints information is stored in the following file in JSON format:

waypoints_file = input("What would you like to call your route?")


#Reads gps coordinates and returns current location in minutes and decimals
def read_gps():
    
    #Specs for GPS module
    ser = serial.Serial('/dev/serial0') #EPäSELVÄÄ MIKÄ DEVICE TÄHÄN
    ser.baudrate=9600

    
    while True:
        try:
            message = ser.readline().decode()
            message = message.strip()     
            if '$GNGGA' in message:    
                gngga = nmea.GPGGA()
                gngga.parse(message)
                lat = gngga.latitude
                print("Lat raw", lat)
                lon = gngga.longitude
                print("Lon raw", lon)
                lat_min = round(float(lat[0:2]) * 60 + float(lat[2:]), 6)
                print("Lat min:", lat_min)
                lon_min = round(float(lon[0:3]) * 60 + float(lon[3:]), 6)
                print("Lon min", lon_min)
                current_min = (lat_min, lon_min)
#                ser.close()
                return(current_min)
        except:
            print("No GPS-signal")
            pass
    
#Retuns compass heading from c program
def read_heading():
    heading = compass_reader.heading
    print("Heading:", heading)
    return(heading)


#Calculates the x and y offsets and straight-line offsets in meters between any two coordinates (minutes and decimals)
def offset_meter_calculator(from_min, to_min):
    from_min = tuple(from_min)
    to_min = tuple(to_min)
    multipliers = (1853, 921.8)
    offset_min = (float(to_min[0]) - float(from_min[0]), float(to_min[1]) - float(from_min[1]))
    offsets_met = [round(offset_min[0] * multipliers[0], 1), round(offset_min[1] * multipliers[1], 1)]
    offset_dist = round(math.sqrt(offsets_met[0] ** 2 + offsets_met[1] ** 2), 1)
    return_dict = {"offsets_met":offsets_met, "offset_dist":offset_dist, "offset_min":offset_min}
    return(return_dict)

#Calculates the bearing and relative bearing from the first coordinate to the second coordinate, considering current heading
def angles(from_coord, to_coord, heading):
    offset_dict = offset_meter_calculator(from_coord, to_coord)
    offset_y = offset_dict["offsets_met"][1]
    offset_x = offset_dict["offsets_met"][0]
    bearing = math.degrees(math.atan(offset_x / offset_y))
    rel_bearing = bearing - heading
    bearings_dict = {"Target bearing":bearing, "Target relative bearing":rel_bearing}
    return(bearings_dict)

#Creates a breadcrumb (series of tracking points) between the start and destination coordinates
#Retuns a list of breadcrumb coordinates

def record_waypoints():
    waypoint_dict = {}
    wpl = []
    while True:
        inp = input("Hit W to record current location as a new waypoint and S to save waypoints to file.")
        if inp.upper() == "W":
            wp = read_gps()
            comp = round(read_heading(), 1)
            wpl.append((wp[0], wp[1], comp))
            del wp
            del comp
        if inp.upper() == "S":
            break
    #Construct JSON
    waypoint_dict["waypoints"] = wpl[1:-1]
    waypoint_dict["start"] = wpl[0]
    waypoint_dict["end"] = wpl[-1]

    print("Waypoint dict:", waypoint_dict)
    
    of = open(waypoints_file, "w+") #Open file determined at the top of the program
    waypoints_json = json.dumps(waypoint_dict)
    of.write(waypoints_json)
    of.close()
    
    print("Waypoints have been recorded")
    
record_waypoints()