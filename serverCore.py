from time import time, sleep
import cv2
import logging

from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer
import numpy as np
from cscore.imagewriter import ImageWriter
from shapeClassificaton import *

class VisionServer:
    '''Base class for the VisionServer'''

def visionConsolePrint(message):
    print(message)

def processStream(input_stream):
    notes = []

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    inputImg = input_stream.grabFrame(img)

    biggestShape = classifyShapeFromImage(inputImg)

    if biggestShape.getShape == ShapeEnum.CIRCLE:
        notes.append(biggestShape)