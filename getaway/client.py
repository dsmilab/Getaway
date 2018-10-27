from .config import *
import threading
import posixpath
import os
from PIL import Image, ImageTk

__all__ = ['Client']


class Client(object):

    def __init__(self, player_name):
        self._canvas_img = {}
        self._timer_count = {}
        self._friend_avatars = ['neutral', 'neutral', 'neutral']
        self._enemy_avatars = ['neutral', 'neutral', 'neutral']

        self._friend_names = ['Ming', 'Hong', 'Thai']
        self._enemy_names = ['Liquid', 'NRG', 'Gas']

    @staticmethod
    def play_sound(sound_path):
        def __os_system(sound_path_):
            os.system('play ' + sound_path_)

        threading.Thread(target=__os_system, args=(sound_path,)).start()

    def add_image(self, keyword, x, y, filename, timer=25):
        img = Image.open(filename).convert('RGBA')
        img = img.resize((70, 70), Image.ANTIALIAS)
        self._canvas_img[keyword] = (x, y, img)
        self._timer_count[keyword] = timer

    def remove_image(self, keyword):
        self._canvas_img.pop(keyword, None)

    def refresh(self):
        tmp_timer_count = self._timer_count.copy()
        for keyword, val in tmp_timer_count.items():
            self._timer_count[keyword] -= 1
            if self._timer_count[keyword] == 0:
                self._timer_count.pop(keyword, None)
                self._canvas_img.pop(keyword, None)

    @property
    def canvas_img(self):
        return self._canvas_img

    @property
    def friend_avatars(self):
        return self._friend_avatars

    @property
    def enemy_avatars(self):
        return self._enemy_avatars

    @property
    def friend_names(self):
        return self._friend_names

    @property
    def enemy_names(self):
        return self._enemy_names