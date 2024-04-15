
import math

#Calculates the x and y offsets and straight-line offsets in meters between any two coordinates (minutes and decimals)
def offset_meter_calculator(from_min, to_min):
    from_min = tuple(from_min)
    to_min = tuple(to_min)
    multipliers = (1853, 921.8)
    offset_min = (float(to_min[0]) - float(from_min[0]), float(to_min[1]) - float(from_min[1]))
    offsets_met = [round(offset_min[0] * multipliers[0], 3), round(offset_min[1] * multipliers[1], 3)]
    offset_dist = round(math.sqrt(offsets_met[0] ** 2 + offsets_met[1] ** 2), 5)
    return_dict = {"offsets_met":offsets_met, "offset_dist":offset_dist, "offset_min":offset_min}
    return(return_dict)