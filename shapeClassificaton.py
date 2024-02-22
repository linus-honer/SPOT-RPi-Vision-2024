import cv2
import numpy as np
import contours as contourUtil
from enum import Enum

def classifyShapeFromImage(image):
    returnShape = Shape.NONE

    img = image

    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    noise_removal = cv2.bilateralFilter(img_gray, 9, 75, 75)

    ret, thresh_image = cv2.threshold(noise_removal, 0, 255, cv2.THRESH_OTSU)
    canny_image = cv2.Canny(thresh_image, 250, 255)
    canny_image = cv2.convertScaleAbs(canny_image)

    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(canny_image, kernel, iterations=1)
    foundContours, h = contourUtil.findContours(dilated_image)
    foundContours = contourUtil.sortContoursByArea(foundContours, True)
    pt = (180, 3 * img.shape[0] // 4)
    for cnt in foundContours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

        if len(approx) == 6 :
            returnShape = Shape.CUBE
        elif len(approx) == 7:
            returnShape = Shape.CUBE
        elif len(approx) == 8:
            returnShape = Shape.CYLINDER
        elif len(approx) > 10:
            returnShape == Shape.CIRCLE



class Shape(Enum):
    NONE = "not assigned"
    CUBE = "cube"
    CYLINDER = "cyl"
    CIRCLE = "circle"

            