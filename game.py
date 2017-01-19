# -*- coding: utf-8 -*-
from Tkinter import *
from os import listdir
from PIL import Image, ImageTk
from random import randint
from time import sleep
from main import SETTINGS_DIR,FILE_SCORE, NEXT, BACK
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
    labels = []

    def __init__(self):
        self.root_frame = Tk()
        self.root_frame.title("Edu Game")
        self.root_frame.attributes("-zoomed", True)
        self.root_frame.config(cursor="none")
        self.toogle_fullscreen(True)
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

    def make_menu_image(self):
        photo_list = []
        self.images = []

        slike = listdir(SETTINGS_DIR + "menu/")

        for i in slike:
            slika = SETTINGS_DIR + "menu/" + i
            photo_list.append(slika)
        photo_list.sort()
        return photo_list


    def show_answer(self, answer):
        photo_list = []
        while len(photo_list) < 8:
            photo_list.append(answer)

        self.show_images(photo_list)
        sleep(self.ANSWER_SLEEP_TIME)

    def show_images(self, photo_list):
        self.create_empty_labels()
        c=r=0;
        self.images[:] = []

        for img in photo_list:
            photo = self.get_image(img)
            label = ttk.Label()
            label.grid(column=c,row=r, padx=(22,22), pady=(80,80))
            label.configure(image = photo)
            self.labels.append(label)
            self.images.append(photo) # dodatna referenca kako nebi garbage collector uništio sliku
            c+=1
            if(c%4==0):
                r+=1
                c=0

    def show_menu(self):
        self.create_empty_labels()
        self.images = []
        self.photo_list = self.make_menu_image()
        self.show_images(self.photo_list)


        #menu_options = ["Nova igra", "Rezultati", "Postavke", "Izlaz"]
        #c=r=i=0
        #for item in menu_options:
            #txt = menu_options[i]
            #label = self.labels[i]
            #label.configure(text=txt)
            #label.grid(column=c, row=r, padx=(150,150), pady=(150,150))

            #i+=1
            #c+=1

            #if(c%4==0):
                  #r+=1
                  #c=0

    #def change_label(self, position, c, r, txt, img):
        #label = self.labels[position]
        #label.configure(text=txt, image=img)
        #label.grid(column=c, row=r, padx=(200,200), pady=(150,150))

    def show_game_list(self, page):
        self.create_empty_labels()
        self.images = []

        self.games = self.get_all_games()
        self.games.sort()
        c=r=0
        for i in range(page*6,page*6+6):
            label = self.labels[i-page*6]
            if(i>=len(self.games)):
              label.configure(text="", image=None)
            else:
              label.configure(text=self.games[i])
              label.grid(column=c, row=r, padx=(150,150), pady=(150,150))

            self.labels.append(label)
            c+=1

            if(c%4==0):
                  r+=1
                  c=0

        back_img = self.get_image(SETTINGS_DIR + BACK)
        next_img = self.get_image(SETTINGS_DIR + NEXT)

        label = ttk.Label()
        if(page==0):
            label.configure(text="RANDOM", image=None)
            label.grid(column=2, row=1, padx=(150,150), pady=(150,150))
        else:
            label.configure(image=back_img)
            label.grid(column=2, row=1, padx=(22,22), pady=(80,80))
            self.images.append(back_img)


        self.labels.append(label)

        label = ttk.Label()

        if(len(self.games)>page*6+6):
            label.configure(image=next_img)
            label.grid(column=3, row=1, padx=(22,22), pady=(80,80))
            self.images.append(next_img)
        else:
            label.configure(text="", image=None)
            label.grid(column=3, row=1, padx=(22,22), pady=(80,80))


        self.labels.append(label)

        return self.games

    def exit_app(self):
        self.close_window
        global run
        run = False


    def replace_image(self, position, path):
        if(position<4):
            c=position
            r=0
        else:
            c=position-4
            r=1

        temp = self.images[position]
        iks = self.get_image(path)

        label = self.labels[position]
        self.images[position]=iks
        label.destroy()
        label = ttk.Label(image = iks)
        label.grid(column=c, row=r, padx=(22,22), pady=(80,80))

        sleep(2)

        label.configure(image=temp)
        self.images[position]=temp


    def create_empty_labels(self):
        if(self.labels!=None and len(self.labels)>0):
            for label in self.labels:
                label.destroy()

        self.labels = []

        for i in range(0,8):
            label = ttk.Label()
            self.labels.append(label)

    #def play_game(self,i):
        #self.images = self.get_images(Game.GAMES_DIR + self.games[i] + "/")

        #c=r=0
        #for img in self.images:
            #label = ttk.Label(image = img).grid(column=c,row=r, padx=(100,100), pady=(100,100))
            #self.images.append(img) # dodatna referenca kako nebi garbage collector uništio sliku
            #c+=1
            #if(c%4==0):
                #r+=1
                #c=0

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

    def show_result(self, page):
        self.create_empty_labels()
        self.images = []
        igrac = ""
        brojac = 0
        self.menu_options = []

        hisc=open(SETTINGS_DIR + FILE_SCORE,"r")
        for line in hisc:
            if(brojac==0):
                brojac = brojac + 1
            elif(brojac==1):
                igrac = igrac + line
                brojac = brojac + 1
            elif(brojac==2):
                igrac = igrac + line
                self.menu_options.append(igrac)
                brojac = 0
                igrac = ""
        hisc.close()

        self.menu_options.reverse()

        j = page*6 + 6
        c=r=i=k=0
        for item in self.menu_options:
            if(i>=page*6 and i<j):
                if(i>len(self.menu_options)-1):
                    continue
                else:
                    txt = self.menu_options[i]
                    label = self.labels[k]
                    label.configure(text=txt)
                    label.grid(column=c, row=r, padx=(60,60), pady=(150,150))

                    i+=1
                    c+=1
                    k+=1

                    if(c%4==0):
                          r+=1
                          c=0
            elif(i>j):
                break
            else:
                i+=1

        back_img = self.get_image(SETTINGS_DIR + BACK)
        next_img = self.get_image(SETTINGS_DIR + NEXT)

        label = ttk.Label()

        if(page==0):
            label.configure(text="")
            label.grid(column=2, row=1, padx=(22,22), pady=(80,80))
        else:
            label.configure(image=back_img)
            label.grid(column=2, row=1, padx=(22,22), pady=(80,80))
            self.images.append(back_img)

        self.labels.append(label)

        label = ttk.Label()

        if(j>len(self.menu_options)-1):
            label.configure(text="")
            label.grid(column=3, row=1, padx=(22,22), pady=(80,80))
        else:
            label.configure(image=next_img)
            label.grid(column=3, row=1, padx=(22,22), pady=(80,80))
            self.images.append(next_img)

        self.labels.append(label)





