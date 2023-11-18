# -*- coding: utf-8 -*-
# -*- 总线程 main.py -*-

# -*- 开发版执行程序 -*-
# Thread-1 Database Thread [数据库线程]
import db
# Thread-2 HTTP Thread [HTTP线程] 
# Thread-3 I/O Camera Thread [摄像头 I/O线程]
from api import app, threadCam
# Thread-4 Scheduler trigger Thread [中心定时调度器线程]
from scheduler import SchedulerThread
# Thread-5 Model Calculator Thread [算法模型计算线程]
from model.cnn import CNNModel

# -*- 中心服务器执行程序 -*-
from config import CenterServerConfig, ClientConfig
from center import app as cApp


if __name__ == '__main__':
    # 初始化数据库 若不存在数据库则自动新建
    db.init()
    cnnModel = CNNModel()
    schedulerThread = SchedulerThread(camera=threadCam, emotionModel=cnnModel)
    schedulerThread.start()
    cApp.run('0.0.0.0', port=CenterServerConfig.port, threaded=True)
    # 开启 web 服务
    app.run('0.0.0.0', port=ClientConfig.port, threaded=True)