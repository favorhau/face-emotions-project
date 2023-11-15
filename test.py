# -*- coding: utf-8 -*-
import time
from model.cnn.net import FaceCNN as FaceCNN
from model.cnn import CNNModel
from model.face_landmarks import FaceLandMarks
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import glob
import os

cnnModel = CNNModel()
faceLandMarks = FaceLandMarks()

def cv2AddChineseText(img, text, position, textSize=30, textColor=(0, 255, 0)):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
       '/System/Library/Fonts/PingFang.ttc', textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

start_time = time.time()

for filename in glob.glob('./test/*.jpg'):
    if 'process' not in filename:
        img = cv2.imread(filename)
        faces = cnnModel.detect_face(img)
        faces_rgb = []
        for (x, y, w, h) in faces:
            imgn = img[y:y+h,x:x+w]
            b, g, r = cv2.split(imgn)
            face_rgb = cv2.merge([r, g, b])
            faces_rgb.append(face_rgb) 
            font = '/System/Library/Fonts/PingFang.ttc'
        
        pd = faceLandMarks.predict(faces_rgb)
        for (x, y, w, h) in faces: cv2.rectangle(img, (x, y), (x+w, y+w), (0,0,255), 2)
        for (x, y, w, h), text in zip(faces, pd): 
            if text: img = cv2AddChineseText(img, text, (x, y), 20, (255, 255, 255))
        
        folder, name = os.path.split(filename)
        n, extenstion = os.path.splitext(name)
        cv2.imwrite(os.path.join(folder, '{}_process {}'.format(n, extenstion)), img)

        end_time = time.time()
        print("耗时: {:.2f}秒".format(end_time - start_time))