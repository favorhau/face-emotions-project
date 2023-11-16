# -*- coding: utf-8 -*-
# -*- 总线程 main.py -*-

# Thread-1 Database Thread [数据库线程]
import db
# Thread-2 HTTP Thread [HTTP线程] 
# Thread-3 I/O Camera Thread [摄像头 I/O线程]
from api import app, threadCam
# Thread-4 Scheduler trigger Thread [中心定时调度器线程]
from scheduler import SchedulerThread
# Thread-5 Model Calculator Thread [算法模型计算线程]
from model.cnn import CNNModel
from model.face_landmarks import FaceLandMarks


if __name__ == '__main__':
    # 初始化数据库 若不存在数据库则自动新建
    db.init()
    cnnModel = CNNModel()
    faceLandMarks = FaceLandMarks()
    schedulerThread = SchedulerThread(camera=threadCam, emotionModel=cnnModel, userRegModel=faceLandMarks)
    schedulerThread.start()
    # 开启 web 服务
    app.run('0.0.0.0', port=8080, threaded=True)