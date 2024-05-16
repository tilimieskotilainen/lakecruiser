import RPi.GPIO as GPIO
from time import sleep
import board
import busio
import adafruit_vl53l0x
import time
import Specs

rel_bearing = 30
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

in1 = 17 #OK23
in2 = 27 #OK23
#en = 17 #OK23
temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
#GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

#SEURAAVAT kumitettu 14.5. koska herjasi ja epäselvää mitä tekee
#p = GPIO.PWM(en,1000)
#p.start(25)


#print("\n")
#print("The default speed & direction of motor is LOW & Forward.....")
#print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
#print("\n")    

x = "s"

def steer():

  print("Steer thread running")
  while True:

    tof_straight = Specs.tof_straight
    tof_toler = Specs.tof_toler
    tof_range = Specs.tof_range
    tof_left = tof_straight - tof_range
    tof_right = tof_straight + tof_range
    steer_toler = Specs.steer_toler

    tof = vl53.range
    print("TOF:,", tof)

  #Establishing the direction to run the motor based on TOF values vs. relative bearing

  #When desired direction (relative bearing) is straight (+/- steering tolerance),
  #determine adjustments needed based on current steer orientation
    if rel_bearing > 0 - steer_toler and rel_bearing < 0 + steer_toler:
      #If current steer orientation is straight +/- tolerance, stop motor
      if tof > tof_straight - tof_toler and tof < tof_straight + tof_toler:
        x = "s"
      #If current steer orientation (TOF) is > straight, run motor backward. This elif is ignored when first if-statement is true.
      elif tof > tof_straight:
        x = "b"
      #If current steer orientation (TOF) is < straight, run motor forward. This elif is ignored when first if-statement is true.
      elif tof < tof_straight:
        x = "f"

    #When desired direction (relative bearing) is left, determine adjustments based on current steer orientation.
    elif rel_bearing < 0:
      if tof > tof_left:
        x = "b"
      elif tof <= tof_left - tof_toler:
        x = "f"
      else:
        x = "s"
  
    #When desired direction (relative bearing) is right, determine adjustments based on current steer orientation.
    elif rel_bearing > 0:
      if tof < tof_right:
        x = "f"
      elif tof >= tof_right + tof_toler:
        x = "b"
      else:
        x = "s"


#Running the motor based on the direction determined above

    """"
      if x=='r':
#          print("run")
          if(temp1==1):
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            x='z'
          else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            print("Steering TOF:", tof, ", running backward")
            x='z'
"""

    if x=='s':
      print("Steering motor stopped")
      GPIO.output(in1,GPIO.LOW)
      GPIO.output(in2,GPIO.LOW)
  #    x='z'

    elif x=='f':
      print("Steering motor forward")
      GPIO.output(in1,GPIO.LOW)
      GPIO.output(in2,GPIO.HIGH)
      temp1=1
  #    x='z'

    elif x=='b':
      print("Steering motor backward")
      GPIO.output(in1,GPIO.HIGH)
      GPIO.output(in2,GPIO.LOW)
      temp1=0
  #    x='z'
      
      
    elif x=='e':
      GPIO.cleanup()
      break
      
    else:
      print("Problem with running steering motor")

    time.sleep(0.5)


def test_steer_motor(direction):
  if direction == "forward":
    print("Steering motor forward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)

  if direction == "backward":
    print("Steering motor backward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

  if direction == "stop":
    print("Steering motor stopped")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)



if __name__ == "__main__":
  steer()


#    test_steer_motor("backward")
#    time.sleep(2)
#    test_steer_motor("stop")

