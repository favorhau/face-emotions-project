from flask import Flask, render_template, Response
import threading
import cv2
from copy import deepcopy
import numpy as np  

global gF

class ThreadCam(threading.Thread):
    def __init__(self):
        super(ThreadCam, self).__init__()
        self.frame = np.zeros((500, 500, 3), dtype=np.uint8)

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
        
    def get_frame(self):
        return deepcopy(self.frame)

    def run(self):

        while True:
            ret, frame = cv2.VideoCapture(self._gstreamer_pipeline()).read()
            _, jpeg = cv2.imencode('.jpg', frame)
            self.frame = jpeg.tobytes()
        
app = Flask(__name__, static_folder='./static')

        
def gen():
    while True:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + thread.get_frame() + b'\r\n\r\n')
               
@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 

if __name__ == '__main__':
    thread = ThreadCam()
    thread.start()
    app.run(host='0.0.0.0', debug=True, port=8080)
    
