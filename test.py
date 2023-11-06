from flask import Flask, render_template, Response
import cv2

class VideoCamera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        # dispW=1280
        # dispH=720
        # flip=0
        # camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
        self.video = cv2.VideoCapture(self._gstreamer_pipeline())
   
    def _gstreamer_pipeline(
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
 
    def __del__(self):
        self.video.release()
   
    def get_frame(self):
        success, image = self.video.read()
        # 在这里处理视频帧
        cv2.putText(image, "hello",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 0))
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

app = Flask(__name__, static_folder='./static')

@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)