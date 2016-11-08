import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(1):
	# Read Frame One
	fgbg = cv2.BackgroundSubtractorMOG()
	ret, frame = cap.read()
	fgbg.apply(frame)

	# Compare Frame Two
	ret, frame = cap.read()
	fgmask = fgbg.apply(frame)

	cv2.imshow('Frame',fgmask)
    
    # Check For Close
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()