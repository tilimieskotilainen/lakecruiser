#This is the backbone of the code, initiating the various stages of the journey based on trigger events
#import asyncio
#import websockets
#import shoot_and_calculate
#import trip_dist_calculator
#import breadcrumb_calculator
#import Approach
#import webbrowser

#For threads to start:
import read_gps
import steering_servo
import compass_reader
import Lautta_GUI

#For actions in backbone:
import json
import threading
import time
import gps_cruise
import Specs

read_gui_thread = threading.Thread(target=Lautta_GUI.gui_loop, args=(), daemon=True) #Define GUI thread
read_gui_thread.start() # Start GUI thread
time.sleep(1)
read_gps_thread = threading.Thread(target=read_gps.read_gps, args=(), daemon=True) #Define GPS thread
read_gps_thread.start() # Start GPS thread
time.sleep(1)
read_compass_thread = threading.Thread(target=compass_reader.read_compass, args=(), daemon=True) #Define compass thread
read_compass_thread.start() # Start compass thread
time.sleep(1)
steering_thread = threading.Thread(target=steering_servo.steer, args=(), daemon=True) #Define compass thread
steering_thread.start() # Start compass thread
time.sleep(1)

#Funktio joka lähtee pyörimään, kun UI:ssa valitaan statukseksi "run"
def run():
    gps_cruise.captain()
    print("GPS Cruise ended")


def route_choice():
    while True:
        print("Select route:", Lautta_GUI.routes_list)
        x = input()
        if x in Lautta_GUI.routes_list:
            Specs.route = x
            Specs.update_calc()
        print("Press R to run route, C to change route selection")
        y = input()
        if y == "R":
            run()
        elif y == "C":
            pass
        else:
            print("Invalid selection!")
            pass

route_choice()

#run()
