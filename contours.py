import cv2 as cv

def findContours(thresholdedImage):
    return cv.findContours(thresholdedImage, cv.REVR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

def findContourBoundingBox(contour):
    return cv.boundingRect(contour)

def findContourArea(contour):
    return cv.contourArea(contour)

def findContourConvexHull(contour):
        return cv.convexHull(contour)

def sortContoursByArea(contours, reverseOrder):
    # return sorted(contours, key=lambda x: cv.contourArea(x))
    return sorted(contours, key=cv.contourArea, reverse=reverseOrder)[:1]