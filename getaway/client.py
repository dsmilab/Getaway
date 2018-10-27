from .config import *
import threading
import posixpath
import os
from PIL import Image, ImageTk

__all__ = ['Client']


class Client(object):

    def __init__(self):
        self._canvas_img = {}
        self._timer_count = {}

    @staticmethod
    def play_sound(sound_path):
        def __os_system(sound_path_):
            os.system('play ' + sound_path_)

        threading.Thread(target=__os_system, args=(sound_path,)).start()

    def add_image(self, keyword, x, y, filename):
        img = Image.open(filename).convert('RGBA')
        img = img.resize((100, 100), Image.ANTIALIAS)
        print(img)
        self._canvas_img[keyword] = (x, y, img)

    def remove_image(self, keyword):
        self._canvas_img.pop(keyword, None)

    @property
    def canvas_img(self):
        return self._canvas_img
