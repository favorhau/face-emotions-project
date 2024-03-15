# -*- coding: utf-8 -*-
import sys
import threading
from time import sleep
from datetime import datetime
import cv2
import numpy as np  
from log import log
import json

class Camera():
    def __init__(self) -> None:
        # 获取当前摄像头
        if(sys.platform.startswith('linux')):
            self.video = cv2.VideoCapture(self._gstreamer_pipeline())
        else:
            self.video = cv2.VideoCapture(0)
        
    def __del__(self):
        self.video.release()
    
    def _gstreamer_pipeline(
        self, 
        capture_width=1280, #摄像头预捕获的图像宽度
        capture_height=720, #摄像头预捕获的图像高度
        display_width=1280, #窗口显示的图像宽度
        display_height=720, #窗口显示的图像高度
        framerate=60,       #捕获帧率
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
        
        self.frame = np.zeros((500, 500, 3), dtype=np.uint8)
        self.camera = Camera()
        self.readTimeInterval = 0
        self.currentEmotions = None
        self.currentFaceWindows = None

    def _read_current(self):
        if(datetime.now().timestamp() - self.readTimeInterval > 1):
            try:
                with open('./config/current.config', 'r') as f:
                    data = json.loads(f.read())
                    self.currentEmotions = data['emotions']
                    self.currentFaceWindows = data['face_windows']
                self.readTimeInterval = datetime.now().timestamp() 
                return data['emotions'], data['face_windows']
            except Exception as e:
                log('读入实时情绪失败', str(e))
        else:
            if(self.currentEmotions and self.currentFaceWindows):
                return self.currentEmotions, self.currentFaceWindows
        
        return [], []

    def run(self):
        while True:
            _, image  = self.camera.video.read()
            emotions, face_windows = self._read_current()
            # print(emotions, face_windows)
            for (x, y, w, h), e in zip(face_windows, emotions):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.rectangle(image, (x, y), (x+w, y+h), (0,0,255), 2)
                cv2.putText(image, e, (x, y), font, 1.2, (255, 255, 255), 2)

            __, jpeg = cv2.imencode('.jpg', image)
            self.frame = jpeg.tobytes()
        
    def gen(self):
        while True:
            sleep(0.03)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n\r\n')
                    
    def get_frame(self):
        return self.frame