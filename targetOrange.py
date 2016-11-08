''' Target Orange
Locate and draw target on largest Orange target

Created by Harris Christiansen on Dec 3, 2014
Project: HackSC Fall 2014 - https://devpost.com/software/ifollow-quadcopter
'''
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# video recorder
fps = 15
ret, frame = cap.read()
capSize = (np.size(frame, 1),np.size(frame, 0)) # this is the size of my source video
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
#vout = cv2.VideoWriter()
#out = vout.open('recording.mov',fourcc,fps,capSize,True)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert To HSV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Search Color
    lowerColor = np.array([0,100,100])
    upperColor = np.array([14,255,255])

    # Threshold Image
    mask = cv2.inRange(hsv, lowerColor, upperColor)
    maskRes = cv2.bitwise_and(frame,frame, mask= mask)
    grayMaskRes = cv2.cvtColor(maskRes, cv2.COLOR_BGR2GRAY)

    # Calculate Result
    #result = cv2.addWeighted(maskRes,0.7,frame,0.3,0)
    result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    result[grayMaskRes != 0] = (0,0,255)

    # Display Result
    #vout.write(grayColor)
    cv2.imshow('Target Orange',result)

    # Check For Close
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
#vout.release()
cv2.destroyAllWindows()
