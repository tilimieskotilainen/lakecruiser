import math

#Calculates the x and y offsets and straight-line offsets in meters between any two coordinates (minutes and decimals)
def offset_meter_calculator(from_min, to_min):
    from_min = tuple(from_min)
    to_min = tuple(to_min)
    multipliers = (1853, 921.8)
    offset_min = (float(to_min[0]) - float(from_min[0]), float(to_min[1]) - float(from_min[1]))
    offsets_met = [round(offset_min[0] * multipliers[0], 3), round(offset_min[1] * multipliers[1], 3)]
    offset_dist = round(math.sqrt(offsets_met[0] ** 2 + offsets_met[1] ** 2), 5)
    return(offset_dist)


def trip_dist_calculator(route):

    total_distance = 0

#    total_distance += offset_meter_calculator(route["start"], route["waypoints"][0])
#    total_distance += offset_meter_calculator(route["waypoints"][-1], route["end"])

    for point in range(len(route)): #Iterate through the indexes in the list, skipping 0
        leg_offset = offset_meter_calculator(route[point - 1], route[point]) #Calcultes the offset for the leg, ie between the waypoint being looped over and the previous one
    #        print("Leg offset:", leg_offset)
        total_distance += leg_offset

    return(total_distance)