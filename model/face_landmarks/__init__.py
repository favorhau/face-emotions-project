# -*- coding: utf-8 -*-
import os, dlib, glob, numpy
from skimage import io
from log import log

dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class FaceLandMarks():
    # 人脸关键点检测器
    predictor_path = dirname + "/package/shape_predictor.dat"
    # 人脸识别模型、提取特征值
    face_rec_model_path =  dirname + "/package/dlib_face_recognition.dat"
    # 训练图像文件夹
    faces_folder_path = dirname + "/package/train_images"
    
    def __init__(self) -> None:
        # 加载模型
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)
        
        # 用户: 脸特征，写在内存当中
        self.faces_feat = {}
        self._train_init()
        
    def _train_init(self):
        for f in glob.glob(os.path.join(self.faces_folder_path,"*.jpg")):
            log("", "正在处理: {}".format(f))
            img = io.imread(f)
            username = f.split('/')[-1].split('.')[0]
            # 人脸检测
            dets = self.detector(img, 1)
            if(dets):
                shape = self.sp(img, dets[0])
                # 提取特征
                face_descriptor = self.facerec.compute_face_descriptor(img, shape)
                v = numpy.array(face_descriptor)
                self.faces_feat[username] = v

    def predict(self, imgs):
        """
        # 匹配人脸
        params imgs [, , ] 图片列表
        return 返回结果数组
        """
        res = []
        
        for img in imgs:
            dets = self.detector(img, 1)
            if not dets:
                res.append(None)
            else:
                
                try:
                    shape = self.sp(img, dets[0])
                    face_descriptor = self.facerec.compute_face_descriptor(img, shape)
                    d_test = numpy.array(face_descriptor)
                    r = []
                    # TODO: 此处可改造为矩阵运算，降低复杂度
                    for k, v in self.faces_feat.items():
                        dist_ = numpy.linalg.norm(v-d_test)
                        r.append(dist_)

                    # 训练集人物和距离组成一个字典
                    c_d = dict(zip(list(self.faces_feat.keys()), r))  
                    cd_sorted = sorted(c_d.items(), key=lambda d:d[1])
                    res.append(cd_sorted[0][0])
                except Exception as e:
                    log(str(e), 'error')
                    res.append(None)
        return res