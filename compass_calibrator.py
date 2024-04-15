from i2clibraries import i2c_hmc5883l
import time
import math
import json
import steering_servo #Own script for controlling steering
import speed_control #Own script for controlling propulsion
 
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)

#Create empty lists for storing x and y values
x_list = []
y_list = []

#Devine value n as zero to be used later for counting while-loop iterations
n = 0

steer_amount = [30]

#Steer 30-degrees to the right
#steering_servo.steer_direction(steer_amount)
#Start propulsion at 50%
speed_control.propulsion(50)

#Run loop to record 100 x and y values
while n < 100:
    hmc5883l.setContinuousMode()
    hmc5883l.setDeclination(9, 0)
    (x, y, z) = hmc5883l.getAxes() #Read readings from compass as variables x, y and z
    x_list.append(x) #Append latest x-reading in list of x-values
    y_list.append(y) #Append latest y-reading in list of y-values
    time.sleep(0.1) #Wait 0.5 seconds
    n = n + 1 #Add 1 to the value of n
    print(n, x, y)

speed_control.propulsion(0) #Stop propulsion
#steering_servo.steer_direction(0) #Return steering to straight

x_min = min(x_list) #Find smallest value from list of x-values
x_max = max(x_list) #Find largest value from list of x-values
y_min = min(y_list) #Find smallest value from list of y-values
y_max = max(y_list) #Find largest value from list of y-values

x_range = x_max - x_min #Calculate the range of x-values between smallest and largest
y_range = y_max - y_min #Calculate the range of y-values between smallest and largest

x_offset = x_max - x_range/2 #Calculate offset value for x
y_offset = y_max - y_range/2 #Calculate offset value for y

#Store offsets in a dictionary
offsets_dict = {"x_offset":x_offset, "y_offset":y_offset}

of = open("compass_offsets.txt", "w+") #Open file for saving offset values
offsets_json = json.dumps(offsets_dict) #Convert dictionary of offset-values to JSON
of.write(offsets_json) #Write JSON data to file
of.close() #Close file

print("Saved offsets to file:", offsets_dict)
