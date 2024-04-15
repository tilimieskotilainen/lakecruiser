import sys
import time
import RPi.GPIO as GPIO
import threading
import board
import busio
import adafruit_vl53l0x
import math


GPIO.setmode(GPIO.BCM)
GPIO_pins = (22, 18, 27, 17)
gpiopins = GPIO_pins

wait = 0.005
initdelay = 0.05
steptype = "full"
batch = 100 #How much to turn the stepper at a time

i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
neutral = 115
movement = 85 # mm in each direction from center
threshold = 10
angle_movement = 45


def steer_direction(target):

    """motor_run,  moves stepper motor based on 7 inputs

     (1) GPIOPins, type=list of ints 4 long, help="list of
     4 GPIO pins to connect to motor controller
     These are the four GPIO pins we will
     use to drive the stepper motor, in the order
     they are plugged into the controller board. So,
     GPIO 18 is plugged into Pin 1 on the stepper motor.
     (2) wait, type=float, default=0.001, help=Time to wait
     (in seconds) between steps.
     (3) steps, type=int, default=512, help=Number of steps sequence's
     to execute. Default is one revolution , 512 (for a 28BYJ-48)
     (4) counterclockwise, type=bool default=False
     help="Turn stepper counterclockwise"
     (5) verbose, type=bool  type=bool default=False
     help="Write pin actions",
     (6) steptype, type=string , default=half help= type of drive to
     step motor 3 options full step half step or wave drive
     where full = fullstep , half = half step , wave = wave drive.
     (7) initdelay, type=float, default=1mS, help= Intial delay after
     GPIO pins initialized but before motor is moved.

    """
    try:
        for pin in GPIO_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        time.sleep(initdelay)

        # select step based on user input
        # Each step_sequence is a list containing GPIO pins that should be set to High
        if steptype == "half":  # half stepping.
            step_sequence = list(range(0, 8))
            step_sequence[0] = [gpiopins[0]]
            step_sequence[1] = [gpiopins[0], gpiopins[1]]
            step_sequence[2] = [gpiopins[1]]
            step_sequence[3] = [gpiopins[1], gpiopins[2]]
            step_sequence[4] = [gpiopins[2]]
            step_sequence[5] = [gpiopins[2], gpiopins[3]]
            step_sequence[6] = [gpiopins[3]]
            step_sequence[7] = [gpiopins[3], gpiopins[0]]
        elif steptype == "full":  # full stepping.
            step_sequence = list(range(0, 4))
            step_sequence[0] = [gpiopins[0], gpiopins[1]]
            step_sequence[1] = [gpiopins[1], gpiopins[2]]
            step_sequence[2] = [gpiopins[2], gpiopins[3]]
            step_sequence[3] = [gpiopins[0], gpiopins[3]]
        elif steptype == "wave":  # wave driving
            step_sequence = list(range(0, 4))
            step_sequence[0] = [gpiopins[0]]
            step_sequence[1] = [gpiopins[1]]
            step_sequence[2] = [gpiopins[2]]
            step_sequence[3] = [gpiopins[3]]
        else:
            print("Error: unknown step type ; half, full or wave")
            quit()
            
        step_sequence_rev = step_sequence.copy()
        step_sequence_rev.reverse()


        # Iterate through the pins turning them on and off.
        while True:

#Tähän if-lauseke joka vertaa sijaintia tahtotilaan
            
            target_position = neutral + target[0] / angle_movement * movement
            
            if target[0] > angle_movement:
                target_position = neutral + movement
            elif target[0] < -angle_movement:
                target_position = neutral - movement

            print("Target position:", target_position)


            measurement = []
            for repeater in range(5):
                measurement.append(vl53.range)
                time.sleep(0.01)
            tof = round(sum(measurement) / len(measurement))
            print("TOF:", tof)
            measurement.clear()

            gap = target_position - tof
            print("GAP:", gap)
            
            if gap < -threshold:
                for step in range(batch):
                    for pin_list in step_sequence_rev:
                        for pin in gpiopins:
                            if pin in pin_list:
                                GPIO.output(pin, True)
                            else:
                                GPIO.output(pin, False)
                        time.sleep(wait)
            elif gap > threshold:
                for step in range(batch):
                    for pin_list in step_sequence:
                        for pin in gpiopins:
                            if pin in pin_list:
                                GPIO.output(pin, True)
                            else:
                                GPIO.output(pin, False)
                        time.sleep(wait)

            for pin in gpiopins:
                GPIO.output(pin, False)
            print("Pins off")



    finally:
        # switch off pins at end
        for pin in gpiopins:
            GPIO.output(pin, False)

if __name__ == "__main__":
    test = [-90]
    steering_thread = threading.Thread(target=steer_direction, args=(test,), daemon=True)
    steering_thread.start()
    while True:
        print("Enter target angle")
        test[0] = int(input())
    

