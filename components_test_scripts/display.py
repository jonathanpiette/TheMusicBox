#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import logging
import spidev as SPI
import time



import circle_loop
import welcome_screen




# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to the Python path
sys.path.append(current_directory)

from lib import LCD_1inch9
from PIL import Image, ImageDraw, ImageFont

# Path to the Python scripts
welcome_screen_script = os.path.join(current_directory, "welcome_screen.py")
animation_script = os.path.join(current_directory, "animation_screen.py")
circle_loop = os.path.join(current_directory, "circle_loop.py")

# Function to run a Python script
def run_script(script_path):
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_path}: {e}")

# Run the scripts
run_script(welcome_screen_script)
time.sleep(5)
run_script(circle_loop)
