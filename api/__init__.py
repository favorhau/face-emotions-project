# -*- coding: utf-8 -*-
import json
from flask import Flask, Response, jsonify, render_template, request
from model.cnn.net import FaceCNN as FaceCNN
from skimage import io
from camera import ThreadCam


app = Flask(__name__)

threadCam = ThreadCam()
threadCam.start()

# cnnModel = CNNModel()
# faceLandMarks = FaceLandMarks()
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log', methods=['GET'])
def log():
    with open('./log/log', 'r') as f:
        data = f.read().replace('\n', '<br>')

    return data
    

@app.route('/config', methods=['POST'])
def config():
    payload = request.get_json()
    if (payload['method'] == 'edit'):
        token = payload['token']
        url = payload['url']
        port = payload['port']
        if(token and url and port):
            with open('./config/server.config', 'w') as f:
                f.write(json.dumps({
                    "client": {
                        "token": token
                    },
                    "centerServer": {
                        "url": url,
                        "port": port
                    }
                }))
            f.close()
            return jsonify({
                'status': 'success',
            })
        else:
            return jsonify({
                'status': 'error',
            })
    else:
        with open('./config/server.config', 'r') as f:
            f_s = json.loads(f.read())
        f.close()
        return f_s


@app.route('/api/test', methods=['POST'])
def test():
    # 取后面需要编码的字符
    # data = eval(request.data)['data'].split(',')[1]
    # imgdata = base64.b64decode(data)
    
    # img_np = np.frombuffer(thread.get_frame(), dtype=np.uint8)
    # img_np_cv2 = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # ret, face_window = cnnModel.predict(img_np_cv2)
    
    # faces = []
    # for (x, y, w, h) in face_window:
    #     face = img_np_cv2[y:y+h, x:x+w]
    #      # 色彩空间变换
    #     b, g, r = cv2.split(face)
    #     face_rgb = cv2.merge([r, g, b])
    #     faces.append(face_rgb)
        
    # faces_ids = faceLandMarks.predict(faces)

    data =  {
        # "data": ret,
        # "face_data": face_window,
        # "faces_ids": faces_ids,
    }
    
    return jsonify(data)

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(threadCam.gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
@app.route('/frame', methods=['GET'])  # 这个地址返回视频流响应
def frame():
    return Response(threadCam.get_frame()
                    ,mimetype='image/jpg')