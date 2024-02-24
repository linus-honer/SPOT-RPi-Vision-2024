import cv2
import numpy as np
import contours as contourUtil
from enum import Enum

def classifyShapeFromImage(image):
    returnShapes = []

    img = image

    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    noise_removal = cv2.bilateralFilter(img_gray, 9, 75, 75)

    thresh_image = cv2.threshold(noise_removal, 0, 255, cv2.THRESH_OTSU)
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
            returnShapes.append(ShapeEnum.CUBE)
        elif len(approx) == 7:
            returnShapes.append(ShapeEnum.CUBE)
        elif len(approx) == 8:
            returnShapes.append(ShapeEnum.CYLINDER)
        elif len(approx) > 10:
            returnShapes.append(ShapeEnum.CIRCLE)
    
    boundingBox = contourUtil.findContourBoundingBox(foundContours[0])
    shapeX = boundingBox[0] + boundingBox[2] // 2
    shapeY = boundingBox[1] + boundingBox[3] // 2
    shapeArea = contourUtil.findContourArea(foundContours[0])

    return Shape(contourObj=foundContours[0], shapeID=returnShapes[0], kX=shapeX, kY=shapeY, kA=shapeArea)

class ShapeEnum(Enum):
    NONE = "not assigned"
    CUBE = "cube"
    CYLINDER = "cyl"
    CIRCLE = "circle"

class Shape:
    def __init__(self, contourObj, shapeID, kX, kY, kA):
        self.contourA = contourObj
        self.shapeName = shapeID
        self.x = kX
        self.y = kY
        self.area = kA
        return
    
    def getShape(self):
        return self.shapeName
    
    def getCenter(self):
        return (self.kX, self.kY)
    
    def getBoundingBox(self):
        return contourUtil.findContourBoundingBox(self.contourA)