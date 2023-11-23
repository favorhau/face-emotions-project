# -*- coding: utf-8 -*-
# -*- 中心服务器 负责验证身份和处理数据 -*-
from datetime import datetime, time
from flask import Flask, request, jsonify, send_file, make_response, Response
from db.report import fetch_report
from .utils import dumps_report
from db.data import insert_data, del_data
from db.user import get_users
from log import log
from model.face_landmarks import FaceLandMarks
import math
import base64
import numpy as np
import json
import os

app = Flask(__name__)
faceLandMarks = FaceLandMarks()

# 接受人脸身份识别，进行识别
@app.route('/api/face_reg', methods=['POST'])
def face_reg():

    """
    到达的数据
    @params emotions: ['happy', ...]
    @params faces: [base64enode(bytes), ...]
    """
    
    data = request.get_json()
    
    # 1. 取得数据库当中对应时间点的用户的列表，决定要进行人脸检测，如果为空，则返回
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second
    users = get_users((time(hour,minute,second), time(hour,minute,second)))
    
    # log('', '当前', [_[1] for _ in users])
    
    if(not users): return ''
    
    # 2. 取得数据 并还原
    try:
        # 解码base64
        decoded_image = [
            np.frombuffer(base64.b64decode(_), dtype=np.uint8)
            for _ in data['faces']
        ]
        # 还原array状态
        reshape_image = [
            _.reshape((int(math.sqrt(_.shape[0]/3)), int(math.sqrt(_.shape[0]/3)), 3)) 
            for _ in decoded_image
        ]
    except Exception as e:
        log('error', 'center/__init__.py', 'decoded Error')
        
    # 3. 进行人脸身份识别
    try:
        res = faceLandMarks.predict(reshape_image)
    except Exception as e:
        log('error', 'center/__init__.py', 'predict Error')
        
    target_data = zip(res, data['emotions'])
    # 4. 录入原始数据
    for (id, emo) in target_data:
        if(id and id in [str(_[0]) for _  in users]):
            insert_data(user_id=id, emotion=emo)
   
    for user in users:
        # 5. 判断当前的时间是否为时间终点，如果是，则计算报告
        if(datetime.now().strftime('%H:%M:%S') == user[3]):
            # 计算报告
            # user[0] 是id
            user_id = str(user[0])
            day = datetime.now().strftime('%Y-%m-%d')
            dumps_report(user_id=user_id, day=day)
            
            # 6. 删除对应的原始数据条目
            del_data(user_id=user_id, day=day)
            log('', 'center.py/__init__.py', '录入', user[1], day, '报告成功')
            
            
    return ''

# 获取报告详情
@app.route('/api/get_report', methods=['POST'])
def get_report():
    data = request.get_json()

    
    user_id = data.get('user_id')
    id = data.get('id')
    name = data.get('name')
    
    if(id and not id.isdigit()) : id = None
    if(user_id and not user_id.isdigit()) : user_id = None
    
    result = fetch_report(user_id=user_id, id=id, name=name)
    
    ret = []
    try:
        for r in result:
            [_id, _user_id, _date, _type, _title, _data, _name] = r
            ret.append({
                "id": _id,
                "user_id": _user_id,
                "date": _date,
                "type": _type, 
                "title": _title,
                "data": json.loads(_data),
                "name": _name,
            })
            
    except Exception as e:
        log(str(e))
        
    return jsonify({
        "data": ret
    })
    

# 图片映射
@app.route('/api/img/<filename>')
def get_file(filename):
    # 假设文件都在 uploads 目录中
    
    try:
        current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_path,'model/package/train_images/{}.jpg'.format(filename))

        with open(file_path, 'rb') as file:
            image_data = file.read()

        file.close()
        # 设置响应头
        headers = {
            'Content-Type': 'image/jpeg',  # 根据实际情况设置正确的 Content-Type
            'Cache-Control': 'public, max-age=31536000',  # 一年的缓存
        }

        return Response(response=image_data, status=200, headers=headers)
    except Exception as e:
        return Response(response=f"Error: {str(e)}", status=500)