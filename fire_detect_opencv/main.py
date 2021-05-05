import cv2 as cv
#import numpy as np
import datetime
import sys, os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from uuid import uuid4
#import schedule

PROJECT_ID = "cap-aacc4"
cred = credentials.Certificate("/home/pi/2021_cap/fire_detect_opencv/cert_key/cap-aacc4-firebase-adminsdk-qc42b-169c65d5e2.json")
default_app = firebase_admin.initialize_app(cred,{'storageBucket':f"{PROJECT_ID}.appspot.com"})
#버킷은 바이너리 객체의 상위 컨테이너. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너.
bucket = storage.bucket()#기본 버킷 사용
fireStatus = False
fireCascade = cv.CascadeClassifier('/home/pi/2021_cap/fire_detect_opencv/fire.xml')
#카메라 정보 받아오기 pi카메라는 -1
capture = cv.VideoCapture(-1)
#비디오 코덱설정
fourcc = cv.VideoWriter_fourcc(*'XVID')
picture_directory="/home/pi/2021_cap/fire_detect_opencv/detect_history/pictures/"
video_directory="/home/pi/2021_cap/fire_detect_opencv/detect_history/videos/"
start_time=datetime.datetime.now()
capture_time=start_time-datetime.timedelta(seconds=1)

def observe():
    print('불꽃 감시 중..')
    global fireStatus
    #키 입력이 없을 시 33ms마다 프레임 받아와서 출력
    while cv.waitKey(33) < 0:
        ret, frame = capture.read()
        fire=fireCascade.detectMultiScale(frame,1.2,5)
        cv.imshow("LiveCam", frame)
        for(x,y,w,h) in fire:
            print('불꽃 감지!!')
            #탐지한 불꽃에 사각형으로 표시
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv.imshow("ObserveFrame", frame)
            fireStatus=True
            now = datetime.datetime.now()
            if capture_time+datetime.timedelta(seconds=1) <= now:
                capture_time=savePhoto(now)
                firename=capture_time+'.jpg'
                uploadPhoto(filename)
            break
        if fireStatus==True:
            break

def savePhoto(now):
    cv.imshow('Fire',frame)
    cv.imwrite(picture_directory+str(now.strftime('%Y-%m-%d %H:%M:%S'))+".jpg",frame)
    print('사진 저장 완료 : '+str(now))
    return now

def saveVideo(filename):
    print('불꽃 감지!! / 녹화 시작')
    global fireStatus
    start_time = datetime.datetime.now()
    while(capture.isOpened()):
        now = datetime.datetime.now()
        ret, frame=capture.read()
        cv.imshow('RecordFrame',frame)
        out.write(frame)
        if start_time + datetime.timedelta(seconds=5) <= now:
            fireStatus=False
            print("영상 저장 완료 / 영상 업로드 시작")
            uploadVideo(filename)
            break
        
def uploadPhoto(file):
    blob = bucket.blob('detect_history/pictures/'+file)
    #new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요하다.
    blob.metadata = metadata

    #upload file
    blob.upload_from_filename(filename='/home/pi/2021_cap/fire_detect_opencv/detect_history/pictures'+file)
    #debugging hello
    print("사진 업로드 완료")
    print(blob.public_url)

def uploadVideo(file):
    blob = bucket.blob('detect_history/videos'+file)
    #new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token} #access token이 필요하다.
    blob.metadata = metadata

    #upload file
    blob.upload_from_filename(filename='/home/pi/2021_cap/fire_detect_opencv/detect_history/videos'+file)
    #debugging hello
    print("영상 업로드 완료")
    print(blob.public_url)
        
while True:
    #print(fireStatus)
    if fireStatus==False:
        observe()
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        out = cv.VideoWriter(video_directory+str(now)+'.avi',fourcc,20.0,(640,480))
        saveVideo(str(now)+'.avi')


capture.release()
out.release()
cv.destroyAllWindows()



