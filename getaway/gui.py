from .config import *
from .client import *
from .image import *
from tkinter import *
from .camera import Camera

import re
import cv2
from PIL import Image, ImageTk
from glob import glob


class GUI(Tk):

    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.title('Getaway')
        self.geometry('1800x1000')
        self.resizable(width=False, height=False)
        self._clients = [Client('Hong'), Client('Ming')]
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
    def clients(self):
        return self._clients


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
        self._camera = Camera()
        
        self.__init_screen()

    def __init_screen(self):
        self.__create_background()
        self.__create_movies()
        self.__create_images()
        self.__create_buttons()
        self.__create_chatbox()

    def __create_background(self):
        # self._canvas['bg'] = Canvas(self)
        #
        # self._canvas['bg'].place(x=0, y=0, width=1800, height=1000)
        filename = posixpath.join(HUD_PATH, 'bg.png')
        self._bg_image = PhotoImage(file=filename)
        background_label = Label(self, image=self._bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # self._canvas['bg'].pack()

    def __create_movies(self):
        self._canvas['friend_bg'] = Canvas(self)
        self._canvas['friend_bg'].place(x=0, y=100, width=800, height=600)
        self._cap['friend_bg'] = cv2.VideoCapture('data/map/20181027_075601.mp4')

        self._canvas['me_bg'] = Canvas(self)
        self._canvas['me_bg'].place(x=1000, y=100, width=800, height=600)
        self._cap['me_bg'] = cv2.VideoCapture('data/map/20181027_075228.mp4')

        self._canvas['camera'] = Canvas(self)
        self._canvas['camera'].place(x=1400, y=700, width=400, height=300)

        self.after(16, self._play_movie)

    def __create_images(self):
        files = sorted(glob('data/concentric/*.png'))
        for filename in files:
            img = Image.open(filename).convert('RGBA')
            res = re.search('\w*.png', filename).group(0)
            fname = res[:-4]
            if fname != 'concentric_02':
                img = img.resize((100, 100), Image.ANTIALIAS)
            self._concentric.append(ImageTk.PhotoImage(img))

        files = sorted(glob('data/emoji/*.png'))
        for filename in files:
            img = Image.open(filename).convert('RGBA')
            img = img.resize((35, 35), Image.ANTIALIAS)
            res = re.search('\w*.png', filename).group(0)
            fname = res[:-4]
            self._images[fname] = ImageTk.PhotoImage(img)

        files = sorted(glob('data/gun_walk/*.png'))
        for filename in files:
            img = Image.open(filename).convert('RGBA')
            img = img.resize((500, 200), Image.ANTIALIAS)
            res = re.search('\w*.png', filename).group(0)
            fname = res[:-4]
            self._images[fname] = ImageTk.PhotoImage(img)

        filename = posixpath.join(HUD_PATH, 'radar_map.png')
        img = Image.open(filename).convert('RGBA')
        img = img.resize((150, 150), Image.ANTIALIAS)
        self._images['radar_map'] = ImageTk.PhotoImage(img)

        filename = posixpath.join(HUD_PATH, 'hp.png')
        img = Image.open(filename).convert('RGBA')
        img = img.resize((500, 50), Image.ANTIALIAS)
        self._images['hp'] = ImageTk.PhotoImage(img)

        filename = posixpath.join(HUD_PATH, 'score.png')
        img = Image.open(filename).convert('RGBA')
        img = img.resize((400, 50), Image.ANTIALIAS)
        self._images['score'] = ImageTk.PhotoImage(img)

        filename = posixpath.join(HUD_PATH, 'team1.png')
        img = Image.open(filename).convert('RGBA')
        img = img.resize((150, 150), Image.ANTIALIAS)
        self._images['team1'] = ImageTk.PhotoImage(img)

        filename = posixpath.join(HUD_PATH, 'team2.png')
        img = Image.open(filename).convert('RGBA')
        img = img.resize((150, 150), Image.ANTIALIAS)
        self._images['team2'] = ImageTk.PhotoImage(img)
        # self._canvas['friend_concentric'] = Canvas(self)
        # self._canvas['friend_concentric'].place(x=0, y=0, width=1200, height=800)

    def __create_buttons(self):
        pass
        # self._buttons['shoot'] = Button(self, text='shoot')
        # self._buttons['shoot'].bind('<Button-1>', self.__click_shoot_button)
        # self._buttons['shoot'].place(x=800, y=800, width=200, height=50)

    def __create_chatbox(self):
        for id_, name in enumerate(['friend_bg', 'me_bg']):
            self._chatbox[name] = Text(self,
                                       wrap=WORD,
                                       highlightbackground='black',
                                       border=0,
                                       font=("helvetica", 16),
                                       fg='white',
                                       state=DISABLED,
                                       bg='black')

            self._chatbox[name].place(x=1 + 1000 * id_, y=629, width=320, height=70)

    def __click_shoot_button(self, event):
        self._controller.clients[1].play_sound(posixpath.join(SOUND_PATH, 'gun_effect_1.mp3'))
        self._chatbox['friend_bg'].config(state=NORMAL)
        self._chatbox['friend_bg'].insert(END, 'fighting!\n')
        self._chatbox['friend_bg'].see(END)
        self._chatbox['friend_bg'].config(state=DISABLED)

    def __trigger_alert_event(self, position, timer=5):
        text_str = ['alert_left', 'alert_right']
        msg_str = ['left', 'right']
        alert_img_path = posixpath.join(SIGNAL_PATH, 'alert_' + msg_str[position] + '.png')

        self._chatbox['me_bg'].config(state=NORMAL)
        self._chatbox['me_bg'].insert(END, 'You asked team to alert ' + msg_str[position] + '!\n')
        self._chatbox['me_bg'].see(END)

        self._chatbox['friend_bg'].config(state=NORMAL)
        self._chatbox['friend_bg'].insert(END, 'Ming asked You to alert ' + msg_str[position] + '!\n')
        self._chatbox['friend_bg'].see(END)
        self._chatbox['friend_bg'].config(state=DISABLED)

        self._controller.clients[0].add_image(text_str[position],
                                              position * 600,
                                              120,
                                              alert_img_path,
                                              timer)

    def __trigger_attack_event(self, position, timer=5):
        text_str = ['attack_left', 'attack_right']
        msg_str = ['left', 'right']
        attack_img_path = posixpath.join(SIGNAL_PATH, 'attack_' + msg_str[position] + '.png')

        self._chatbox['me_bg'].config(state=NORMAL)
        self._chatbox['me_bg'].insert(END, 'You asked team to attack ' + msg_str[position] + '!\n')
        self._chatbox['me_bg'].see(END)

        self._chatbox['friend_bg'].config(state=NORMAL)
        self._chatbox['friend_bg'].insert(END, 'Ming asked You to attack ' + msg_str[position] + '!\n')
        self._chatbox['friend_bg'].see(END)

        self._controller.clients[0].add_image(text_str[position],
                                              position * 600,
                                              120,
                                              attack_img_path,
                                              timer)

    def _play_movie(self):
        for cli_ in self._controller.clients:
            cli_.refresh()

        self._show_frame(0)
        self._show_frame(1)
        self._show_camera()
        self.after(16, self._play_movie)

    def _show_camera(self):
        self._canvas['camera'].delete('all')

        ret, frame = self._camera.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # cv2image = cv2.flip(cv2image, 1)
        self._controller.clients[1].write_camera_image(cv2image)
        pos = self._controller.clients[1].query_pos()
        sys.stdout.write('>> %s\n' % pos)
        sys.stdout.flush()
        if pos == 'turn_left':
            self.__trigger_alert_event(0)
        elif pos == 'turn_right':
            self.__trigger_alert_event(1)
        elif pos == 'down_left':
            self.__trigger_attack_event(0, 25)
        elif pos == 'down_right':
            self.__trigger_attack_event(1, 25)

        img = Image.fromarray(cv2image).resize((400, 300))

        self._images['camera'] = ImageTk.PhotoImage(image=img)
        self._canvas['camera'].create_image(0, 0, image=self._images['camera'], anchor=NW)

    def _show_frame(self, who):
        name = 'friend_bg' if who == 0 else 'me_bg'
        self._canvas[name].delete('all')

        ret, frame = self._cap[name].read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        if self._controller.clients[who].zoom_mode:
            cv2image = geta_zoom(cv2image, 10)

        img = Image.fromarray(cv2image).resize((800, 600))
        self._images[name] = ImageTk.PhotoImage(image=img)
        self._canvas[name].create_image(400, 300, image=self._images[name], anchor=CENTER)

        if self._controller.clients[who].zoom_mode:
            self._canvas[name].create_image(400, 300, image=self._concentric[1], anchor=CENTER)
        else:
            gun_walk_keyword = '%02d' % self._controller.clients[who].gun_walk_loop_id
            self._canvas[name].create_image(300, 400, image=self._images[gun_walk_keyword], anchor=NW)
            self._canvas[name].create_image(400, 300, image=self._concentric[0], anchor=CENTER)

        self._canvas[name].create_image(0, 0, image=self._images['radar_map'], anchor=NW)
        self._canvas[name].create_image(300, 550, image=self._images['hp'], anchor=NW)
        self._canvas[name].create_image(400, 0, image=self._images['score'], anchor=N)
        self._canvas[name].create_image(0, 250, image=self._images['team1'], anchor=NW)
        self._canvas[name].create_image(800, 250, image=self._images['team2'], anchor=NE)

        if who == 0:
            for keyword, canvas_img in self._controller.clients[who].canvas_img.items():
                x = canvas_img[0]
                y = canvas_img[1]
                img_ = canvas_img[2]
                self._images[keyword] = ImageTk.PhotoImage(image=img_)
                self._canvas[name].create_image(x, y, image=self._images[keyword], anchor=NW)

        for id_, avatar_key in enumerate(self._controller.clients[who].friend_avatars):
            self._canvas[name].create_image(150 - 20, 300 + 35 * id_, image=self._images[avatar_key], anchor=E)

        for id_, avatar_name in enumerate(self._controller.clients[who].friend_names):
            self._canvas[name].create_text(0 + 10, 300 + 35 * id_, font=("Times New Roman", 12, "bold"),
                                           text=avatar_name, fill='skyblue', anchor=W)

        for id_, avatar_key in enumerate(self._controller.clients[who].enemy_avatars):
            self._canvas[name].create_image(650 + 20, 300 + 35 * id_, image=self._images[avatar_key], anchor=W)

        for id_, avatar_name in enumerate(self._controller.clients[who].enemy_names):
            self._canvas[name].create_text(800 - 10, 300 + 35 * id_, font=("Times New Roman", 12, "bold"),
                                           text=avatar_name, fill='tomato', anchor=E)
