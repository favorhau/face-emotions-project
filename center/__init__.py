# -*- coding: utf-8 -*-
# -*- 中心服务器 负责验证身份和处理数据 -*-
from datetime import datetime, time
from flask import Flask, request
from .utils import cal_report
from db.data import insert_data
from db.user import get_users
from log import log
from model.face_landmarks import FaceLandMarks
import math
import base64
import numpy as np

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
    
    log('', '当前', [_[1] for _ in users])
    
    if(not users): return
    
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
            report = cal_report(user_id=user_id, day=day)
            
            # del_data()
            # 6. 删除对应的原始数据条目


    return ''
