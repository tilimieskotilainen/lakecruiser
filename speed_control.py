import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
GPIO.output(19, GPIO.LOW)
pwm_fwd = GPIO.PWM(13, 1000) # Set Frequency to 1 KHz
pwm_rev = GPIO.PWM(19, 1000)
pwm_fwd.start(0) # Set the starting Duty Cycle
pwm_rev.start(0)

max_speed = 80
max_rev = -40


def propulsion(speed):
    
    if speed > max_speed:
        speed = max_speed
        print("Max speed limited to:", max_speed)
    if speed < max_rev:
        speed = -max_rev
        print("Max reverse limited to:", max_rev)


    if speed > 0:
        pwm_rev.ChangeDutyCycle(0)
        pwm_fwd.ChangeDutyCycle(speed)
        print("Forward", speed)
    elif speed < 0:
        pwm_fwd.ChangeDutyCycle(0)
        pwm_rev.ChangeDutyCycle(-speed)
        print("Reverse", speed)
    else:
        pwm_fwd.ChangeDutyCycle(0)
        pwm_rev.ChangeDutyCycle(0)
        GPIO.cleanup()
        print("Stopped")
     
if  __name__ == '__main__':
    propulsion(-100)