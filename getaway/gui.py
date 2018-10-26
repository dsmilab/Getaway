from tkinter import *
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from glob import glob


class GUI(Tk):

    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title('Getaway')
        self.geometry('1600x1200')
        self.resizable(width=False, height=False)
        self._stage = 0
        self._screen = None

        self.__init_window()

    def __init_window(self):
        self._container = Frame(self)
        self._container.pack(side='top', fill='both', expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)
        self._switch_screen(_StartScreen)

    def goto_next_screen(self, now_scr):
        pass

    def _switch_screen(self, scr):
        if self._screen:
            self._screen.grid_forget()
            self._screen.destroy()

        self._screen = scr(parent=self._container, controller=self)
        self._screen.grid(row=0, column=0, sticky="nsew")
        self._screen.tkraise()


class _StartScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self._controller = controller

        self._labels = {}
        self._canvas = {}
        self._cap = {}
        self._concentric = []
        self._images = {}
        self.__init_screen()

    def __init_screen(self):
        self.__create_movies()
        self.__create_concentric()

    def __create_movies(self):
        self._canvas['friend_bg'] = Canvas(self)
        self._canvas['friend_bg'].place(x=0, y=50, width=800, height=600)
        self._cap['friend_bg'] = cv2.VideoCapture('data/map/20181025_210601.mp4')

        self._canvas['me_bg'] = Canvas(self)
        self._canvas['me_bg'].place(x=800, y=50, width=800, height=600)
        self._cap['me_bg'] = cv2.VideoCapture('data/map/20181025_211153.mp4')

        self.after(16, self._play_movie)

    def __create_concentric(self):
        files = sorted(glob('data/concentric/*.png'))
        for filename in files:
            img = Image.open(filename).convert('RGBA')
            img = img.resize((100, 100), Image.ANTIALIAS)
            self._concentric.append(ImageTk.PhotoImage(img))

        # self._canvas['friend_concentric'] = Canvas(self)
        # self._canvas['friend_concentric'].place(x=0, y=0, width=1200, height=800)

    def _play_movie(self):
        self._show_frame(0)
        self._show_frame(1)
        self.after(16, self._play_movie)

    def _show_frame(self, who):
        name = 'friend_bg' if who == 0 else 'me_bg'
        self._canvas[name].delete('all')
        ret, frame = self._cap[name].read()

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image).resize((800, 600))
        imgtk = ImageTk.PhotoImage(image=img)
        self._images[name] = imgtk
        self._canvas[name].create_image(0, 0, image=self._images[name], anchor=NW)
        self._canvas[name].create_image(400, 300, image=self._concentric[1], anchor=CENTER)
