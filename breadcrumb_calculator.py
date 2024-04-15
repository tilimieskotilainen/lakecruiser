import offset_calculator

approx_int_m = 1

breadcrumb_coordinates = []

closest_index = 0

def breadcrumb(waypoints_list):

    for wp in waypoints_list: #Take each coordinate pair within the waypoints list
        for coord in wp: #Take each half of each coordinate (lat and lon)
            coord = float(coord) #Change the waypoint coordinates to floats

#    breadcrumb_coordinates.append(tuple(waypoints_list[0][0:2])) #Enter the first location as the first item in the list
    for point in range(1, len(waypoints_list)): #Iterate through the indexes in the list, skipping 0
        #0 is skipped because it is the start position, not to be used by the gps-leg of the journey
        leg_offset = offset_calculator.offset_meter_calculator(waypoints_list[point - 1], waypoints_list[point]) #Calcultes the offset for the leg, ie between the waypoint being looped over and the previous one
#        print("Leg offset:", leg_offset)
        total_offsets_met = leg_offset["offset_dist"] #Extracts the distance in meters from the dictionary returned by the calculator function
#        print("Total offset met:", total_offsets_met)
        total_offsets_min = leg_offset["offset_min"] #Extracts the distance in minutes from the dictionary returned by the calculator function
        breadcrumb_intervals = int(total_offsets_met / approx_int_m) #Calculates the number of breadcrumb intervals needed for the leg in question, based on specified length of breadcrumb interval.
        interval_offsets = (total_offsets_min[0] / breadcrumb_intervals, total_offsets_min[1] / breadcrumb_intervals) #Calculates the lon and lat offsets of intervals, in minutes
#        print("Interval offsets:", interval_offsets)

        for iik in range(breadcrumb_intervals): #Start creating breadcrumb coordinates for the number of breadcrumbs calculated above
            next_point = (float(waypoints_list[point-1][0]) + float(interval_offsets[0]) * int(iik), float(waypoints_list[point-1][1]) + float(interval_offsets[1]) * int(iik)) #Calculate the coordinates of the next point based on the offsets
            breadcrumb_coordinates.append(next_point) #Add previously calculated coordinates to the breadcrumb list

#    print("Breadcrumbs calculated:", breadcrumb_coordinates)
#    print("Breadcrumb coordinates:", breadcrumb_coordinates)
    return(breadcrumb_coordinates)

#Calculates the closest breadcrumb and the target breadcrumb from the current location considering the "closest_plus" parameter
def closest_crumb(location_now, crumbs, closest_plus):
    global crumbs_left
    global closest_index
    bc_dists = []
    for j in crumbs:
        point_dist = offset_calculator.offset_meter_calculator(location_now, j)["offset_dist"]
        bc_dists.append(point_dist)
#    print("BC dists", bc_dists)
    closest_index = bc_dists.index(min(bc_dists))
#    print("Closest index:", closest_index)
    crumbs_left = len(crumbs) - closest_index
    if crumbs_left > closest_plus: #If the closest breadcrumb is more than "closest plus" number of crumbs from the end...
        head_towards = crumbs[closest_index + closest_plus]
        return(crumbs[closest_index], head_towards, crumbs_left)
    else: #If closest crumb is less than "closest plus" number of crumbs from the end, head for the end
#        print("Under")
        return(crumbs[closest_index], crumbs[-1], crumbs_left) #