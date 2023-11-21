# -*- coding: utf-8 -*-
# -*- 总线程 main.py -*-
import argparse

# -*- 开发版执行程序 -*-
# Thread-1 Database Thread [数据库线程]
import db
# Thread-2 HTTP Thread [HTTP线程] 
# Thread-3 I/O Camera Thread [摄像头 I/O线程]
# Thread-4 Scheduler trigger Thread [中心定时调度器线程]
from scheduler import SchedulerThread
# Thread-5 Model Calculator Thread [算法模型计算线程]
from model.cnn import CNNModel


# -*- 中心服务器执行程序 -*-
from config import CenterServerConfig, ClientConfig

parser = argparse.ArgumentParser(
                    prog='Atom Go',
                    description='Emotion Test')


if __name__ == '__main__':

    parser.add_argument('-c', '--client', help='运行在客户端', action='store_true')      # option that takes a value
    parser.add_argument('-t', '--test', help='在本机上测试', action='store_true')      # option that takes a value
    parser.add_argument('-s', '--server', help='运行在服务端', action='store_true')      # option that takes a value
    
    args = parser.parse_args()

    if args.client:
        # 客户端 数据采集侧 运行
        from api import app, threadCam
        cnnModel = CNNModel()
        schedulerThread = SchedulerThread(camera=threadCam, emotionModel=cnnModel)
        schedulerThread.start()
        app.run('0.0.0.0', port=ClientConfig.port, threaded=True)
        
    else:
        # 服务端 数据处理侧 运行
        
        from center import app as cApp
        # 初始化数据库 若不存在数据库则自动新建
        db.empty()
        db.init()
       
        cApp.run('0.0.0.0', port=CenterServerConfig.port, threaded=True)
