import time
import math
import steering_servo
#import speed_control
import compass_reader
import breadcrumb_calculator
import offset_calculator
import read_gps
import Specs

crumbs_left = 10 #Arbitrary number for initializing

dist_bc = 0

#Calculates the bearing and relative bearing from the first coordinate to the second coordinate, considering current heading
def angles(from_coord, to_coord, heading):
    offset_dict = offset_calculator.offset_meter_calculator(from_coord, to_coord)
    offset_y = offset_dict["offsets_met"][0]
    offset_x = offset_dict["offsets_met"][1]


    #Rules to bypass calculations for special cases that would cause division error
    if offset_y == 0 and offset_x < 0:
        bearing = -90
    elif offset_y == 0 and offset_x > 0:
        bearing = 90
    #Calculation of bearings in most situations
    else:
        #Calculation of bearing angle
        bearing = math.degrees(math.atan(offset_x / offset_y))
        
        #Adjustments needed for lower two 90-degree quadrants
        if offset_y < 0 and offset_x < 0:
            bearing = -180 + abs(bearing)
        elif offset_y < 0 and offset_x > 0:
            bearing = 180 - abs(bearing)
        
    #Determining the relative bearing
    rel_bearing = bearing - heading
    
    
    #Adjusting if rel_bearing > 180 in either direction to find the direction with samallest angle
    if rel_bearing < -180:
        rel_bearing = 360 + rel_bearing
    if rel_bearing > 180:
        rel_bearing = rel_bearing - 360

    bearings_dict = {"Target bearing":bearing, "Target relative bearing":rel_bearing}
    return(bearings_dict)

def captain():
    waypoints_list = Specs.waypoints_list
    breadcrumb_coordinates = Specs.breadcrumb_coordinates
    print("Captain started, breadcrumbs:", breadcrumb_coordinates)
    global dist_bc
    location_now = read_gps.current_min #Find out current location for plotting
    while True:
        closest_plus = Specs.closest_plus
        location_now = read_gps.current_min
        closest_c, target_c, crumbs_left = breadcrumb_calculator.closest_crumb(location_now, breadcrumb_coordinates, closest_plus)
        print("Closest crumb:", closest_c, "Target crumb:", target_c, "Crumbs left:", crumbs_left)
        if crumbs_left > 1:
            dist_bc = offset_calculator.offset_meter_calculator(location_now, closest_c)
            bearings = angles(location_now, target_c, compass_reader.heading)
            rel_bearing = bearings["Target relative bearing"]
            steering_servo.angle = rel_bearing
        else:
            print("Out of crumbs! Captain done.")
            return("GPS Done")
        
        time.sleep(2)
    return("GPS Terminated")
