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
servoX=pigpio.pi()
servoY=pigpio.pi()
x=15
y=18

print("main start")

ser=serial.Serial("/dev/ttyUSB0",9600)
APIKEY="AAAAalMeKts:APA91bEiB12GcGeo5W0MmzOjjmcDiR9LwrVgUxmspbWpI4eZz0LjuFIuTVxnfCbqd_IoeMjVkqJt5BGe9V77gvzFLmfSj5utQtj_0C0B0Y3LYM9nFytYpgDA_RV4HouwU-Qp7t8RwWMd"
TOKEN="dfjVL2OCTOOZDLE0VSBV1Q:APA91bEaotIIYMcGb3SYu8_UZn9z3MLg9oQ8eOE6OINuBP6EyT7SXq9WbFGH5GRKLIRbR-cyAV_qV2c1vLRT_i_QI7IzxgUFFkBxxl--PjpimTxc0DJTV-y7APm59nDCGpghWzTaVO3C"
config={
	"apiKey":"kk4ks2sHVBKCA5TExxZPjEiqlNmJOdUywZN4At5g",
	"authDomain": "project-8965d.firebaseapp.com",
	"databaseURL": "https://project-8965d-default-rtdb.firebaseio.com",
	"storageBucket": "gs://project-8965d.appspot.com"
}
firebase=pyrebase.initialize_app(config)
db=firebase.database()
push_service = FCMNotification(api_key=APIKEY)
PROJECT_ID = "project-8965d"
cred = credentials.Certificate(
    "/home/pi/2021_cap/fire_detect_opencv/cert_key/cap-aacc4-firebase-adminsdk-qc42b-169c65d5e2.json")
default_app = firebase_admin.initialize_app(cred, {'storageBucket': f"{PROJECT_ID}.appspot.com"})
# 버킷은 바이너리 객체의 상위 컨테이너. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너.
bucket = storage.bucket()  # 기본 버킷 사용

print("firebase setup end")

fireStatus = False
fireCascade = cv.CascadeClassifier('/home/pi/2021_cap/fire_detect_opencv/fire.xml')
capture = cv.VideoCapture(-1)
# capture.set(cv.CAP_PROP_FRAME_WIDTH, 680)
# capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
picture_directory = "/home/pi/2021_cap/fire_detect_opencv/detect_history/pictures/"

print("camera setup end")

capture_time = datetime.datetime.now()
   
def observe():
    print('불꽃 감시 중..')
    global fireStatus, capture_time
    # 키 입력이 없을 시 33ms마다 프레임 받아와서 출력
    while cv.waitKey(33) < 0:
        ret, frame = capture.read()
        print(type(frame))
        print("after capture")
        
        fire = fireCascade.detectMultiScale(frame, 1.2, 5)
        cv.imshow("LiveCam", frame)
        
        print("after imshow")
        
        for (x, y, w, h) in fire:
            now = datetime.datetime.now()
            str_now=str(now.strftime('%Y-%m-%d %H:%M:%S'))
            print('불꽃 감지!! (' + str_now + ')')
            # 탐지한 불꽃에 사각형으로 표시
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            capture_time = savePhoto(now, frame)
            filename = str(capture_time.strftime('%Y-%m-%d %H:%M:%S')) + '.jpg'
            uploadPhoto(filename)
            fireStatus=True
            break

def move_up():
    valY=servoY.get_servo_pulsewidth(y)
    if valY+300<=2400:
        valY+=300
        servoY.set_servo_pulsewidth(y,valY)

def move_down():
    valY=servoY.get_servo_pulsewidth(y)
    if valY-300>=600:
        valY-=300
        servoY.set_servo_pulsewidth(y,valY)
    
def move_left():
    valX=servoX.get_servo_pulsewidth(x)
    if valX+300<=2400:
        valX+=300
        servoX.set_servo_pulsewidth(x,valX)
    
def move_right():
    valX=servoX.get_servo_pulsewidth(x)
    if valX-300>=600:
        valX-=300
        servoX.set_servo_pulsewidth(x,valX)
    
def servoReset():
    servoX.set_servo_pulsewidth(x,1500)
    servoY.set_servo_pulsewidth(y,1500)
 
def sendMessage(now):
    data_message={
        "title":now,
        "body": "실내에 화재가 감지되었습니다."
        }
    push_service.single_device_data_message(registration_id=TOKEN, data_message=data_message)
def savePhoto(now, frame):
    cv.imwrite(picture_directory + str(now.strftime('%Y-%m-%d %H:%M:%S')) + ".jpg", frame)
    print('사진 저장 완료 (' + str(now.strftime('%Y-%m-%d %H:%M:%S')) + ".jpg)")
    return now

def trans_data():
    while True:
        val=ser.readline().strip()
        val=val.decode()
        a=list(val.split())
        Co2_gas=int(a[0])
        print(Co2_gas,"ppm")
        db.child("data_a").child("1-set").set(Co2_gas)
        db.child("data_a").child("2-push").push(Co2_gas)
        
        now = datetime.datetime.now()
        str_now=str(now.strftime('%Y-%m-%d %H:%M:%S'))
        data_message={
            "title":str_now,
            "body": "현재 CO2수치:"+str(Co2_gas)+"ppm"
            }
        push_service.single_device_data_message(registration_id=TOKEN, data_message=data_message)

#data trans fer from arduino-> rpi
print("serial start")
thread_serial_data=threading.Thread(target=trans_data,args=())
thread_serial_data.start()
print("serial end")

def fire_detect():
    global fireStatus
    while True:
        if fireStatus==False:
            observe()
        else:
            time.sleep(10) #no effect -> background thread is running..
            fireStatus=False



while True:
    observe()