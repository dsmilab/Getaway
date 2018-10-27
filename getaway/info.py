from .tools.singleton import *
import sys

__all__ = ['Info']


class Info(metaclass=_Singleton):

    def __init__(self):
        self._friend_avatars = ['neutral', 'neutral', 'neutral']
        self._enemy_avatars = ['neutral', 'neutral', 'neutral']

        self._friend_names = ['Ming', 'Hong', 'Thai']
        self._enemy_names = ['Liquid', 'NRG', 'Gas']

    def set_friend_avatars(self, who_name, emoji):
        sys.stdout.write(str(emoji) + '\n')
        sys.stdout.flush()

        if emoji == 'none':
            return

        for i_, friend in enumerate(self._friend_names):
            if friend == who_name:
                self._friend_avatars[i_] = emoji
                break

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
