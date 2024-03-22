import argparse
import functools

# from camera import CameraThread, ThreadCam, Camera
from utils.utils import add_arguments, print_arguments

from predictor import Predictor
import cv2
import numpy as np
from CSIcamera import CSI_Camera, gstreamer_pipeline


parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('image_path',               str,     './children7.jpg',                 '预测图片路径')
add_arg('face_db_path',             str,     'face_db',                          '人脸库路径')
add_arg('threshold',                float,   0.6,                                '判断相识度的阈值')
add_arg('mobilefacenet_model_path', str,     'save_model/mobilefacenet.pth',     'MobileFaceNet预测模型的路径')
add_arg('mtcnn_model_path',         str,     'save_model/mtcnn',                 'MTCNN预测模型的路径')
add_arg('emotion_model_path',         str,     'save_model/best_checkpoint.tar', 'emotion预测模型的路径')
args = parser.parse_args()
print_arguments(args)




if __name__ == '__main__':

    predictor = Predictor(args.mtcnn_model_path, args.mobilefacenet_model_path, args.emotion_model_path, args.face_db_path, threshold=args.threshold)
    img = cv2.imdecode(np.fromfile(args.image_path, dtype=np.uint8), -1)
    boxes, names, emotions = predictor.recognition(img)
    predictor(boxes, names, emotions)
    # img = predictor.draw_face(img, boxes, names, emotions)
    
    # camera = CSI_Camera()
    # camera.open(
    #     gstreamer_pipeline(
    #         sensor_id=0,
    #         capture_width=1920,
    #         capture_height=1080,
    #         flip_method=0,
    #         display_width=960,
    #         display_height=540,
    #     )
    # )
    # camera.start()
    # if camera.video_capture.isOpened():
    #     try:
    #         while True:
    #             res, img  = camera.read()
    #             if res == False:
    #                 print('img is None')
    #                 break
    #             # # kk = cv2.waitKey(1)
    #             # # do other things
    #             boxes, names, emotions = predictor.recognition(img)

    #             img = predictor.draw_face(img, boxes, names, emotions)
    #             cv2.imshow("face recognition",img)
    #             # This also acts as
    #             keyCode = cv2.waitKey(30) & 0xFF
    #             # Stop the program on the ESC key
    #             if keyCode == 27:
    #                 break
    #     finally:
    #         camera.stop()
    #         camera.release()
                
    #     cv2.destroyAllWindows()   

    #     # camera.video.release()
    # else:
        # print("Error: Unable to open both cameras")
        # camera.stop()
        # camera.release()