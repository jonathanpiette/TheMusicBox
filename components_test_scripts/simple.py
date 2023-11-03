#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# Configuration of the KY-040 rotary encoder pins
CLK = 26
DT = 16
SW = 6

# Setup GPIO
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(CLK)

try:
    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)
        swState = GPIO.input(SW)
        
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                print("Clockwise")
            else:
                counter -= 1
                print("Counter Clockwise")
            print("Counter:", counter)
        clkLastState = clkState
        
        if swState == 0:
            print("Button Pressed")
            time.sleep(0.2)  # debounce delay

finally:
    GPIO.cleanup()