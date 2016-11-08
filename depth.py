import numpy as np
import cv2

imgL = cv2.imread('tsucuba_left.png',0)
imgR = cv2.imread('tsucuba_right.png',0)

#stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET, ndisparities=16, SADWindowSize=15)

window_size = 3
min_disp = 16
num_disp = 112-min_disp
stereo = cv2.StereoSGBM(minDisparity = min_disp,
	numDisparities = num_disp,
	SADWindowSize = window_size,
	uniquenessRatio = 10,
	speckleWindowSize = 200,
	speckleRange = 32,
	disp12MaxDiff = 1,
	P1 = 8*3*window_size**2,
	P2 = 32*3*window_size**2,
	fullDP = False
)

disparity = stereo.compute(imgL,imgR).astype(np.float32) / 16.0
cv2.imshow('Disparity',(disparity-min_disp)/num_disp)

while(True):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cv2.destroyAllWindows()