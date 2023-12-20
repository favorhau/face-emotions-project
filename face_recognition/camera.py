# -*- coding: utf-8 -*-
import threading
from time import sleep
import cv2
import os
import numpy as np

from threading import Thread, Lock
from datetime import datetime
import copy  

import time


class Camera():
    def __init__(self) -> None:
        # 获取当前摄像头
        env = os.environ.get('ENV', 'linux')
        if(env == 'linux'):
            self.video = cv2.VideoCapture(self._gstreamer_pipeline()).release()
            self.video = cv2.VideoCapture(self._gstreamer_pipeline())
        elif (env == 'mac'):
            self.video = cv2.VideoCapture(0)
        
    def __del__(self):
        self.video.release()
    
    def _gstreamer_pipeline(
        self, 
        capture_width=1280, #摄像头预捕获的图像宽度
        capture_height=720, #摄像头预捕获的图像高度
        display_width=1280, #窗口显示的图像宽度
        display_height=720, #窗口显示的图像高度
        framerate=5,       #捕获帧率
        flip_method=0,      #是否旋转图像
    ):  

        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )
    

            
class ThreadCam(threading.Thread):
    # 多线程读取摄像头
    # 使用其他线程读取 不占用主线程
    def __init__(self):
        super(ThreadCam, self).__init__()
        
        # self.frame = np.zeros((512, 512, 3), dtype=np.uint8)
        self.camera = Camera()
        _, self.frame = self.camera.video.read()
        self.read_lock = Lock()

    def read(self):
        self.read_lock.acquire()
        frame = copy.deepcopy(self.frame)
        p = 0
        self.read_lock.release()
        return frame

    def run(self):
        while True:
            res, self.frame  = self.camera.video.read()
            if(res) == None:
                self.video.release()
                break
            # __, jpeg = cv2.imencode('.jpg', image)
            # self.frame = jpeg.tobytes()
            # print("2----------------------")
            if p < 10:
                p = p + 1
            sleep(self.p*0.1)

            # 如果按下 "q" 键，退出循环
            key = cv2.waitKey(100) & 0xFF
            if key == ord('q'):
                self.video.release()
                break

        
    # def gen(self):
    #     while True:
    #         sleep(0.05)
    #         yield (b'--frame\r\n'
    #                 b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n\r\n')
                    
    # def get_frame(self):
    #     return copy.deepcopy(self.frame)
    
    
class CameraThread(Thread):
    def __init__(self):
        self.time_cycle = 80
        # self.kill_event = kill_event
        
        self.stream = cv2.VideoCapture(self._gstreamer_pipeline())
        # self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        (self.grabbed, self.frame) = self.stream.read()
        self.read_lock = Lock()

        Thread.__init__(self)

    def update(self):
        (grabbed, frame) = self.stream.read()
        self.read_lock.acquire()
        self.grabbed, self.frame = grabbed, frame
        self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = copy.deepcopy(self.frame)
        self.read_lock.release()
        return frame

    def run(self):
        while self.stream.video.isOpened():
            start_time = datetime.now()

            self.update()

            finish_time = datetime.now()
            dt = finish_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            if ms < self.time_cycle:
                time.sleep((self.time_cycle - ms) / 1000.0)

    def _gstreamer_pipeline(
        self, 
        capture_width=1280, #摄像头预捕获的图像宽度
        capture_height=720, #摄像头预捕获的图像高度
        display_width=1280, #窗口显示的图像宽度
        display_height=720, #窗口显示的图像高度
        framerate=30,       #捕获帧率
        flip_method=0,      #是否旋转图像
    ):  

        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )

