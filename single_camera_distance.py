# Import Packages
import numpy as np
import cv2
import cv2.aruco as aruco
import math

# Calculate Hipotenus
def hipotenus(x1, x2, y1, y2):
    xfark = x2 - x1
    yfark = y2 - y1
    return math.sqrt(math.pow(xfark, 2) + math.pow(yfark, 2))
# -----

# Capture Frame from Webcam (V4L)
cap = cv2.VideoCapture(0)
# -----

# Camera Resolution Settings
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# -----

KNOWN_LENGTH = 50 #cm

# Multi Frame Start
while (True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    parameters = aruco.DetectorParameters_create()
    
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # IF DETECT ARUCO MARKER
    if len(corners) >= 1 and markerID == 373:

        hip1 = hipotenus((corners[0][0])[0][0], (corners[0][0])[1][0], (corners[0][0])[1][1], (corners[0][0])[2][1])
        hip2 = hipotenus((corners[0][0])[3][0], (corners[0][0])[2][0], (corners[0][0])[1][1], (corners[0][0])[2][1])

        if hip1 != 0 and hip2 != 0:
            dist = KNOWN_LENGTH * (245 * math.sqrt(2)) / hip1
            dist2 = KNOWN_LENGTH * (245 * math.sqrt(2)) / hip2
        else:
            dist = 0
            dist2 = 0

        frame = aruco.drawDetectedMarkers(frame, corners)
        
        # if distance is less than 101
        if dist <= 100:
            cv2.line(frame, ((corners[0][0])[0][0], (corners[0][0])[0][1]),
                     ((corners[0][0])[2][0], (corners[0][0])[2][1]), (0, 255, 0), 1)
               
        # if distance is between 101 and 199
        elif dist > 100 and dist < 200:
            cv2.line(frame, ((corners[0][0])[0][0], (corners[0][0])[0][1]),
                     ((corners[0][0])[2][0], (corners[0][0])[2][1]), (0, 150, 255), 1)
        
        else:
            cv2.line(frame, ((corners[0][0])[0][0], (corners[0][0])[0][1]),
                     ((corners[0][0])[2][0], (corners[0][0])[2][1]), (0, 0, 255), 1)

        # DISTANCE GROUNDS
        cv2.rectangle(frame, (5, 5), (160, 27), (0, 0, 0), -1)
        cv2.rectangle(frame, (5, 33), (160, 55), (0, 0, 0), -1)
        # DISTANCE TEXTS
        cv2.putText(frame, ("DIST1: " + str('%.2f' % dist) + " cm"), (int(10), int(20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255))
        cv2.putText(frame, ("DIST2: " + str('%.2f' % dist2) + " cm"), (int(10), int(48)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255))
        # ARUCO FOUND GROUND
        cv2.rectangle(frame, (500, 462), (640, 480), (0, 190, 50), -1)
        # ARUCO FOUND TEXT
        cv2.putText(frame, ("ArUco FOUND"), (510, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))

    # IF CANT DETECT ARUCO MARKER
    elif len(corners) == 0:
        # ARUCO NOT FOUND GROUND
        cv2.rectangle(frame, (500, 462), (640, 480), (0, 0, 255), -1)
        # ARUCO NOT FOUND TEXT
        cv2.putText(frame, ("ArUco NOT FOUND"), (510, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
