''' Video Recorder
Capture and record video stream from input device

Created by Harris Christiansen on Dec 3, 2014
Project: HackSC Fall 2014 - https://devpost.com/software/ifollow-quadcopter
'''
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
#cap.set(3,1028)
#cap.set(4,720)

# video recorder
fps = 15
ret, frame = cap.read()
capSize = (np.size(frame, 1),np.size(frame, 0)) # this is the size of my source video
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
vout = cv2.VideoWriter()
out = vout.open('output.mov',fourcc,fps,capSize,True) 

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    vout.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
vout.release()
cv2.destroyAllWindows()
