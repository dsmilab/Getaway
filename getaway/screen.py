from collections import deque

__all__ = ['Chatbox']


class Chatbox(object):
    ROWS = 3

    def __init__(self):
        self._messages = deque([''] * Chatbox.ROWS)

    def insert_message(self, text):
        if len(self._messages) >= Chatbox.ROWS:
            self._messages.popleft()
        self._messages.append(text)


