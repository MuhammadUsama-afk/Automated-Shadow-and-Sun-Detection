# Automated-Shadow-and-Sun-Detection

Dependencies:

-Python 3.x
-Numpy
-OpenCV 3.3+ Contrib modules
-Aruco (https://github.com/njanirudh/Aruco_Tracker)
-imutils
-skimage

-----------------------------------------

Video used in example of shadow detection: https://www.youtube.com/watch?v=9fEfX3KNxVg

-----------------------------------------
Some Notes on shadow detection

-If a version of opencv is installed then please uninstall it and install opencv-contrib using opencv-contrib-python
-The aruco markers detected need to be 4x4 (6x6 if the outer black borders are considered), sample markers have been provided

-----------------------------------------
For Sun detection, enter following commands in cmd along with video you want to see:

python brightest_spot.py --video 1.mp4

or

python threshold_connectivity.py --video 1.mp4

or

python template_match.py --video 1.mp4
