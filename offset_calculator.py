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

#Convert coordinates to meter-based coordinates for easier plotting purposes

def coord_to_met(coord_list):
    met_list = []
    for jip in coord_list:
        y_met = jip[0]*multipliers[0]
        x_met = jip[1]*multipliers[1]
        yx_met = [y_met, x_met]
        met_list.append(yx_met)
    return(met_list)

if __name__ == "__main__":
    from_coord = [3610.489215, 1486.459584]
    to_coord = [3610.495225, 1486.712915]
    print(offset_meter_calculator(from_coord, to_coord))
