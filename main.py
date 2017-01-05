# -*- coding: utf-8 -*-
from game import *
from sound import *

run = True
global my_game, game_list, game_state, answer
STATE_SHOWING_GAMES=0
STATE_PLAYING_GAME=1
SETTINGS_DIR = "Postavke/"
IKS = "iks.png"
CHECKMARK = "kvaka.png"

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
            global my_game, game_list, game_state, answer, SETTINGS_DIR, IKS, CHECKMARK
            sleep(.1)
            if(GPIO.input(channel)):
                key = gpio_to_use(channel) -1
                print "key", key
                if(game_state == STATE_PLAYING_GAME):
                    sound = Sound()
                    if(answer == key ):
                        my_game.replace_image(key, SETTINGS_DIR + CHECKMARK)
                        sound.sound_bingo()
                        print "bingo"
                    else:
                         my_game.replace_image(key, SETTINGS_DIR + IKS)
                         sound.sound_wrong()
                         print "wrong"
                elif(game_state == STATE_SHOWING_GAMES):
                    play_game(key)
                    game_state = STATE_PLAYING_GAME
                    return



def play_game(key):
            global answer
            photo_list = my_game.make_game_image(game_list[key])
            answer = randint(0, 7)
            my_game.show_answer(photo_list[answer])
            my_game.show_images(photo_list)


def main():
    global my_game, game_list, game_state
    my_game = Game()
    game_list=my_game.show_game_list()
    game_state = STATE_SHOWING_GAMES
    my_game.add_events(my_callback)
    my_game.root_frame.mainloop()

if __name__ == '__main__':
    main()
