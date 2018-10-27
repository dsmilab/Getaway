from .config import *
from .client import *
from .image import *
from tkinter import *
import cv2
from PIL import Image, ImageTk
from glob import glob
from tkinter.scrolledtext import ScrolledText
import tkinter.font as tkFont


class GUI(Tk):

    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title('Getaway')
        self.geometry('1800x1100')
        self.resizable(width=False, height=False)
        self._client = Client()
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

    @property
    def client(self):
        return self._client


class _StartScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self._controller = controller

        self._labels = {}
        self._chatbox = {}
        self._canvas = {}
        self._cap = {}
        self._concentric = []
        self._images = {}
        self._buttons = {}
        self.__init_screen()

    def __init_screen(self):
        self.__create_movies()
        self.__create_concentric()
        self.__create_buttons()
        self.__create_chatbox()

    def __create_movies(self):
        self._canvas['friend_bg'] = Canvas(self)
        self._canvas['friend_bg'].place(x=0, y=100, width=800, height=600)
        self._cap['friend_bg'] = cv2.VideoCapture('data/map/20181027_075228.mp4')

        self._canvas['me_bg'] = Canvas(self)
        self._canvas['me_bg'].place(x=1000, y=100, width=800, height=600)
        self._cap['me_bg'] = cv2.VideoCapture('data/map/20181027_075228.mp4')

        self.after(16, self._play_movie)

    def __create_concentric(self):
        files = sorted(glob('data/concentric/*.png'))
        for filename in files:
            img = Image.open(filename).convert('RGBA')
            img = img.resize((100, 100), Image.ANTIALIAS)
            self._concentric.append(ImageTk.PhotoImage(img))

        # self._canvas['friend_concentric'] = Canvas(self)
        # self._canvas['friend_concentric'].place(x=0, y=0, width=1200, height=800)

    def __create_buttons(self):
        self._buttons['shoot'] = Button(self, text='shoot')
        self._buttons['shoot'].bind('<Button-1>', self.__click_shoot_button)
        self._buttons['shoot'].place(x=800, y=800, width=200, height=50)

    def __create_chatbox(self):
        for id_, name in enumerate(['friend_bg', 'me_bg']):
            self._chatbox[name] = Text(self,
                                       wrap=WORD,
                                       highlightbackground='black',
                                       border=0,
                                       font=("helvetica", 18),
                                       fg='white',
                                       state=DISABLED,
                                       bg='black')

            self._chatbox[name].place(x=1 + 1000 * id_, y=599, width=300, height=100)

    def __click_shoot_button(self, event):
        self._controller.client.play_sound(posixpath.join(SOUND_PATH, 'gun_effect_1.mp3'))
        self._chatbox['friend_bg'].config(state=NORMAL)
        self._chatbox['friend_bg'].insert(END, 'fighting!\n')
        self._chatbox['friend_bg'].see(END)
        self._chatbox['friend_bg'].config(state=DISABLED)

    def _play_movie(self):
        self._show_frame(0)
        self._show_frame(1)
        self.after(16, self._play_movie)

    def _show_frame(self, who):
        name = 'friend_bg' if who == 0 else 'me_bg'
        self._canvas[name].delete('all')

        ret, frame = self._cap[name].read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        if who == 0:
            cv2image = geta_zoom(cv2image, 10)
        img = Image.fromarray(cv2image).resize((800, 600))
        self._images[name] = ImageTk.PhotoImage(image=img)
        self._canvas[name].create_image(0, 0, image=self._images[name], anchor=NW)
        self._canvas[name].create_image(400, 300, image=self._concentric[1], anchor=CENTER)
        # self._canvas[name].create_text(0, 0, font=("helvetica", 50), text="fighting!", fill='white', anchor=NW)
