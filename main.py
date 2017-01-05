# -*- coding: utf-8 -*-
from game import *
from sound import *

run = True
global my_game, game_list, game_state, answer, bodovi, last_game_key
global current_game_page
bodovi = 0
current_game_page = 0
STATE_SHOWING_GAMES=0
STATE_PLAYING_GAME=1
SETTINGS_DIR = "Postavke/"
IKS = "iks.png"
CHECKMARK = "kvaka.png"
NEXT = "next.png"
BACK = "back.png"
BLANK = "blank.png"

def gpio_to_use(channel):
    if(channel == 4): return 1
    if(channel == 5): return 2
    if(channel == 6): return 3
    if(channel == 7): return 4
    if(channel == 12): return 5
    if(channel == 13): return 6
    if(channel == 19): return 7
    if(channel == 26): return 8

def my_callback(channel):
            global my_game, game_list, game_state, answer, SETTINGS_DIR
            global IKS, CHECKMARK, bodovi, current_game_page
            sleep(.1)
            if(GPIO.input(channel)):
                key = gpio_to_use(channel) -1
                print key
                if(game_state == STATE_PLAYING_GAME):
                    sound = Sound()
                    if(answer == key ):
                        sound.sound_bingo()
                        my_game.replace_image(key, SETTINGS_DIR + CHECKMARK)
                        print "bingo"
                        bodovi = bodovi + 8
                        print "Bodovi= ", bodovi
                        sleep(1)
                        play_game(last_game_key)
                    else:
                        sound.sound_wrong()
                        my_game.replace_image(key, SETTINGS_DIR + IKS)
                        print "wrong"
                        bodovi = bodovi - 1
                elif(game_state == STATE_SHOWING_GAMES):
                    if(key == 6):
                        if(current_game_page!=0):
                            current_game_page = current_game_page - 1
                            my_game.show_game_list(current_game_page)
                    elif(key == 7):
                        #game_list = my_game.get_all_games()
                        if((len(my_game.get_all_games()))/6 > current_game_page):
                            current_game_page = current_game_page + 1
                            my_game.show_game_list(current_game_page)
                    else:
                        play_game(key)
                        game_state = STATE_PLAYING_GAME
                    return

def play_game(key):
            global answer, last_game_key
            last_game_key = key
            photo_list = my_game.make_game_image(game_list[key])
            answer = randint(0, 7)
            my_game.show_answer(photo_list[answer])
            my_game.show_images(photo_list)


def main():
    global my_game, game_list, game_state, current_game_page
    my_game = Game()
    my_game.add_events(my_callback)
    game_list=my_game.show_game_list(current_game_page)
    game_state = STATE_SHOWING_GAMES
    my_game.root_frame.mainloop()

if __name__ == '__main__':
    main()
