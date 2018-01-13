#!/usr/bin/env python

from __future__ import division
import RPi.GPIO as GPIO, time
import sys
import time
import pygame

class Sequencer():
    # Defines the mapping of logical mapping to physical mapping
    # 1 - 5 are lights from top to bottom on tree
    # 6 = RED
    # 7 = GREEN
    # 8 = BLUE
    gpio_pins = []

    def __init__(self):
        # Get the output pin numbers
        with open('setup.txt', 'r') as f:
            data = f.readlines()
            for i in range(8):
                self.gpio_pins.append(int(data[i]))

        # Setup the board
        GPIO.setmode(GPIO.BCM)
        for i in range(8):
            GPIO.setup(self.gpio_pins[i], GPIO.OUT)
            GPIO.output(self.gpio_pins[i], GPIO.LOW)
        time.sleep(2.0)

    def run_sequence(self, song):
        music = 'static/music/' + song + '.mp3'
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()

        # Sequence the associated file
        start_time = int(round(time.time() * 1000))
        with open('static/sequences/' + song + '.txt', 'r') as f:
            data = f.readlines()
            for i in range(1,len(data)):
                if data[i][0] != '#' and data[i].strip() != '':
                    [tm, command, value] = map(int, data[i].split(','))
                    curr_time = int(round(time.time() * 1000)) - start_time
                    while curr_time < tm:
                        curr_time = int(round(time.time() * 1000)) - start_time
                    GPIO.output(self.gpio_pins[command - 1], value)
        # Turn off all lights
        for i in range(8):
            GPIO.output(self.gpio_pins[i], False)
        # Wait for the music to end
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def main():
    sequencer = Sequencer()
    sequencer.run_sequence(sys.argv[1])

if __name__ == '__main__':
    main()
