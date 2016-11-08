''' Depth Cam
Attempt to determine distance to object using pair of images

Created by Harris Christiansen on Dec 3, 2014
Project: HackSC Fall 2014 - https://devpost.com/software/ifollow-quadcopter
'''
import numpy as np
import cv2
import time

#imgL = cv2.imread('tsucuba_left.png',0)
#imgR = cv2.imread('tsucuba_right.png',0)

cap = cv2.VideoCapture(0)

print("first")
ret, imgL = cap.read()
time.sleep(0.1)
print("second")
reg, imgR = cap.read()

imgL = cv2.resize(imgL, (0,0), fx=0.5, fy=0.5)
imgR = cv2.resize(imgR, (0,0), fx=0.5, fy=0.5) 

cap.release()

#stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET, ndisparities=16, SADWindowSize=15)

window_size = 3
min_disp = 0
num_disp = 112-min_disp
stereo = cv2.StereoSGBM(minDisparity = min_disp,
	numDisparities = num_disp,
	SADWindowSize = window_size
)
''',
	uniquenessRatio = 10,
	speckleWindowSize = 100,
	speckleRange = 32,
	disp12MaxDiff = 1,
	P1 = 8*3*window_size**2,
	P2 = 32*3*window_size**2,
	fullDP = False
)'''

disparity = stereo.compute(imgL,imgR).astype(np.float32) / 16.0
cv2.imshow('Disparity',(disparity-min_disp)/num_disp)
cv2.imshow('First',imgL)
cv2.imshow('Second',imgR)

while(True):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()