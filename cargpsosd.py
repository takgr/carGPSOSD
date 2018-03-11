#!/usr/bin/python

import picamera
import datetime as dt
from gps import *
from time import *
import threading
import time
import numpy as np
import string
import random
import os

from PIL import Image, ImageDraw, ImageFont

gpsd = None #seting the global variable

os.system('clear') #clear the terminal (optional)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer



# Video Resolution for recording
VIDEO_HEIGHT = 940
VIDEO_WIDTH = 1280

baseDir='/home/pi/osd/' # directory where the video will be recorded
filename='test.h264'
 
os.system('clear') # clear the terminal from any other text


with picamera.PiCamera() as camera:
   topText = "Alt: 310m       Spd: 45km/h         Dir: N"
   bottomText = "47.6062 N, 122.3321 W   Home: 322m    Rec: 3:22"
   camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
   camera.framerate = 30
   camera.led = False
   camera.start_preview()
   camera.annotate_background = picamera.Color('black')
   camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   camera.start_recording(filename)
   gpsp = GpsPoller() # create the thread
   gpsp.start() # start it up

   start = dt.datetime.now()
   try:
     while True:
       lat = " Lat: " + "%.5f" % gpsd.fix.latitude
       lon = " Lon: " + "%.5f" % gpsd.fix.longitude
       spd = " Spd: " + "%.2f" % (3.6*gpsd.fix.speed) + " Km/h"
       alt = " Alt: " + str(gpsd.fix.altitude) + " M"
#       sats = " Sats: " + str(gpsd.satellites)
       camera.annotate_text = gpsd.utc + " | " + lat + lon + spd + alt
       sleep(0.01)
   except KeyboardInterrupt:
      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing
      camera.stop_recording()
      camera.stop_preview()
      print "Cancelled"



   finally:
      #camera.stop_recording()
      camera.stop_preview()
      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing
