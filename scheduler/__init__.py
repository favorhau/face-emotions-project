# -*- coding: utf-8 -*-
# 调度中心 每 1s 执行一次 多线程写入原始数据 -*-
from camera import ThreadCam
from db.data import insert_data
from model.face_landmarks import FaceLandMarks
from datetime import time, datetime
from model.cnn import CNNModel
from log import log
from db.user import get_users
import cv2
import numpy as np
import threading
import schedule
import time as t


class SchedulerThread(threading.Thread):
    def __init__(self, camera: ThreadCam, emotionModel: CNNModel, userRegModel: FaceLandMarks) -> None:
        super(SchedulerThread, self).__init__()
        # 摄像头调度线程
        self.camera = camera
        self.emotionModel = emotionModel
        self.userRegModel = userRegModel


    def exec(self):
        # 1. 取得数据库当中对应时间点的用户的列表，决定要进行人脸检测
        hour = datetime.now().hour
        minute = datetime.now().minute
        second = datetime.now().second
        users = get_users((time(hour,minute,second), time(hour,minute,second)))
        # log('', '当前', [_[1] for _ in users])
        
        # 2. 取得对应的图片进行人脸检测，并指定检测的用户，返回结果
        img_np = np.frombuffer(self.camera.get_frame(), dtype=np.uint8)
        img_np_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        ret, face_window = self.emotionModel.predict(img_np_cv2)
        
        faces = []
        for (x, y, w, h) in face_window:
            face = img_np_cv2[y:y+h, x:x+w]
            # 色彩空间变换
            b, g, r = cv2.split(face)
            face_rgb = cv2.merge([r, g, b])
            faces.append(face_rgb)
            
        faces_ids = self.userRegModel.predict(faces)
        
        target_data = zip(faces_ids, ret)

        # 3. 录入原始数据
        for (id, emo) in target_data:
            if(id and id in [str(_[0]) for _  in users]):
                insert_data(user_id=id, emotion=emo)
        
        # 4. 判断当前的时间是否超过指定时间，如果超过，则计算报告
        
        

        # 5. 删除对应的原始数据条目
        
        
        
    def run(self):
        schedule.every(1).seconds.do(self.exec)
        while True:
            # 运行待执行的任务
            schedule.run_pending()
            t.sleep(1)