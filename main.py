# -*- coding: utf-8 -*-
from game import *
from sound import *
from cp import *
import os
import time

run = True
global my_game, game_list, game_state, answer, bodovi, last_game_key
global current_game_page, random_flag, ukupni_bodovi
ukupni_bodovi = 0
bodovi = 8
random_flag=False
current_game_page = 0
current_result_page = 0
STATE_SHOWING_MENU=0
STATE_SHOWING_GAMES=1
STATE_PLAYING_GAME=2
STATE_SHOWING_RESULT=3
SETTINGS_DIR = "Postavke/"
IKS = "iks.png"
CHECKMARK = "kvaka.png"
NEXT = "next.png"
BACK = "back.png"
FILE_SCORE = "rezultati.dat"
CONFIG_FILE = "postavke.config"
millis = 0
flag_sound = 0

def gpio_to_use(channel):
    if(channel == 4): return 6
    if(channel == 5): return 7
    if(channel == 6): return 5
    if(channel == 7): return 8
    if(channel == 12): return 1
    if(channel == 13): return 3
    if(channel == 19): return 2
    if(channel == 26): return 4
    if(channel == 23): return 9

def my_callback(channel):
            global my_game, game_list, game_state, answer, SETTINGS_DIR
            global IKS, CHECKMARK, bodovi, current_game_page, random_flag
            global ukupni_bodovi, current_result_page
            global millis, flag_sound
            
            if(int(round(time.time() * 1000))-millis > 300):
                if(GPIO.input(channel)):
                    key = gpio_to_use(channel) - 1
                    print key 
                    if(key == 8):
                        if (game_state == STATE_PLAYING_GAME):
                            game_state = STATE_SHOWING_GAMES
                            if(ukupni_bodovi>0):
                                save_score()
                            my_game.show_game_list(current_game_page)
                        elif(game_state == STATE_SHOWING_MENU):
                            #print "dobar sam ki kruh"
                            game_state = STATE_SHOWING_MENU
                        else:
                            game_state = STATE_SHOWING_MENU
                            show_start_menu()
                    elif(game_state == STATE_PLAYING_GAME):
                        sound = Sound()
                        if(answer == key ):
                            if(flag_sound == 1):
                                sound.sound_bingo()
                            my_game.replace_image(key, SETTINGS_DIR + CHECKMARK)
                            print "bingo"
                            ukupni_bodovi = ukupni_bodovi + bodovi
                            sleep(1)
                            if(random_flag==False):
                                play_game(last_game_key)
                            else:
                                random = randint(0,len(game_list)-1)
                                play_game(random)
                        else:
                            if(flag_sound == 0):
                                sound.sound_wrong()
                            my_game.replace_image(key, SETTINGS_DIR + IKS)
                            #print "wrong"
                            if (bodovi == 0):
                                bodovi = 0
                            else:
                                bodovi = bodovi - 1
                    elif(game_state == STATE_SHOWING_GAMES):
                        if(key == 6):
                            if(current_game_page==0):
                                random = randint(0,len(game_list)-1)
                                random_flag = True
                                #print "Random ",random
                                #print "game list ",len(game_list)
                                play_game(random)
                            else:
                                current_game_page = current_game_page - 1
                                my_game.show_game_list(current_game_page)
                        elif(key == 7):
                            #game_list = my_game.get_all_games()
                            if((len(my_game.get_all_games()))/6 > current_game_page):
                                current_game_page = current_game_page + 1
                                my_game.show_game_list(current_game_page)
                        else:
                            play_game(key + (6*current_game_page))
                            print "page ",current_game_page

                    elif(game_state == STATE_SHOWING_MENU):
                        if(key == 0):
                            game_list=my_game.show_game_list(current_game_page)
                            game_state = STATE_SHOWING_GAMES
                        elif(key == 2):
                            print "postavke"
                            update_folders()
                        elif(key == 3):
                            print "GASIM"
                            #os.system("sudo shutdown -h now")
                        elif(key==1):
                            print "prikaz Rezultati"
                            game_state = STATE_SHOWING_RESULT
                            my_game.show_result(current_result_page)
                    elif(game_state == STATE_SHOWING_RESULT):
                        if(key==6):
                            if(current_result_page==0):
                                current_result_page = 0
                            else:
                                current_result_page = current_result_page - 1
                                my_game.show_result(current_result_page)
                        elif(key==7):
                            if(score_count()>current_result_page*6+6):
                                current_result_page = current_result_page + 1
                                my_game.show_result(current_result_page)
                            else:
                                current_result_page = current_result_page
                    millis = int(round(time.time() * 1000))

def play_game(key):
            global answer, last_game_key, game_state, bodovi
            bodovi = 8
            game_state = STATE_PLAYING_GAME
            last_game_key = key
            print "Key ",key
            photo_list = my_game.make_game_image(game_list[key])
            answer = randint(0, 7)
            my_game.show_answer(photo_list[answer])
            my_game.show_images(photo_list)
            

def show_start_menu():
    global game_state
    my_game.show_menu()
    game_state = STATE_SHOWING_MENU
    

def score_count():
    hisc=open(SETTINGS_DIR + FILE_SCORE,"r")
    i = 0
    for line in hisc:
        i+=1
    hisc.close()
    i = i / 3
    return i


def sound_play():
    global flag_sound
    count = 0              
    hisc=open(SETTINGS_DIR + CONFIG_FILE,"r")
    for line in hisc:
        if(count == 7):
            flag_sound = int (line[:-1])
        count = count + 1
    hisc.close()

def update_folders():
    count = 0
    folder1 = ""
    folder2 = ""
    
    hisc=open(SETTINGS_DIR + CONFIG_FILE,"r")
    for line in hisc:
        if(count == 1):
            folder1 = line
        elif(count == 3):
            folder2 = line
        count = count + 1
    hisc.close()
    
    my_dispatch = Dispatch('aaron')
    node1 = Node(folder1[:-1], 'node1')
    node2 = Node(folder2[:-1], 'node2')
    my_dispatch.add_node(node1)
    my_dispatch.add_node(node2)
    my_dispatch.compare_nodes()
    print 'Total files copied ' + str(my_dispatch.file_copied_count)
    print 'Total folders copied ' + str(my_dispatch.folder_copied_count)



def save_score():
    global ukupni_bodovi, current_result_page

    current_result_page = 0

    localtime = time.asctime(time.localtime(time.time()))

    #citanje zadnje linije u file-u tj koliko korisnika je uneseno
    hisc=open(SETTINGS_DIR + FILE_SCORE,"r")
    igrac = int(hisc.readlines()[-1]) + 1
    hisc.close()

    #append - dodavanje na kraj file-a novi rezultat
    hisc=open(SETTINGS_DIR + FILE_SCORE,"a")
    hisc.write("\nIgrac " + str(igrac) + ": " + str(ukupni_bodovi) + "\nVrijeme: " + str(localtime) + "\n")
    hisc.write(str(igrac))
    hisc.close()

def main():
    global my_game, game_list, current_game_page
    sound_play()
    my_game = Game()
    my_game.add_events(my_callback)
    show_start_menu()
    my_game.root_frame.mainloop()

if __name__ == '__main__':
    main()
