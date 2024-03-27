import torch
from torchvision import transforms
import cv2
import numpy as np
import os

from .ResNet import ResNet18
from model.detection.face_detect import MTCNN
from PIL import ImageDraw, ImageFont, Image


import time



class Predictor:
    def __init__(self, mtcnn_model_path, emotion_model_path, threshold=0.6):
        self.device = torch.device("cuda")
        os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

        mu, st = 0, 255
        self.test_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((40,40)),
            transforms.Grayscale(),
            transforms.ToTensor(),
            transforms.Normalize(mean=(mu,), std=(st,))
            # transforms.TenCrop(40),
            # transforms.Lambda(lambda crops: torch.stack(
            #     [transforms.ToTensor()(crop) for crop in crops])),
            # transforms.Lambda(lambda tensors: torch.stack(
            #     [transforms.Normalize(mean=(mu,), std=(st,))(t) for t in tensors])),
            ])

        self.threshold = threshold
        self.mtcnn = MTCNN(model_path=mtcnn_model_path)

        # self.emotion_model = MobileNetV3_Large(num_classes=7)
        # self.emotion_model = EmoNet(n_expression=8)
        # self.emotion_model.load_state_dict(torch.load(emotion_model_path, map_location='cpu'))
        self.emotion_model = ResNet18()
        checkpoint = torch.load(emotion_model_path)
        self.emotion_model.load_state_dict(checkpoint['model_state_dict'])


        self.emotion_model.to(self.device)
        self.emotion_model.eval()

        # self.emotion_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}
        self.emotion_labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
        # self.emotion_labels = {0: 'Neutral', 1: 'Happy', 2: 'Sad', 3: 'Surprise', 4: 'Fear', 5: 'Disgust', 6: 'Anger', 7: 'Contempt'}

    @staticmethod
    def process(imgs):
        imgs1 = []
        for img in imgs:
            img = img.transpose((2, 0, 1))
            img = (img - 127.5) / 127.5
            imgs1.append(img)
        return imgs1

    def recognition(self, img):
        # img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        s = time.time()
        imgs, boxes = self.mtcnn.infer_image(img)
        print('人脸检测时间：%dms' % int((time.time() - s) * 1000))
        if imgs is None or boxes is None:
            return [], []
        s = time.time()
        images = self.process(imgs)
        images = np.array(images, dtype='float32')
        
        s = time.time()
        emotions = []
        # for box in boxes:
        for face in imgs:
            # x,y,w,h,n = box
            # face = img[int(y):int(h), int(x):int(w)]
            try:
                gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            except:
                # print(box)
                print(face)
            gray = self.test_transform(gray)
            gray = gray.to(self.device)
            gray = torch.unsqueeze(gray, dim=0)
            # print(gray.shape)
            out = self.emotion_model(gray)
            # print(out)
            # max_index = torch.argmax(out['expression'])
            max_index = torch.argmax(out)
            # print(max_index)
            out = max_index.detach().cpu().numpy()
            # print(out)
            emotion = self.emotion_labels[int(out)]
            # print(emotion)
            emotions.append(emotion)

        print('表情识别时间：%dms' % int((time.time() - s) * 1000))
        new_boxes = []
        for i in range(boxes.shape[0]):
            bbox = boxes[i, :4]
            corpbbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
            new_boxes.append(corpbbox)
        
        return new_boxes, emotions

    def add_text(self, img, text, left, top, color=(0, 0, 0), size=20):
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('DejaVuSerif.ttf', size)
        draw.text((left, top), text, color, font)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 画出人脸框和关键点
    def draw_face(self, img, boxes_c, names, emotions):
        # img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        if boxes_c is not None:
            for i in range(boxes_c.shape[0]):
                bbox = boxes_c[i, :4]
                name = names[i]
                emotion = emotions[i]
                corpbbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
                # 画人脸框
                cv2.rectangle(img, (corpbbox[0], corpbbox[1]),
                              (corpbbox[2], corpbbox[3]), (0, 255, 255), 1)
                # 判别为人脸的名字
                img = self.add_text(img, name, corpbbox[0], corpbbox[1] -15, color=(3, 255, 255), size=15)
                img = self.add_text(img, emotion, corpbbox[0], corpbbox[1] -30, color=(3, 255, 255), size=15)
                print(name)
                print(emotion)
            # 在文件系统中保存图像  
            # cv2.imwrite('test.jpg', img)
        return img
        # cv2.imshow("result", img)
        # cv2.waitKey(1)
