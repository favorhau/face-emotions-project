# -*- coding: utf-8 -*-
from model.cnn.net import FaceCNN as FaceCNN
from model.cnn import CNNModel
from api import app
import cv2



if __name__ == '__main__':
    # im = cv2.imread('template.png', 1)
    # 初始化模型
    # cnnModel = CNNModel()
    app.run('0.0.0.0', port=80)
    # print(cnnModel.predict(im))

# FaceCNN()