# -*- coding: utf-8 -*-
# A motion detection program based on Adrian Rosebrock's code from
# http://www.pyimagesearch.com

#Log: 21/6/16
#Added specified area bounding
#Added object count in bounding area
#Added mouseXY location 
#Added center of x,y in bounding box of object

import cv2
import numpy as np
import argparse
import datetime
import imutils
import time

font=cv2.FONT_HERSHEY_COMPLEX
xlist=[]
ylist=[]

left_counter=0
right_counter=0

state=0
special_counter=0

#**************Mouse Coordinates***********
mouseX=None
mouseY=None
 
def draw_circle(event,x,y,flags,param):
    global mouseX
    mouseX=x
    global mouseY
    mouseY=y
    print (mouseX,mouseY)
#**************Mouse Coordinates***********

cv2.namedWindow('frame')
cv2.setMouseCallback("frame",draw_circle)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# if the video argument is None, then we are reading from webcam
# otherwise, we are reading from a video file
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25) 
	cv2.setMouseCallback("frame",draw_circle)
else:
	camera = cv2.VideoCapture(args["video"])


firstFrame = None


# loop over the frames of the video
while True:
	(grabbed, frame) = camera.read()
	text = "Undetected"

	# if the frame could not be grabbed, we have reached the end of the video
	if not grabbed:
		break
 
	# 1.Resize frame to 500pixels 2.Convert it to grayscale 3.Blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue
		
	# compute the absolute difference bet. current frame & first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	# We then threshold frameDelta
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, 
	thresh = cv2.dilate(thresh, None, iterations=2)
	#then find contours on thresholded image
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create a black image, a window and bind the function to window
        if mouseX!=None and mouseY!=None:
            cen="x: %d y: %d" %(mouseX,mouseY)
            cv2.putText(frame,cen,(mouseX,mouseY),font,0.5,(200,255,255),1,cv2.LINE_AA)      
            print (mouseX,mouseY)

        #Rectangle map out the area
        cv2.rectangle(frame, (0, 190), (200, 360), (0, 255, 0), 2)
	
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# compute BOUNDING BOX for CONTOUR (C), draw it on the frame, & update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #draw rectangle for each c! 
           	print "x,y: ", x,y
                        	         	
           	
           	#Moments - find center x,y 
           	M = cv2.moments(c)
                if ["m00"] !=0 and M["m00"]!=0:
                        center = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]
                        coord="x: %d y: %d" %(center[0],center[1])
                        #area = cv2.contourArea(M["m00"])     #!!!
                        cv2.putText(frame, coord, (center[0],center[1]),font,1,(200,255,255),1,cv2.LINE_AA)
                        #cv2.putText(frame, (10,50), area,font,1,(200,255,255),1,cv2.LINE_AA)	
	                text = "Detected"
	                
	        if 0<center[0]<200 & 190<center[1]<360:
                    if state == 0:
                        special_counter+=1
                    state=1 
                    print "Special! State: ", state, "Counter: ", special_counter
                else:
                    state=0
                    print "Normal. State: ", state, "Counter: ", special_counter
	             
                    		     		
   	# draw the text and timestamp on the frame
   	cv2.putText(frame, "Movement: {}".format(text), (10, 20),
   	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
   	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
  		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	cv2.imshow("frame", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()










