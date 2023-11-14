import cv2
import torch
import numpy as np
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class CNNModel():
    def __init__(self) -> None:
        #opencv自带的一个面部识别分类器
        detection_model_path = dirname + '/package/haarcascade_frontalface_default.xml'

        classification_model_path = dirname + '/package/model_cnn.pkl'

        # 加载人脸检测模型
        self.face_detection = cv2.CascadeClassifier(detection_model_path)

        # 加载表情识别模型
        self.emotion_classifier = torch.load(classification_model_path)


    # 人脸数据归一化,将像素值从0-255映射到0-1之间
    def _preprocess_input(self, images):
        """ preprocess input by substracting the train mean
        # Arguments: images or image of any shape
        # Returns: images or image with substracted train mean (129)
        """
        images = images/255.0
        return images

    def detect_face(self, img):
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 转化成灰度
        faces = self.face_detection.detectMultiScale(gray,1.3,5)
        
        return faces
        

    def predict(self, img):

        #表情标签
        emotion_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}

        emotion_window = []
        face_window = []
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detect_face(img=img)
        # font = cv2.FONT_HERSHEY_SIMPLEX
        
        for (x, y, w, h) in faces:
            # 在脸周围画一个矩形框，(255,0,0)是颜色，2是线宽
            # cv2.rectangle(gray, (x,y),(x+w,y+h),(84,255,159),2)

            # 获取人脸图像
            face = gray[y:y+h,x:x+w]

            try:
                # shape变为(48,48)
                face = cv2.resize(face,(48,48))
            except:
                continue

            # 扩充维度，shape变为(1,48,48,1)
            #将（1，48，48，1）转换成为(1,1,48,48)
            face = np.expand_dims(face,0)
            face = np.expand_dims(face,0)

            # 人脸数据归一化，将像素值从0-255映射到0-1之间
            face = self._preprocess_input(face)
            new_face=torch.from_numpy(face)
            new_new_face = new_face.float().requires_grad_(False)
            
            # 调用我们训练好的表情识别模型，预测分类
            emotion_arg = np.argmax(self.emotion_classifier.forward(new_new_face).detach().numpy())
            emotion = emotion_labels[emotion_arg]

            emotion_window.append(emotion)
            face_window.append([ int(x) , int(y), int(w), int(h)])
            
            
        return emotion_window, face_window