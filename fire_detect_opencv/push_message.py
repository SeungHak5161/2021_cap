# -*- encoding: utf-8 -*-
import datetime
from pyfcm import FCMNotification

APIKEY="AAAAalMeKts:APA91bEiB12GcGeo5W0MmzOjjmcDiR9LwrVgUxmspbWpI4eZz0LjuFIuTVxnfCbqd_IoeMjVkqJt5BGe9V77gvzFLmfSj5utQtj_0C0B0Y3LYM9nFytYpgDA_RV4HouwU-Qp7t8RwWMd"
TOKEN="dfjVL2OCTOOZDLE0VSBV1Q:APA91bEaotIIYMcGb3SYu8_UZn9z3MLg9oQ8eOE6OINuBP6EyT7SXq9WbFGH5GRKLIRbR-cyAV_qV2c1vLRT_i_QI7IzxgUFFkBxxl--PjpimTxc0DJTV-y7APm59nDCGpghWzTaVO3C"

# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(api_key=APIKEY)


def sendMessage(now):  # 메시지 (data 타입)
    data_message = {
        "title": now,
        "body": "불꽃이 감지되었습니다!"
    }
    push_service.single_device_data_message(registration_id=TOKEN, data_message=data_message)
    #sendMessage(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


