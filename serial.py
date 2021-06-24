# 시리얼, 시간 객체 가져오기
import serial, time
from msg import sendTextMessage
import threading
#USB 0번 포트를 9600bps 속도로 ser 객체 선언, 만약 에러가 난다면 USB0을 USB1로 변경 요망
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#0.1초 대기
time.sleep(0.1)
def data_commute():
    print("dsd")
    try:
        time.sleep(0.1)
        fire = 0;
        while 1:
        # serial 포트로 들어온 데이터를 \n까지 읽은 뒤 string형으로 캐스팅
            response = str(ser.read_until())
        # 문자열로 전송되는 데이터에서 원하는 값만 추출, 문자열 슬라이싱
            pos_start = response.find('a')
            if pos_start != -1:
                pos_end = response.find('r')
                fire = response[pos_start+1:pos_end-1]
                print("D")
                #추가한 부분. 불꽃검출됐을 때 트윌리오 메시지 전송
                if fire==1:
                    msg.sendTextMessage()
                    print(fire)
                time.sleep(1)

    #예외처리
    except KeyboardInterrupt:
        ser.close()