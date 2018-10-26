from tkinter import *
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class GUI(Tk):

    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title('Getaway')
        self.geometry('1024x768')
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
        self._cap = cv2.VideoCapture('data/map/20181025_210601.mp4')
        self.__init_screen()

    def __init_screen(self):
        self._lmain = Label(self)
        self._lmain.grid(row=0, column=0)
        self._lmain.after(10, self._show_frame)

    def _show_frame(self):
        ret, frame = self._cap.read()

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image).resize((1024, 768))
        imgtk = ImageTk.PhotoImage(image=img)
        self._lmain.imgtk = imgtk
        self._lmain.configure(image=imgtk)
        self._lmain.after(10, self._show_frame)
