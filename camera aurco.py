import numpy as np
import cv2
from matplotlib import pyplot as plt
import cv2.aruco as aruco
import math

marker = cv2.imread('aruco42.png',0)
cap = cv2.VideoCapture(0)



while(cap.isOpened()):
    ret, marker = cap.read()

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
    marker, aruco_dict, parameters=parameters)
    print("Corners:",  corners, "IDs:", ids)
    aruco.drawDetectedMarkers(marker, corners, ids)
    
    cv2.namedWindow('Aruco Detection', cv2.WINDOW_NORMAL)
    cv2.imshow('Aruco Detection', marker)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
# When everything done, release the capture
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
