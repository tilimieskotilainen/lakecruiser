# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import datetime


# initialize the camera and grab a reference to the raw camera capture

x_res = 640
y_res = 480
frate = 20

target_x = x_res/2

camera = cv2.VideoCapture(0)
camera.set(3, x_res)
camera.set(4, y_res)
camera.set(5, frate)

font = cv2.FONT_HERSHEY_COMPLEX

diff = 0
y_median = 0

#Determines whether shape detection is turned on or off
detect = False


def calculate_diff(status):
    global diff
    global y_median

    rawCapture = PiRGBArray(camera, size=(x_res, y_res)) ###TÄMÄ ON EPÄVARMA TOIMIIKO VAI EI
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera
    
    outer_shape = []
    inner_shape = []

    marker_list = []
    x_marker = 0
    
    # using datetime module

    # ct stores current time
    ct = datetime.datetime.now()
    
    writer = cv2.VideoWriter('Recording {}.mp4'.format(ct), cv2.VideoWriter_fourcc(*'DIVX'), frate, (x_res,y_res))


    while status[0] == "run":
#    for frame in camera: #.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text

        ret, image = camera.read()


        if detect == True: #The below shape detection stuff only happens if the variable for detection is true

            success = False #To mark frame as target found or not found
            #Convert to grayscale
            imgGry = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            imgGry = cv2.GaussianBlur(imgGry, (5, 5), 1)
            
            #Set threshold with parameters Source, thresholdValue, maxVal, thresholdingTechnique
        #    ret , thresh = cv2.threshold(imgGry, 40 , 255, cv2.THRESH_BINARY)
            thresh = cv2.adaptiveThreshold(imgGry,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,10)
            
            #Identify contours
            contours , hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #TÄHÄN ASTI SIIRTO OK
            for cnt in contours:
                (xx, yy, ww, hh) = cv2.boundingRect(cnt)

                area = cv2.contourArea(cnt)
                approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                x = approx.ravel()[0]
                y = approx.ravel()[1]

    #            cv2.drawContours(image, [approx], 0, (0, 0, 200), 2)
                    
                if len(approx) == 4 and x > 1 and ww > hh and ww < 2 * hh and area > 50:
        #                cv2.rectangle(image, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)
                    cv2.drawContours(image, [approx], 0, (0, 200, 0), 4)
    #                cv2.putText( image, "Square", (x, y), font, 0.5, (0, 200, 0) )
                    outer_shape.append([xx, yy, ww, hh])

                if len(approx) == 5 and abs(ww / hh -1) < 0.3 and area > 30:
        #            cv2.rectangle(image, (xx, yy), (xx + ww, yy + hh), (0, 255, 0), 2)
                    cv2.drawContours(image, [approx], 0, (0, 200, 0), 4)
    #                cv2.putText( image, "Pentagon", (x, y), font, 0.5, (0, 0, 200) )
                    inner_shape.append([xx, yy, ww, hh])

            for outer in outer_shape:
                for inner in inner_shape:
                    if inner[0] > outer[0] and inner[0] + inner[2] < outer[0] + outer[2]:
                        if inner[1] > outer[1] and inner[1] + inner[3] < outer[1] + outer[3]:
                            marker_list.append(inner[0] + int(inner[2] / 2))
                            if len(marker_list) > 5:
                                marker_list.pop(0)
                                success = True #To mark frame as successful in finding mark
    #                        cv2.line(image, (inner[0], 0), (inner[0], y_res), (255, 0, 0), 1)
                            break
                
            inner_shape.clear()
            outer_shape.clear()

            if len(marker_list) > 4:
                x_marker_sorted = marker_list.copy()
                x_marker_sorted.sort()
                x_marker = x_marker_sorted[2]
                cv2.line(image, (x_marker, 0), (x_marker, y_res), (0, 200, 0), 2)
                x_marker_sorted.clear()
            
            if x_marker > 0 and success == True:
    #            cv2.line(image, (x_marker, 0), (x_marker, y_res), (200, 0, 0), 1)
                diff = x_marker - target_x
            else:
                diff = 0

        # show the frame
        cv2.imshow("Frame", image)
        
        if detect == True: #Show mask frame only if detection is set to True
            cv2.imshow("Mask", thresh)
            print("Shoot:", diff)

        writer.write(image)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        

    writer.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    status = ["run"]
    calculate_diff(status)

