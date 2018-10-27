import cv2
import threading


class Camera:
    def __init__(self):
        self.cap = None
        # create instance of VideoCapture
        self.cap = cv2.VideoCapture(0)
        # set frame rate
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        print('camera started!')

    def read(self):
        return self.cap.read()

    def set_frame_rate(self, frame_rate=60):
        self.cap.set(cv2.CAP_PROP_FPS, frame_rate)

    def set_window_size(self, width, height):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame_rate(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

    def get_window_size(self):
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return width, height

    def release(self):
        self.cap.release()

    # #using thread to read
    # def start(self):
    #     print('camera started!')
    #     # use thread to capture image
    #     # daemon=True means run until main thread close
    #     threading.Thread(target=self.capture, daemon=True, args=()).start()
    #
    # def stop(self):
    #     self.if_stop = True
    #     print('camera stopped!')
    # def capture(self):
    #     pass



