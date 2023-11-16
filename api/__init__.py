# -*- coding: utf-8 -*-
from datetime import time
from flask import Flask, Response, jsonify
from db.user import get_users
from log import log
from model.cnn.net import FaceCNN as FaceCNN
from model.cnn import CNNModel
from model.face_landmarks import FaceLandMarks
from skimage import io
from camera import ThreadCam
import numpy as np
import cv2


app = Flask(__name__)

threadCam = ThreadCam()
threadCam.start()

# cnnModel = CNNModel()
# faceLandMarks = FaceLandMarks()
    
@app.route('/')
def index():
    return Response('Tensor Flow object detection')


@app.route('/api/test', methods=['POST'])
def test():
    # 取后面需要编码的字符
    # data = eval(request.data)['data'].split(',')[1]
    # imgdata = base64.b64decode(data)
    
    img_np = np.frombuffer(thread.get_frame(), dtype=np.uint8)
    img_np_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    ret, face_window = cnnModel.predict(img_np_cv2)
    
    faces = []
    for (x, y, w, h) in face_window:
        face = img_np_cv2[y:y+h, x:x+w]
         # 色彩空间变换
        b, g, r = cv2.split(face)
        face_rgb = cv2.merge([r, g, b])
        faces.append(face_rgb)
        
    faces_ids = faceLandMarks.predict(faces)

    data =  {
        "data": ret,
        "face_data": face_window,
        "faces_ids": faces_ids,
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