# import the necessary packages
import time
import json
import steering_servo
import speed_control
import sys
from compass_reader import heading
from backbone import status

#target_y = 430

#status = "run"

def Approach(waypoints):
    
    target_heading = waypoints["end"][-1]
    print("Target heading:", target_heading)
    
    print("Heading:", heading)
    
    #Reitistä vikan pisteen orientaation lukeminen
    #Nykyisen headingin lukeminen
    #Erotuksen laskeminen

    while status == "run":
        print("Diff:", diff)
        synth_angle = int(diff / 320 * 90) #Muuttaminen kameran kulman mukaisiksi asteiksi (per puoli)
        print("synth_angle:", synth_angle)
        
        steering_servo.steer_direction(synth_angle/2)

        ###########
        #The distance determination has to be done with camera or other sensor. For now hard-coded as 200
        dist = 200
        print("Distance:", dist)
        if dist < 80:
            speed_control.propulsion("Stop")
            print("DONE!")
            return("Approach done")
        else:
            speed_control.propulsion(60)
        #########

        time.sleep(0.2)

    print("status is now:", status)

    speed_control.propulsion(0)
    return("Approach terminated")


if __name__ == "__main__":
    Approach() #Ei toimi koska ei ole luettu waypointseja