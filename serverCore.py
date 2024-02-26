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

    def processStream(self, input_stream):
        self.notes = []
        self.otherShapes = []

        img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
        inputImg = input_stream.grabFrame(img)

        biggestShape = classifyShapeFromImage(inputImg, self.maxDetect)

        if biggestShape.getShape == ShapeEnum.CIRCLE:
            self.notes.append(biggestShape)
        else:
            self.otherShapes.append(biggestShape)
    
    def validNote(self):
        if self.notes.count > 0:
            return True
        return False
    
    def getNoteContour(self, index):
        return self.notes[index].getContour()

    def getNoteCenter(self, index):
        return self.notes[index].getCenter()
    
    def getNoteBoundingBox(self, index):
        return self.notes[index].getBoundingBox()