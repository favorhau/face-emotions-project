# -*- coding: utf-8 -*-
# 调度中心 每 1s 执行一次 多线程写入原始数据 -*-
import base64
from config import CenterServerConfig
from log import log
from model.cnn import CNNModel
from camera import ThreadCam
import requests
import cv2
import numpy as np
import threading
import schedule
import time as t


class SchedulerThread(threading.Thread):
    """
    # 调度器
    * 只负责定期监听摄像头，走一次情绪识别，并把对应身份的信息传递给中心服务器
    * 由中心服务器进行身份识别
    """
    def __init__(self, camera: ThreadCam, emotionModel: CNNModel) -> None:
        super(SchedulerThread, self).__init__()
        # 摄像头调度线程
        self.camera = camera
        self.emotionModel = emotionModel
        self.session = requests.session()

    def exec(self):
        img_np = np.frombuffer(self.camera.get_frame(), dtype=np.uint8)
        img_np_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        ret, face_window = self.emotionModel.predict(img_np_cv2)
        
        faces = []
        
        for (x, y, w, h) in face_window:
            face = img_np_cv2[y:y+h, x:x+w]
            # 色彩空间变换
            b, g, r = cv2.split(face)
            face_rgb = cv2.merge([r, g, b])
            
            encoded_data = base64.b64encode(face_rgb.tobytes()).decode('utf-8')
            faces.append(encoded_data)
            
        try:
            self.session.post(
                '{}:{}{}'.format(CenterServerConfig.url, CenterServerConfig.port, CenterServerConfig.face_reg),
                json={
                    'emotions': ret,
                    'faces': faces,
                },
                timeout=3000
            )
            
        except Exception as e:
            log(str(e), '数据同步异常')
            return
            

        
    def run(self):
        schedule.every(1).seconds.do(self.exec)
        while True:
            # 运行待执行的任务
            schedule.run_pending()
            t.sleep(1)