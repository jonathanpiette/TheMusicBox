import os
import sys
import time
import logging
import spidev as SPI
import pygame
import math
import random
from PIL import Image
sys.path.append("..")
from lib import LCD_1inch9

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

# Initialize Pygame for animation
pygame.init()
width, height = 170, 320  # Set to your LCD's resolution
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Rotating Circles")

# Initialize display
disp = LCD_1inch9.LCD_1inch9()
disp.Init()
disp.clear()

# Circle settings
num_circles = 5
circles = []
for _ in range(num_circles):
    radius = random.randint(20, 120)  # Adjusted for smaller screen
    thickness = random.randint(2, 10)  # Adjusted for smaller screen
    speed = random.uniform(0.001, 0.01)  # Slower speed for smoother animation
    segments = random.randint(1, 5)
    direction = 1 if random.random() > 0.2 else -1  # 20% chance to rotate in the opposite direction
    circle = {'radius': radius, 'thickness': thickness, 'speed': speed, 'segments': segments, 'direction': direction}
    circles.append(circle)

# Sort circles by radius
circles = sorted(circles, key=lambda x: x['radius'], reverse=True)

# Define colors
colors = []
for i in range(num_circles):
    gray_value = 205 + (i * (50 // num_circles))  # Range from light gray to white
    colors.append((gray_value, gray_value, gray_value))

# Main loop
running = True
angle = 0
try:
    while True:  # Infinite loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Draw circles
        for i, circle in enumerate(circles):
            perimeter = 2 * math.pi * circle['radius']
            segment_length = 0.3 * perimeter / circle['segments']  # 30% of the perimeter
            space_length = (0.7 * perimeter) / (circle['segments'] - 1) if circle['segments'] > 4 else 0

            for j in range(circle['segments']):
                start_angle = angle * (i + 1) * circle['direction'] + (j * (segment_length + space_length) / circle['radius'])
                end_angle = start_angle + (segment_length / circle['radius'])
                for k in range(circle['thickness']):
                    offset_radius = circle['radius'] - k
                    pygame.draw.arc(screen, colors[i], (width // 2 - offset_radius, height // 2 - offset_radius, 2 * offset_radius, 2 * offset_radius), start_angle, end_angle, 1)

        # Capture Pygame screen
        pygame.display.flip()
        pygame_surface = pygame.display.get_surface()
        pil_image = Image.frombytes('RGB', pygame_surface.get_size(), pygame.image.tostring(pygame_surface, 'RGB'))

        # Display on LCD
        disp.ShowImage(pil_image)

        # Control the animation speed
        angle += 0.005
        pygame.time.Clock().tick(60)

finally:
    disp.module_exit()
    logging.info("Animation ended")
    pygame.quit()
    sys.exit()
