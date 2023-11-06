from flask import Flask, render_template, Response
import threading
import cv2
from copy import deepcopy
import numpy as np  

thread_lock = threading.Lock()
thread_exit = False

class ThreadCam(threading.Thread):
    def __init__(self):
        super(ThreadCam, self).__init__()
        self.frame = np.zeros((500, 500, 3), dtype=np.uint8)
        self.cap = cv2.VideoCapture(self._gstreamer_pipeline())


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
        global thread_exit
        
        while not thread_exit:
            ret, frame = self.cap.read()
            if ret:
                ret, jpeg = cv2.imencode('.jpg', frame)
                thread_lock.acquire()
                self.frame = jpeg.tobytes()
                thread_lock.release()
            else:
                thread_exit = True
                
        self.cap.release()
        
app = Flask(__name__, static_folder='./static')

        
def gen():
    global thread_exit
    while not thread_exit:
        thread_lock.acquire()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + thread.get_frame() + b'\r\n\r\n')
        thread_lock.release()
               
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
    
