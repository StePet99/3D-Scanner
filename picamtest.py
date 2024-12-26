#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 21:11:11 2024

@author: stefanopetraccini
"""

from picamera2 import Picamera2, Preview 
import time

picam2 = Picamera2() 
camera_config = picam2.create_preview_configuration() 
picam2.configure(camera_config) 
picam2.start_preview(Preview.DRM)
picam2.start() 
time.sleep(2) 
picam2.capture_file("test.jpg")