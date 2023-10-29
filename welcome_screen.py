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
logging.basicConfig(level = logging.DEBUG)
try:
    # Initialize display
    disp = LCD_1inch9.LCD_1inch9()
    disp.Init()
    disp.clear()

    # Define text and font
    text1 = "The Arthur's"
    text2 = "Music Box"
    font = ImageFont.truetype("Font/Font02.ttf", 55)

    # Create an image and draw object
    image = Image.new("RGB", (disp.height, disp.width), "BLACK")
    draw = ImageDraw.Draw(image)

    # Calculate text size and spacing using textbbox
    text1_bbox = draw.textbbox((0, 0), text1, font=font)
    text1_width = text1_bbox[2] - text1_bbox[0]
    text1_height = text1_bbox[3] - text1_bbox[1]

    text2_bbox = draw.textbbox((0, 0), text2, font=font)
    text2_width = text2_bbox[2] - text2_bbox[0]
    text2_height = text2_bbox[3] - text2_bbox[1]

    spacing = 20  # space between lines

    # Calculate total text height
    total_text_height = text1_height + text2_height + spacing

    # Calculate x and y coordinates
    x1 = (disp.height - text1_width) / 2
    y1 = (disp.width - total_text_height) / 2
    x2 = (disp.height - text2_width) / 2
    y2 = y1 + text1_height + spacing

    # Draw the text
    draw.text((x1, y1), text1, fill="WHITE", font=font)
    draw.text((x2, y2), text2, fill="WHITE", font=font)

    # Display the image
    while True:
        disp.ShowImage(image)
    
    # disp.module_exit()
    # logging.info("quit:")

except IOError as e:
    logging.info(e)    
    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
