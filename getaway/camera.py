from .config import *
import cv2
import sys


class Camera:
    def __init__(self):
        self._cap = None
        # create instance of VideoCapture
        self._cap = cv2.VideoCapture(posixpath.join(MAP_PATH, 'left_view.mp4'))
        # set frame rate
        self._cap.set(cv2.CAP_PROP_FPS, 60)
        sys.stdout.write('camera started!\n')
        sys.stdout.flush()

    def read(self):
        return self._cap.read()

    def set_frame_rate(self, frame_rate=60):
        self._cap.set(cv2.CAP_PROP_FPS, frame_rate)

    def set_window_size(self, width, height):
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame_rate(self):
        return self._cap.get(cv2.CAP_PROP_FPS)

    def get_window_size(self):
        width = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return width, height

    def release(self):
        self._cap.release()
