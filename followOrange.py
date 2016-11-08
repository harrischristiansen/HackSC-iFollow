''' Follow Orange
Locate largest orange target, calculate throttles to follow target with quadcopter, output throttles over serial

Created by Harris Christiansen on Dec 3, 2014
Project: HackSC Fall 2014 - https://devpost.com/software/ifollow-quadcopter
'''
import numpy as np
import cv2
import serial
import time

cap = cv2.VideoCapture(0)

# Get First Frames
ret, frame = cap.read()

# Video Recorder
fps = 15
capSize = (np.size(frame, 1)*2,np.size(frame, 0)) # this is the size of my source video
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
#vout = cv2.VideoWriter()
#out = vout.open('recording.mov',fourcc,fps,capSize,True)

# Serial Port
ser = serial.Serial('/dev/tty.usbmodem1421', 115200)

# Get Stable Throttle Factor
throttleAdd = 0;
def throttleSet(_):
	global throttleAdd
	throttleAdd = cv2.getTrackbarPos("Throttle", "Tracker")
	print throttleAdd
cv2.namedWindow('Tracker')
cv2.createTrackbar("Throttle", "Tracker", 0, 20, throttleSet)
cv2.imshow("Tracker", frame)
while(True):
	ser.write(" 398 " + str(964 + throttleAdd) + " 696 98 ")
	# Check For Save
	if cv2.waitKey(1000) & 0xFF == ord('s'):
		break
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	frameOrig = frame.copy()
	height, width, depth = frame.shape
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Blur and Convert To HSV
	#frame = cv2.blur(frame,(10,10))
	frame = cv2.medianBlur(frame,13)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Search Color
	lowerColor = np.array([1,90,100])
	upperColor = np.array([14,255,255])

	# Threshold Image
	mask = cv2.inRange(hsv, lowerColor, upperColor)
	maskRes = cv2.bitwise_and(frame,frame, mask= mask)
	grayMaskRes = cv2.cvtColor(maskRes, cv2.COLOR_BGR2GRAY)

	# Find Object And Circle
	moments = cv2.moments(mask, 0)
	area = moments['m00']
	if(area > 500000):
		x = (int) (moments['m10'] / area)
		y = (int) (moments['m01'] / area)
	else:
		x = width/2
		y = 200

	# Calculate Result
	#result = cv2.addWeighted(maskRes,0.7,frame,0.3,0)
	result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
	result[grayMaskRes != 0] = (0,0,255)

	# Display Result
	centerPoint = (x,y)
	cv2.circle(result, centerPoint, 20, 255, 2)
	vis = np.hstack((frameOrig,result))
	#vout.write(vis)
	cv2.imshow('Tracker',vis)

	##### Output To Serial #####

	# Off From Center
	offFromCenter = (x-(width/2))/4
	if(offFromCenter>100):
		offFromCenter = 100
	if(offFromCenter<-100):
		offFromCenter = -100
	offFromCenter = (int)(-1 * offFromCenter * abs(offFromCenter) / 100) + 696
	if(offFromCenter>700):
		print("Turning Left")
	else:
		print("Turning Right")

	# Off From Target
	if(area<800000): # Out of View
		print("Out Of View")
		offFromTarget=98
	elif(area<5000000): # Go Toward
		print("Toward")
		offFromTarget=107
	elif(area>10000000): # Go Away
		print("Away")
		offFromTarget=89
	else: # Perfect Distance
		print("Perfect")
		offFromTarget=98
	#print offFromCenter

	# Up and Down
	upDown = 964 + throttleAdd
	upFromCenter = (y-(height/2))

	if(upFromCenter>100):
		print("Going Down")
		upDown = 960 + throttleAdd
	if(upFromCenter<-100):
		print("Going Up")
		upDown = 973 + throttleAdd

	ser.write(" 392 " + str(upDown) + " " + str(offFromCenter) + " " + str(offFromTarget))

	# Check For Close
	if cv2.waitKey(10) & 0xFF == ord('q'):
		break

# Cleanup
cap.release()
#vout.release()
cv2.destroyAllWindows()
