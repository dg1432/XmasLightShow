#!/usr/bin/env python

from __future__ import division
from flask import Flask, render_template, request
from forms import MusicForm
import RPi.GPIO as GPIO, time
import pygame
import time
import sys
import os

app = Flask(__name__)
app.secret_key = 's3cr3t'

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = BLUE
# 7 = GREEN
# 8 = RED

gpio_pins = []

song_list = {
  'LetItGo' : {
    'filename' : 'LetItGo',
    'name' : 'Let it Go',
    'artist' : 'Idina Menzel',
    'time': '3:37'
  },
  'CarolOfTheBells' : {
    'filename' : 'CarolOfTheBells',
    'name' : 'Carol of the Bells',
    'artist' : 'Trans-Siberian Orchestra',
    'time': '3:23'
  },
  'MadRussianXmas' : {
    'filename' : 'MadRussianXmas',
    'name' : 'A Mad Russian\'s Christmas',
    'artist' : 'Trans-Siberian Orchestra',
    'time': '4:39'
  },
  'LinusAndLucy' : {
    'filename' : 'LinusAndLucy',
    'name' : 'Linus and Lucy',
    'artist' :'Vince Guaraldi Trio',
    'time': '3:03'
  },
  'SilentNight' : {
    'filename' : 'SilentNight',
    'name' : 'Silent Night',
    'artist' : 'Christmas Carols by Candlelight',
    'time': '2:04'
  },
  'WizardsInWinter' : {
    'filename' : 'WizardsInWinter',
    'name' : 'Wizards In Winter',
    'artist' : 'Trans-Siberian Orchestra',
    'time': '3:03'
  },
  'GodRestYeMerryGentlemen' : {
    'filename' : 'GodRestYeMerryGentlemen',
    'name' : 'God Rest Ye Merry Gentlemen',
    'artist' : 'Barenaked Ladies',
    'time': '3:26'
  },
  'TwelveDaysOfChristmas' : {
    'filename' : 'TwelveDaysOfChristmas',
    'name' : 'Twelve Days of Christmas',
    'artist' : 'The Muppets',
    'time': '4:18'
  }
}

pygame.init()
pygame.mixer.init()

# Get the output pin numbers
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

@app.route('/', methods=['GET', 'POST'])
def main():
    form = MusicForm()
    return render_template('home.html', form=form, song_list=song_list)

@app.route('/play/<song>')
def play(song=None):
    reset()
    # Start the music
    music = 'static/music/' + song + '.mp3'
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()
    # Start sequencing the associated file
    start_time = int(round(time.time() * 1000))
    with open('static/sequences/' + song + '.txt', 'r') as f:
        data = f.readlines()
        for i in range(1,len(data)):
            if data[i][0] != '#' and data[i].strip() != '':
                [tm, command, value] = map(int, data[i].split(','))
                curr_time = int(round(time.time() * 1000)) - start_time
                while curr_time < tm:
                    curr_time = int(round(time.time() * 1000)) - start_time
                GPIO.output(gpio_pins[command - 1], value)
    # Turn off all lights
    for i in range(8):
        GPIO.output(gpio_pins[i], False)
    # Wait for the music to end
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    return render_template('home.html', song_list=song_list)

@app.route('/poweroff')
def poweroff():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    os.system("sudo poweroff")

'''
@app.route('/volume/<volume_value>')
def volume(volume_value):
    pygame.mixer.music.set_volume(int(volume_value) / 100)
    return render_template('home.html', song_list=song_list)
'''

def reset():
    # Stop any music that is playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    # Turn off all lights
    for i in range(8):
        GPIO.output(gpio_pins[i], False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

