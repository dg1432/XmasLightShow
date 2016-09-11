#!/usr/bin/env python

from __future__ import division
from flask import Flask, render_template, request
from forms import MusicForm
import RPi.GPIO as GPIO, time
import pygame
import time
import sys

print 'Beginning setup'

# Create the Flask app
app = Flask(__name__)
app.secret_key = 's3cr3t'

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = RED
# 7 = GREEN
# 8 = BLUE

gpio_pins = []

# Song data to be passed to the web page
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
  'WizardsInWinter' : {
    'filename' : 'WizardsInWinter',
    'name' : 'Wizards in Winter',
    'artist' : 'Trans-Siberian Orchestra',
    'time' : '3:03'
  }
}

# Set up the music mixer
pygame.init()
pygame.mixer.init()

# Get the output pin numbers
with open('setup.txt', 'r') as f:
    data = f.readlines()
    for i in range(8):
        gpio_pins.append(int(data[i]))

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for i in range(8):
    GPIO.setup(gpio_pins[i], GPIO.OUT)
    GPIO.output(gpio_pins[i], GPIO.LOW)
time.sleep(2.0)

print 'Setup complete'

@app.route('/', methods = ['GET', 'POST'])
def main():
    if request.method == 'POST':
        # Get the name of the song
        key_list = request.form.keys()
        key_list.remove('Play')
        key_list.remove('musicTable_length')
        song_name = key_list[0].split('.')[0]

        reset()

        # Start the music
        print 'Starting the music'

        music = 'static/music/' + song_name + '.mp3'
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()

        print 'Music started'

        # Sequence the associated file
        print 'Starting to sequence the associated file'

        start_tm = int(round(time.time() * 1000))

        with open('static/sequences/' + song_name + '.txt', 'r') as f:
            data = f.readlines()
            for i in range(1, len(data)):
                # Ignore comments and blank lines
                if data[i][0] != '#' and data[i].strip() != '':
                    [tm, command, value] = map(int, data[i].split(','))
                    curr_tm = int(round(time.time() * 1000)) - start_tm

                    while curr_tm < tm:
                        curr_tm = int(round(time.time() * 1000)) - start_tm

                    GPIO.output(gpio_pins[command - 1], value)

                    print 'Command executed. Time = ' + str(tm) + ', LED # = ' + str(command)

        # Turn off all lights
        for i in range(8):
            GPIO.output(gpio_pins[i], False)
        # Wait for the music to end
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print 'Music ended'
        print 'Successfully completed execution.'
        return render_template('home.html', song_list = song_list)

    elif request.method == 'GET':
        form = MusicForm()
        return render_template('home.html', form = form, song_list = song_list)

def reset():
    # Stop any music that is playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    # Turn off all lights
    for i in range(8):
        GPIO.output(gpio_pins[i], False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
