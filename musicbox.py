#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import OPi.GPIO as GPIO
from time import sleep
import os
import subprocess
import signal
import random

#Install info:
#  sudo pip3 install OrangePi.GPIO
#  sudo apt install sox libsox-fmt-all
#
#We're using https://github.com/Jeremie-C/OrangePi.GPIO because it implements pull-up/down and OPi.GPIO library doesn't

#Add User to Groups:
#  sudo usermod -a -G audio orangepi
#
#Make sure audio is set to output from line out and not hdmi:
#  pacmd set-default-sink 0
#
#Normalize tracks to volumes are relatively the same
#  sudo apt install normalize-audio
#  normalize-audio -m *

musicdir = "/home/orangepi/musicbox/music/"
startupsound = "ding.wav.mp3"

#Assign favorite songs:
favorite1 = "13 - The Goldfish.mp3"
favorite2 = "11 - Drivin' in My Car.mp3"
favorite3 = "02 - Rocketship Run.mp3"
favorite4 = "08 - Fast And Slow (The Rabbit And The Turtle).mp3"
favorite5 = "01 - Bumblebee (Buzz Buzz).mp3"
favorite6 = "04 - We Are The Dinosaurs.mp3"

#Assign Buttons:
but_play = GPIO.PA+10
but_stop = GPIO.PA+20
but_fav1 = GPIO.PA+9
but_fav2 = GPIO.PA+8
but_fav3 = GPIO.PA+7
but_fav4 = GPIO.PC+7
but_fav5 = GPIO.PC+4
but_fav6 = GPIO.PD+14

#Button timeout (how long to wait before another button press can happen)
play_button_timeout = 2
stop_button_timeout = 1

randomlist = os.listdir(musicdir)
randomlist.pop(randomlist.index(startupsound))  #Don't play startup sound in random playlist
random.shuffle(randomlist)

process = None
keep_playing = True
playlist_idx = 0
playlist_size = len(randomlist)

def play(f):
    global process
    killprocess(process)
    cmd = 'play "' + musicdir + f + '"'
    #cmd = cmd.replace(" ","\ ").replace("'","\\'")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    sleep(play_button_timeout)

def play_next():
    global playlist_idx
    #Sanity check idx value
    if playlist_idx >= playlist_size:
        playlist_idx = 0
    #Preserve idx to use this time around
    cur_idx = playlist_idx
    #Inc idx for next time
    playlist_idx += 1
    play(randomlist[cur_idx])

def killprocess(p):
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGINT)
        sleep(0.5)
    except:
        return

def killplay():
    reset_playing_flag()
    #Kills all instances of play
    try:
        for line in os.popen("ps ax | grep play | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)
    except:
        pass

def reset_playing_flag(status=False):
    global keep_playing
    keep_playing = status

#Pinout: https://i.stack.imgur.com/lzt4s.png
GPIO.setboard(GPIO.PCPCPLUS)        # Orange Pi PC Plus
GPIO.setmode(GPIO.SOC)        # set up BOARD SOC numbering
GPIO.setup(but_play, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but_fav1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but_fav2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but_fav3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but_fav4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but_fav5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but_fav6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

killplay()
print("\n##### Music Box Running and Ready #####\n")
process = play(startupsound)
sleep(0.5)

try:
    while True:
        if not GPIO.input(but_stop):
            print("\n##### Stop Button Pressed #####\n")
            reset_playing_flag()
            killplay()
            sleep(stop_button_timeout)
        elif not GPIO.input(but_play):
            print("\n##### Play Button Pressed #####\n")
            reset_playing_flag(status=True)
            play_next()
        elif not GPIO.input(but_fav1):
            print("\n##### Favorite1 Button Pressed #####\n")
            reset_playing_flag()
            play(favorite1)
        elif not GPIO.input(but_fav2):
            print("\n##### Favorite2 Button Pressed #####\n")
            reset_playing_flag()
            play(favorite2)
        elif not GPIO.input(but_fav3):
            print("\n##### Favorite3 Button Pressed #####\n")
            reset_playing_flag()
            play(favorite3)
        elif not GPIO.input(but_fav4):
            print("\n##### Favorite4 Button Pressed #####\n")
            reset_playing_flag()
            play(favorite4)
        elif not GPIO.input(but_fav5):
            print("\n##### Favorite5 Button Pressed #####\n")
            reset_playing_flag()
            play(favorite5)
        elif not GPIO.input(but_fav6):
            print("\n##### Favorite6 Button Pressed #####\n")
            reset_playing_flag()
            play(favorite6)

        #Handle auto-play
        if keep_playing and process.poll() is not None:
            play_next()

        sleep(0.1)

finally:
    GPIO.cleanup()
