# -*- coding: utf-8 -*-
from flask import Flask, Response, request, jsonify
from model.cnn.net import FaceCNN as FaceCNN
from model.cnn import CNNModel
from camera import thread
import base64
import numpy as np
import cv2

app = Flask(__name__)

cnnModel = CNNModel()

@app.route('/')
def index():
    return Response('Tensor Flow object detection')


@app.route('/api/test', methods=['POST'])
def test():
    # 取后面需要编码的字符
    data = eval(request.data)['data'].split(',')[1]
    imgdata = base64.b64decode(data)
    
    img_np = np.frombuffer(imgdata, dtype=np.uint8)
    img_np_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    ret, face_window = cnnModel.predict(img_np_cv2)

    data =  {
        "data": ret,
        "face_data": face_window,
    }
    
    return jsonify(data)

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(thread.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/frame', methods=['GET'])  # 这个地址返回视频流响应
def frame():
    return Response(thread.get_frame()
                    ,mimetype='image/jpg')