from model.cnn.net import FaceCNN
from model.cnn import predict
import cv2

if __name__ == '__main__':
    im = cv2.imread('template.png', 1)

    print(predict(im))

# FaceCNN()