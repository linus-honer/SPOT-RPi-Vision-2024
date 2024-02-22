from time import time, sleep
import cv2
import logging

import cscore
from wpilib import SmartDashboard, SendableChooser
from cscore.imagewriter import ImageWriter
from networktables.util import ntproperty, ChooserControl
from networktables import NetworkTables

class VisionServer:
    '''Base class for the VisionServer'''

    # NetworkTable parameters

    # this will be under /SmartDashboard, but the SendableChooser code does not allow full paths
    ACTIVE_MODE_KEY = "vision/active_mode"

    # frame rate is pretty variable, so set this a fair bit higher than what you really want.
    # using a large number for no limit
    output_fps_limit = ntproperty('/SmartDashboard/vision/output_fps_limit', 60,
                                  doc='FPS limit of frames sent to MJPEG server')

    # default "compression" on output stream. This is actually quality, so low is high compression, poor picture
    default_compression = ntproperty('/SmartDashboard/vision/default_compression', 30,
                                     doc='Default compression of output stream')

    output_port = ntproperty('/SmartDashboard/vision/output_port', 1190,
                             doc='TCP port for main image output')

    # Resolution, FPS
    image_width = ntproperty('/SmartDashboard/vision/width', 424, writeDefault=False, doc='Image width')
    image_height = ntproperty('/SmartDashboard/vision/height', 240, writeDefault=False, doc='Image height')
    camera_fps = ntproperty('/SmartDashboard/vision/fps', 30, writeDefault=False, doc='FPS from camera')

    image_writer_state = ntproperty('/SmartDashboard/vision/write_images', False, writeDefault=True,
                                    doc='Turn on saving of images')

    # Targeting info sent to RoboRio
    # Send the results as one big array in order to guarantee that the results
    #  all arrive at the RoboRio at the same time.
    # Value is (time, success, finder_id, distance, angle1, angle2) as a flat array.
    # All values are floating point (required by NT).
    target_info = ntproperty('/SmartDashboard/vision/target_info', 6 * [0.0, ],
                             doc='Packed array of target info: time, success, finder_id, distance, angle1, angle2')

    