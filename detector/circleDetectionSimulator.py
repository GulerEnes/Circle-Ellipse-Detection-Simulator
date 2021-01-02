"""
2 January 2021
Written by Enes Güler
Contact on twitter.com/FuzuliKral
"""
import cv2 as cv
import numpy as np
from os import remove


def circleDetector(_):
    img = np.ones([500, 500], dtype=np.uint8) * 255  # white background with size 500x500 px

    # inputs from trackbars
    showAll = cv.getTrackbarPos('showAll', frameName)
    showEstimated = cv.getTrackbarPos('showEstimated', frameName)
    thickness = cv.getTrackbarPos('Thickness', frameName)
    dAngle = cv.getTrackbarPos('DrawnAngle', frameName)
    major = cv.getTrackbarPos('Major', frameName)
    minor = cv.getTrackbarPos('Minor', frameName)

    p1 = cv.getTrackbarPos('p1', frameName)  # HoughCircle function's param1
    p2 = cv.getTrackbarPos('p2', frameName)  # HoughCircle function's param2

    if minor == 0:  # to avoid zero division error
        cv.setTrackbarPos('Minor', frameName, 1)
        minor = 1
    if minor < major:  # we only interest with major >= minor
        cv.setTrackbarPos('Minor', frameName, major)
        minor = major

    angle = np.arccos(major / minor) * 180 / np.pi  # look angle

    cv.ellipse(img, (250, 250), (major, minor), 0, 0, dAngle, (0, 0, 0), thickness)  # drawn ellipse
    cv.circle(img, (250, 250), 2, (0, 0, 0), 3)  # center

    # Finding circles
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20, param1=p1, param2=p2, minRadius=0, maxRadius=250)

    # converting BGR mode to draw colored things
    cv.imwrite('ellipse.png', img)
    img = cv.imread('ellipse.png', 1)

    try:
        detected_circles = np.uint16(np.around(circles))
        noc = len(detected_circles[0])  # Number of Detected Circles
        cv.putText(img, "Number of Circles " + str(noc), (10, 20), font, .5, (0, 0, 0), 1, cv.LINE_AA)

        estimatedCircle = [0, 0, 0]  # initializing (x, y, r) of estimated circle
        for (x, y, r) in detected_circles[0, :]:
            if showAll == 1:
                cv.circle(img, (x, y), r, (0, 255, 0), 3)  # detected circle
                cv.circle(img, (x, y), 2, (255, 0, 0), 3)  # center
            estimatedCircle = [i[0] + i[1] for i in zip(estimatedCircle, [x, y, r])]
        if showEstimated == 1 and estimatedCircle[2] != 0:
            x, y, r = [int(i / noc) for i in estimatedCircle]
            cv.circle(img, (x, y), r, (0, 0, 255), 3)  # estimated circle
            cv.circle(img, (x, y), 2, (255, 0, 255), 3)  # center
    except:
        cv.putText(img, "No Circle!", (10, 30), font, 1, (0, 0, 255), 2, cv.LINE_AA)
    finally:
        cv.putText(img, "Look Angle: " + str(angle), (350, 20), font, .5, (0, 0, 0), 1, cv.LINE_AA)
        cv.putText(img, "All circles", (10, 475), font, .5, (0, 255, 0), 1, cv.LINE_AA)
        cv.putText(img, "/their centers", (90, 475), font, .5, (255, 0, 0), 1, cv.LINE_AA)
        cv.putText(img, "Estimated circles", (10, 490), font, .5, (0, 0, 255), 1, cv.LINE_AA)
        cv.putText(img, "/its center", (145, 490), font, .5, (255, 0, 255), 1, cv.LINE_AA)
        cv.imshow(frameName, img)


font = cv.FONT_HERSHEY_SIMPLEX
frameName = 'Circle Detection Simulator'
cv.namedWindow(frameName)

cv.createTrackbar('Major', frameName, 100, 240, circleDetector)  # Vertical length
cv.createTrackbar('Minor', frameName, 100, 240, circleDetector)  # Horizontal length
cv.createTrackbar('Thickness', frameName, 3, 20, circleDetector)
cv.createTrackbar('DrawnAngle', frameName, 345, 360, circleDetector)
cv.createTrackbar('p1', frameName, 100, 200, circleDetector)  # HoughCircle function's param1
cv.createTrackbar('p2', frameName, 35, 150, circleDetector)  # HoughCircle function's param2
cv.createTrackbar('showAll', frameName, 1, 1, circleDetector)
cv.createTrackbar('showEstimated', frameName, 1, 1, circleDetector)

cv.setTrackbarPos('Minor', frameName, 1)  # dummy process to start program

if cv.waitKey(0) == ord('q'):  # to avoid auto close situation
    cv.destroyAllWindows()

remove('ellipse.png')  # removing temp png file
