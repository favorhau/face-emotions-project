import cv2
import torch
import numpy as np
import os


dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
img = cv2.imread('./couple.jpg')

detection_model_path = dirname + '/model/package/haarcascade_frontalface_default.xml'

face_detection = cv2.CascadeClassifier(detection_model_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

for i in range(100):
    faces = face_detection.detectMultiScale(gray,1.3,5)
    print(faces)