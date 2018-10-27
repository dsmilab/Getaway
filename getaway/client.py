from .config import *
import threading
import posixpath
import os

__all__ = ['Client']


class Client(object):

    def __init__(self):
        pass

    @staticmethod
    def play_sound(sound_path):
        def __os_system(sound_path_):
            os.system('play ' + sound_path_)

        threading.Thread(target=__os_system, args=(sound_path,)).start()
