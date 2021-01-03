
# import the necessary packages
from imutils import contours
from skimage import measure
import argparse
import numpy as np
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--video", help="path to the video file")
args = vars(ap.parse_args())
cap = cv2.VideoCapture(args["video"])

while(cap.isOpened()):

	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (11, 11), 0)

	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blurred)

	thresh = cv2.threshold(blurred, maxVal-2, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.erode(thresh, None, iterations=2)
	thresh = cv2.dilate(thresh, None, iterations=4)

	labels = measure.label(thresh, neighbors=8, background=0)
	mask = np.zeros(thresh.shape, dtype="uint8")

	for label in np.unique(labels):
		if label == 0:
			continue

		labelMask = np.zeros(thresh.shape, dtype="uint8")
		labelMask[labels == label] = 255
		numPixels = cv2.countNonZero(labelMask)

		if numPixels > 500:
			mask = cv2.add(mask, labelMask)


	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	for (i, c) in enumerate(cnts):

		(x, y, w, h) = cv2.boundingRect(c)
		((cX, cY), radius) = cv2.minEnclosingCircle(c)
		cv2.circle(frame, (int(cX), int(cY)), int(radius),
			(0, 0, 255), 3)
		cv2.putText(frame, "Sun", (x, y - 15),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	# define the screen resulation
	screen_res = 1280, 720
	scale_width = screen_res[0] / frame.shape[1]
	scale_height = screen_res[1] / frame.shape[0]
	scale = min(scale_width, scale_height)

	# resized window width and height
	window_width = int(frame.shape[1] * scale)
	window_height = int(frame.shape[0] * scale)

	# cv2.WINDOW_NORMAL makes the output window resizealbe
	cv2.namedWindow('Resized Window', cv2.WINDOW_NORMAL)

	# resize the window according to the screen resolution
	cv2.resizeWindow('Resized Window', window_width, window_height)

	cv2.imshow('Thresholding', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
			break

cap.release()
cv2.destroyAllWindows()