#-*- encoding: utf-8 -*-
from time import sleep
import pigpio

import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import cv2 as cv
from uuid import uuid4
from pyfcm import FCMNotification
from flask import Flask
from time import sleep
import threading
import serial
import pyrebase

fireCascade = cv.CascadeClassifier('/home/pi/2021_cap/fire_detect_opencv/fire.xml')
capture = cv.VideoCapture(-1)

capture.release()
    #out.release()
cv.destroyAllWindows()