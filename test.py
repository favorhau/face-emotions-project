from flask import Flask, render_template, Response
import threading
import cv2
import numpy as np  

class MyCamera():
    def __init__(self) -> None:
        # 获取当前
        self.video = cv2.VideoCapture(self._gstreamer_pipeline())
        # self.video = cv2.VideoCapture(0)
        
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
            "nvvidconv ! flip-method=%d ! "
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
    def __init__(self):
        super(ThreadCam, self).__init__()
        
        self.frame = np.zeros((500, 500, 3), dtype=np.uint8)
        self.camera = MyCamera()

    def run(self):
        while True:
            success, image  = self.camera.video.read()
            _, jpeg = cv2.imencode('.jpg', image)
            self.frame = jpeg.tobytes()
        
    def gen(self):
        while True:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n\r\n')
                    
    def get_frame(self):
        return self.frame
        
                    
app = Flask(__name__, static_folder='./static')
               
@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(thread.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/frame', methods=['GET'])  # 这个地址返回视频流响应
def frame():
    return Response(thread.get_frame()
                    ,mimetype='image/jpg')

if __name__ == '__main__':
    thread = ThreadCam()
    thread.start()
    app.run(host='0.0.0.0', port=8080)