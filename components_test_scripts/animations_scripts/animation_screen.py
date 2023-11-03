#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch9
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

sys.path.append("..")

# Generate list of file names
frame_files = [f"animation_frame{str(i).zfill(3)}.png" for i in range(45)]

try:
    # Initialize display
    disp = LCD_1inch9.LCD_1inch9()
    disp.Init()
    disp.clear()

    padding = 80  # Set the desired padding here

    while True:  # Loop forever
        for frame_file in frame_files:
            # Construct the full path to the image file
            image_path = os.path.join("animation", frame_file)
            
            # Open the image file
            image = Image.open(image_path)
            
            # Convert image to RGB (if not already in this mode)
            image = image.convert("RGB")
            
            # Calculate new dimensions to maintain aspect ratio
            aspect_ratio = image.width / image.height
            new_width = disp.height - 2 * padding
            new_height = int(new_width / aspect_ratio)
            
            # Resize image to new dimensions
            image = image.resize((new_width, new_height))
            
            # Create a background image with the dimensions of the screen
            background = Image.new("RGB", (disp.height, disp.width), "BLACK")
            
            # Calculate position to paste the image onto the background
            x = (disp.height - new_width) // 2
            y = (disp.width - new_height) // 2
            
            # Paste the image onto the background
            background.paste(image, (x, y))
            
            # Display the image
            disp.ShowImage(background)
            
            # Wait for a short period of time
            time.sleep(0.1)  # Sleep time for 24 frames per second

finally:
    disp.module_exit()
    logging.info("Animation ended")
