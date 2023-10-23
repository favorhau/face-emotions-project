from PIL import Image
from flask import Flask, Response
import os


app = Flask(__name__)


@app.route('/')
def index():
    return Response('Tensor Flow object detection')


@app.route('/test')
def test():

    PATH_TO_TEST_IMAGES_DIR = 'object_detection/test_images'  # cwh
    TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3)]

    image = Image.open(TEST_IMAGE_PATHS[0])
    # objects = object_detection_api.get_objects(image)

    return ''