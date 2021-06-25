#!/usr/bin/python

"""
Handles interrupts from GPIO pins following KY040 actions (rotating or pressing)
Then publishes MIDI messages on a virtual MIDI port for mixxx

GorgiAstro - Clément Jonglez (clement@jonglez.space)

This code is largely inspired from https://blog.sharedove.com/adisjugo/index.php/2020/05/10/using-ky-040-rotary-encoder-on-raspberry-pi-to-control-volume/
"""

import mido
import os
from RPi import GPIO
from time import sleep

# Set up virtual MIDI port
outport = mido.open_output('KY-040 Rotary encoder', virtual=True)

step = 5  # linear steps for increasing/decreasing volume
paused = False  # paused state

# tell to GPIO library to use logical PIN names/numbers, instead of the physical PIN numbers
GPIO.setmode(GPIO.BCM)

# set up the pins we have been using
clk = 17
dt = 18
sw = 27

# set up the GPIO events on those pins
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# get the initial states
counter = 0
clkLastState = GPIO.input(clk)
dtLastState = GPIO.input(dt)
swLastState = GPIO.input(sw)

# define functions which will be triggered on pin state changes

def clkClicked(channel):
    global counter
    global step

    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)

    if clkState == 0 and dtState == 1:
        counter = counter + step
        msg = mido.Message('control_change', control=1, value=0)
        outport.send(msg)


def dtClicked(channel):
    global counter
    global step

    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)

    if clkState == 1 and dtState == 0:
        counter = counter - step
        msg = mido.Message('control_change', control=0, value=0)
        outport.send(msg)


def swClicked(channel):
    global paused
    paused = not paused
    #print ("Paused ", paused)
    msg = mido.Message('control_change', control=2, value=1)
    outport.send(msg)


# set up the interrupts
GPIO.add_event_detect(clk, GPIO.FALLING, callback=clkClicked, bouncetime=200)
GPIO.add_event_detect(dt, GPIO.FALLING, callback=dtClicked, bouncetime=200)
GPIO.add_event_detect(sw, GPIO.FALLING, callback=swClicked, bouncetime=200)

while True:
    sleep(1)
