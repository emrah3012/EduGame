# -*- coding: utf-8 -*-
from Tkinter import *
from os import listdir
from PIL import Image, ImageTk
from random import randint
from time import sleep
import sys
import random
import ttk
import sys
import RPi.GPIO as GPIO

class Game:
    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = 200
    ANSWER_SLEEP_TIME = 5
    GAMES_DIR = "Igre/"
    counter = 0

    def __init__(self):
        self.root_frame = Tk()
        self.root_frame.attributes("-zoomed", True)
        self.mainframe = ttk.Frame(self.root_frame)
        self.mainframe.grid(column=0, row=0, sticky=(N,W,S,E))
        self.root_frame.bind("<Escape>", self.exit_app())
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.init_gpio()

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #tipka 1
        GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #tipka 2
        GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #tipka 3
        GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #tipka 4

        GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def add_events(self, my_callback):
        GPIO.add_event_detect(4, GPIO.RISING, callback=my_callback, bouncetime=50)
        GPIO.add_event_detect(5, GPIO.RISING, callback=my_callback, bouncetime=50)
        GPIO.add_event_detect(6, GPIO.RISING, callback=my_callback, bouncetime=50)
        GPIO.add_event_detect(7, GPIO.RISING, callback=my_callback, bouncetime=50)

        GPIO.add_event_detect(12, GPIO.FALLING, callback=my_callback, bouncetime=50)
        GPIO.add_event_detect(13, GPIO.FALLING, callback=my_callback, bouncetime=50)
        GPIO.add_event_detect(19, GPIO.FALLING, callback=my_callback, bouncetime=50)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback, bouncetime=50)
        GPIO.add_event_detect(26, GPIO.FALLING, callback=my_callback, bouncetime=50)

    def make_game_image(self, path):
        photo_list = []

        slike = listdir(Game.GAMES_DIR + path + "/")
        self.images = []

        while len(photo_list)<8:
            slika = Game.GAMES_DIR + path + "/" + random.choice(slike)
            if slika not in photo_list:
                photo_list.append(slika)

        return photo_list


    def show_answer(self, answer):
        photo_list = []
        while len(photo_list) < 8:
            photo_list.append(answer)

        self.show_images(photo_list)
        sleep(self.ANSWER_SLEEP_TIME)

    def show_images(self, photo_list):
        c=r=0;
        for img in photo_list:
            photo = self.get_image(img)
            label = ttk.Label(image=photo).grid(column=c,row=r, padx=(100,100), pady=(100,100))
            self.images.append(photo) # dodatna referenca kako nebi garbage collector uništio sliku
            c+=1
            if(c%4==0):
                r+=1
                c=0

    def show_game_list(self):
        self.games = self.get_all_games()
        self.games.sort()
        c=r=0
        for i in range(0,8):
            label = ttk.Label(text=self.games[i], background='yellow').grid(column=c, row=r, padx=(200,200), pady=(150,150))
            c+=1

            if(c%4==0):
                  r+=1
                  c=0
        return self.games

    def exit_app(self):
        self.close_window
        global run
        run = False


    def replace_image(self, position, path):
        print "uso"
        if(position<4):
            c=position
            r=0
        else:
            c=position-4
            r=1

        iks = self.get_image(path)
        label = ttk.Label(image=iks).grid(column=c,row=r, padx=(100,100), pady=(100,100))
        self.images[position] = iks

    def create_empty_labels(self):
        self.labels = []
        self.textVars = []
        c=r=0
        for i in range(0,8):
            s = str(i) + "jfadjjjjjjjjjjjjjj"
            label = ttk.Label(textvariable=s, background='blue').grid(column=c,row=r, padx=(200,200), pady=(100,100))
            self.labels.append(label)
            self.textVars.append(s)
            c+=1

            if(c%4==0):
                  r+=1
                  c=0

    def play_game(self,i):
        self.images = self.get_images(Game.GAMES_DIR + self.games[i] + "/")

        c=r=0
        for img in self.images:
            label = ttk.Label(image = img).grid(column=c,row=r, padx=(100,100), pady=(100,100))
            self.images.append(img) # dodatna referenca kako nebi garbage collector uništio sliku
            c+=1
            if(c%4==0):
                r+=1
                c=0

    def toogle_fullscreen(self, state):
        self.root_frame.attributes("-fullscreen", state)
        return "break"

    def close_window(self, event=None):
        print "Closing window"
        self.root_frame.destroy()
        return "break"

    def get_image(self, image_path):
       image = Image.open(image_path)
       image = image.resize((Game.IMAGE_WIDTH,Game.IMAGE_HEIGHT), Image.ANTIALIAS)
       photo = ImageTk.PhotoImage(image)
       return photo

    def get_images(self, game_name):
        images = []
        for image_path in listdir(game_name):
            images.append(self.get_image(game_name + image_path))
        return images

    def get_all_games(self):
        return listdir(Game.GAMES_DIR);


