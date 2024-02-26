from time import time, sleep
import cv2
import logging

from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
import numpy as np
from cscore.imagewriter import ImageWriter
from shapeClassificaton import *

class ServerCore:
    '''Base class for the VisionServer'''

    def __init__(self, maxDetect):
        self.notes = []
        self.otherShapes = []
        self.maxDetect = maxDetect

    def visionConsolePrint(message):
        print(message)

    def processStream(self, inputImg):

        self.notes = []
        self.otherShapes = []

        biggestShape = classifyShapeFromImage(inputImg, self.maxDetect)

        if biggestShape.getShape == ShapeEnum.CIRCLE:
            self.notes.append(biggestShape)
        else:
            self.otherShapes.append(biggestShape)
    
    def validNote(self):
        if self.notes.count > 0:
            return True
        return False
    
    def detected(self):
        if self.notes.count > 0:
            if self.otherShapes.count > 0:
                return True
        return False
    
    def getNoteContour(self, index):
        return self.notes[index].getContour()

    def getNoteCenter(self, index):
        return self.notes[index].getCenter()
    
    def getNoteBoundingBox(self, index):
        return self.notes[index].getBoundingBox()

    def getShapeName(self, index):
        return self.otherShapes[index].getShape()
    
    def getShapeCenter(self, index):
        return self.otherShapes[index].getCenter()
    
    def getShapeBoundingBox(self, index):
        return self.getNoteBoundingBox()