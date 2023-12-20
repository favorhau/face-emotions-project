from flask import Flask, Response
from CSIcamera import CSI_Camera, gstreamer_pipeline


app = Flask(__name__) # 实例app

camera = CSI_Camera()
camera.open(
    gstreamer_pipeline(
        sensor_id=0,
        capture_width=1920,
        capture_height=1080,
        flip_method=0,
        display_width=960,
        display_height=540,
        framerate=10,
    )
)
camera.start()

@app.route("/") # 路由
def hello_world():
    return 'hello world' # 返回值

@app.route("/video_feed") 
def video_feed():
    return Response(camera.gen(), mimetype='image/jpg')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug = True)
    # 开启 debug 模式
    # app.run(host='127.0.0.1', port=8080)
    # if camera.video_capture.isOpened():
    #     # try:
    #     while True:
    #         res, img  = camera.read()

