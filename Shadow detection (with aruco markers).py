import numpy as np
import cv2
from matplotlib import pyplot as plt
import cv2.aruco as aruco
import math

#Reading video stream:
cap = cv2.VideoCapture('vid1.mp4')
ret, frame = cap.read()
#Reading marker:
marker = cv2.imread('aruco42.png',0)
image = marker

marker = cv2.resize(marker,(127,119))

shape = marker.shape
#print(shape)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #Conversion to greyscale and thresholding:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret1,marked = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    th1 = ~marked
    marked = ~marked

    #Drawing the markers on the binary thresholded image:
    for i in range(119):
        for j in range(127):
            marked[360+i,550+j] = marker[i,j]
            marked[490+i,700+j] = marker[i,j]
            marked[360+i,700+j] = marker[i,j]
            marked[490+i,550+j] = marker[i,j]

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        marked, aruco_dict, parameters=parameters)
    #print("Corners:",  corners, "IDs:", ids)
    #aruco.drawDetectedMarkers(marker, corners, ids)

    #Corner points for region of interest extracted:
    try:
        corner0 = corners[0]
        corner0 = corner0[0,:]
        corRow0 = corner0[:,0]
        corCol0 = corner0[:,1]

        corner1 = corners[1]
        corner1 = corner1[0,:]
        corRow1 = corner1[:,0]
        corCol1 = corner1[:,1]

        corner2 = corners[2]
        corner2 = corner2[0,:]
        corRow2 = corner2[:,0]
        corCol2 = corner2[:,1]

        if len(corners)>=3:
            rowArr = [corRow0,corRow1,corRow2]
            colArr = [corCol0,corCol1,corCol2]
            minRow = min(rowArr[0])
            minCol = min(colArr[0])
            maxRow = max(rowArr[0])
            maxCol = max(colArr[0])
            for i in range(3):
                if min(rowArr[i])<minRow:
                    minRow = min(rowArr[i])
                if max(rowArr[i])>maxRow:
                    maxRow = max(rowArr[i])
                if min(colArr[i])<minCol:
                    minCol = min(colArr[i])
                if max(colArr[i])>maxCol:
                    maxCol = max(colArr[i])
            #mistakenly exchanged rows with columns in the
            #above processing. correcting below:
            temp = minRow
            minRow = minCol
            minCol = temp
            
            temp = maxRow
            maxRow = maxCol
            maxCol = temp
            #print("minRow:" ,minRow, "maxRow:", maxRow)
            #print("minCol:" ,minCol, "maxCol:", maxCol)
    except:
        pass

    rowMin = int(minRow)
    rowMax = int(maxRow)
    colMin = int(minCol)
    colMax = int(maxCol)
    
    #rowMin = 210+119#369
    #rowMax = 550+7#557
    #colMin = 450 + 119#569
    #colMax = 800+7#807
    #cv2.circle(frame,(rowMin,colMin), 63, (0,0,255), -1)
    #cv2.circle(frame,(rowMax,colMax), 63, (0,0,255), -1)

    #Drawing contours on the detected shadow within ROI:
    newFrame = th1[rowMin:rowMax,colMin:colMax]
    try:
        im2, contours, _ = cv2.findContours(newFrame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        maxCont = max(contours, key = cv2.contourArea)
        cv2.drawContours(frame[rowMin:rowMax,colMin:colMax], maxCont, -1, (0,255,0), 3)
    except:
        pass
    #x,y,w,h = cv2.boundingRect(maxCont)
    #cv2.rectangle(frame[rowMin:rowMax,colMin:colMax],(x,y),(x+w,y+h),(0,255,0),2)
    
    
    
    # Display the resulting frame
    cv2.namedWindow('BW Mask', cv2.WINDOW_NORMAL)
    cv2.imshow('BW Mask', marked)
    cv2.namedWindow('Detection', cv2.WINDOW_NORMAL)
    cv2.imshow('Detection',frame)
    newFrame = frame[rowMin:rowMax,colMin:colMax]
    try:
        cv2.namedWindow('newFrame', cv2.WINDOW_NORMAL)
        cv2.imshow('newFrame',newFrame)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
