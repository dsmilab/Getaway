from .config import *
from .utils.inference import detect_faces
from .utils.inference import apply_offsets
from .utils.inference import load_detection_model
from .utils.preprocessor import preprocess_input

import cv2
from keras.models import load_model
import numpy as np
import posixpath
import sys

__all__ = ['Activity']


class Activity(object):

    def __init__(self):
        detection_model_path = posixpath.join(MODEL_PATH, 'detection_models/haarcascade_frontalface_default.xml')
        emotion_model_path = posixpath.join(MODEL_PATH, 'emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5')
        cnn_model_path = posixpath.join(MODEL_PATH, 'cnn_models/cnn_threshold140.h5')
        self._cnn_model = load_model(cnn_model_path)
        self._face_detection = load_detection_model(detection_model_path)
        self._emotion_classifier = load_model(emotion_model_path, compile=False)

    def read_pos_emoji(self, image):
        position = ['none', 'left', 'right']
        emoji = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

        emotion_target_size = self._emotion_classifier.input_shape[1:3]

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(self._face_detection, gray_image)
        emotion_offsets = (20, 40)
        emotion_label_arg = None

        for face_coordinates in faces:

            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, emotion_target_size)
            except Exception as e:
                sys.stderr.write(str(e))
                sys.stderr.flush()

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            if gray_face.shape[0] == 0 or gray_face.shape[1] == 0:
                continue

            emotion_prediction = self._emotion_classifier.predict(gray_face)
            emotion_label_arg = int(np.argmax(emotion_prediction))

        if len(faces) == 0 or emotion_label_arg is None:
            emo = 'none'
        else:
            emo = emoji[emotion_label_arg]

        image_compress = cv2.resize(image, (80, 60),
                                    interpolation=cv2.INTER_CUBIC)
        image_compress = cv2.flip(image_compress, 1)
        image_compress = cv2.cvtColor(image_compress, cv2.COLOR_BGR2GRAY)
        image_compress = np.reshape(image_compress, (-1, 60, 80, 1))

        y = self._cnn_model.predict(image_compress)
        pos = position[int(np.argmax(y))]

        return emo, pos
