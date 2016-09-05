'''
This is a tester program that plays the music/sequence files locally.

The syntax to run this program is as follows:
    python sequencer.py <filename without extension>
'''

#!/usr/bin/env python

from __future__ import division
import RPi.GPIO as GPIO, time
import sys
import time
import pygame

# Defines the mapping of logical mapping to physical mapping
# 1 - 5 are lights from top to bottom on tree
# 6 = RED
# 7 = GREEN
# 8 = BLUE

gpio_pins = []

print 'Beginning setup'

# Get the output pin numbers
with open('setup.txt', 'r') as f:
    data = f.readlines()
    for i in range(8):
        gpio_pins.append(int(data[i]))

# Setup the board
GPIO.setmode(GPIO.BCM)
for i in range(8):
    GPIO.setup(gpio_pins[i], GPIO.OUT)
    GPIO.output(gpio_pins[i], GPIO.LOW)
time.sleep(2.0)

print 'Setup complete'

# Start the music
print 'Starting the music'

music = 'static/music/' + sys.argv[1] + '.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play()

print 'Music started'

# Start sequencing the associated file
print 'Starting to sequence the associated file'

start_time = int(round(time.time() * 1000))

with open('static/sequences/' + sys.argv[1] + '.txt', 'r') as f:
    data = f.readlines()
    for i in range(1, len(data)):
        if data[i][0] != '#':
            if data[i].strip() != '':
                [tm, command, value] = map(int, data[i].split(','))
                curr_time = int(round(time.time() * 1000)) - start_time
                while curr_time < tm:
                    curr_time = int(round(time.time() * 1000)) - start_time
                GPIO.output(gpio_pins[command - 1], value)
                print 'Command executed. Time = ' + str(tm) + ', LED # = ' + str(command) + ', on/off = ', str(value)

# Turn off all lights
for i in range(8):
    GPIO.output(gpio_pins[i], False)

# Wait for the music to end
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

print 'Music ended'
print 'Successfully completed execution.'
