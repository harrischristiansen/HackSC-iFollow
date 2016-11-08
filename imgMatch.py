import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	img = frame.copy()
	template = cv2.imread('shirt.jpg',0)
	w, h = template.shape[::-1]

	# All the 6 methods for comparison in a list
	methods = ['cv2.TM_CCOEFF']
	''' 'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
		'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']'''

	for meth in methods:
		img = frame.copy()
		method = eval(meth)

		# Apply template Matching
		res = cv2.matchTemplate(img,template,method)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

		# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			top_left = min_loc
		else:
			top_left = max_loc

		# Center Box
		#top_left = list(top_left)
		#top_left[0] = top_left[0] + w/2 - 75
		#top_left[1] = top_left[1] + h/2 - 75
		#top_left = tuple(top_left)
		bottom_right = (top_left[0] + 150, top_left[1] + 150)

		cv2.rectangle(img,top_left, bottom_right, 255, 2)
		cv2.imshow("Test",res);
		cv2.imshow("Test2",img);

	# Check For Close
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()