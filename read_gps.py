import serial
from pynmea import nmea
import time


#Specs for GPS module
ser = serial.Serial('/dev/serial0') #Aikaisemmin käytetty
ser.baudrate=9600

current_min = (0.0, 0.0)

#Reads gps coordinates and returns current location in minutes and decimals
def read_gps():

    print("GPS Running")

    global current_min

    #Variable for ensuring readings are printed only once
    gps_read_cycle = 1

    while True:
        try:
            message = ser.readline().decode()
            if '$GNGGA' in message:
                message_list = message.split(",")
                lat = message_list[2]
                lon = message_list[4]
                lat_min = round(float(lat[0:2]) * 60 + float(lat[2:]), 6)
                lon_min = round(float(lon[0:3]) * 60 + float(lon[3:]), 6)
                current_min = (lat_min, lon_min)


                # Code to print gps results once, but only once.
                if gps_read_cycle == 1:
                    print(message)
                    print (current_min)
                    print ("GPS continuing to run without further prints")
                gps_read_cycle = gps_read_cycle + 1

#                return(current_min)
        except:
            print("No GPS-signal")
            time.sleep(5)
            pass
        time.sleep(1)
        
if __name__ == "__main__":
    read_gps()