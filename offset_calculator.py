import math

multipliers = (1853, 921.8)

#Calculates the x and y offsets and straight-line offsets in meters between any two coordinates (minutes and decimals)
def offset_meter_calculator(from_min, to_min):
    from_min = tuple(from_min)
    to_min = tuple(to_min)
    offset_min = (float(to_min[0]) - float(from_min[0]), float(to_min[1]) - float(from_min[1]))
    offsets_met = [round(offset_min[0] * multipliers[0], 3), round(offset_min[1] * multipliers[1], 3)]
    offset_dist = round(math.sqrt(offsets_met[0] ** 2 + offsets_met[1] ** 2), 5)
    return_dict = {"offsets_met":offsets_met, "offset_dist":offset_dist, "offset_min":offset_min}
    return(return_dict)


x_minimum = 0
y_minimum = 0

#Convert coordinates to meter-based coordinates for easier plotting purposes
def coord_to_met(coord_list):
    met_list = [[],[]]
    for jip in coord_list:
        print("coord_list:", coord_list)
        y_met = jip[0]*multipliers[0]
        met_list[0].append(y_met)
        x_met = jip[1]*multipliers[1]
        met_list[1].append(x_met)

    global y_minimum
    global x_minimum

#Find smllest and largest values IF more than one coordinate in question
#This is to distinguish between waypoint list (list of locations) and current gps-location (one location)
    if len(met_list[0])>1:
        y_minimum = min(met_list[0])
        x_minimum = min(met_list[1])

    y_cut_list = []
    x_cut_list = []
    yx_cut_list = []

    #Subtract y_min and x_min from 
    for jia in met_list[0]:
        y_cut = jia - y_minimum
        y_cut_list.append(y_cut)
    for jea in met_list[1]:
        x_cut = jea - x_minimum
        x_cut_list.append(x_cut)

    return(y_cut_list, x_cut_list)
if __name__ == "__main__":
    from_coord = [3610.489215, 1486.459584]
    to_coord = [3610.495225, 1486.712915]
    print(offset_meter_calculator(from_coord, to_coord))
