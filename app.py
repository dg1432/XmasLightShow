#!/usr/bin/env python

from __future__ import division
from flask import Flask, render_template, request
from forms import MusicForm
import RPi.GPIO as GPIO, time
import pygame
import time
import sys
import os
from sequencer import Sequencer

app = Flask(__name__)
app.secret_key = 's3cr3t'

sequencer = Sequencer()

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = BLUE
# 7 = GREEN
# 8 = RED
gpio_pins = []
with open('setup.txt', 'r') as f:
    data = f.readlines()
    for i in range(8):
        gpio_pins.append(int(data[i]))

# Setup the board
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for i in range(8):
    GPIO.setup(gpio_pins[i], GPIO.OUT)
    GPIO.output(gpio_pins[i], GPIO.LOW)
time.sleep(2.0)

# Get the song information
song_list = {}
with open('song_info.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        song_info = line.split(' | ')
        song_list[song_info[0]] = {}
        song_list[song_info[0]]['filename'] = song_info[0]
        song_list[song_info[0]]['name'] = song_info[1]
        song_list[song_info[0]]['artist'] = song_info[2]
        song_list[song_info[0]]['time'] = song_info[3]

pygame.init()
pygame.mixer.init()

@app.route('/', methods=['GET', 'POST'])
def main():
    form = MusicForm()
    return render_template('home.html', form=form, song_list=song_list)

@app.route('/play/<song>')
def play(song=None):
    reset()
    sequencer.run_sequence(song.strip())
    return render_template('home.html', song_list=song_list)

@app.route('/poweroff')
def poweroff():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    os.system("sudo poweroff")

def reset():
    # Stop any music that is playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    # Turn off all lights
    for i in range(8):
        GPIO.output(gpio_pins[i], False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
