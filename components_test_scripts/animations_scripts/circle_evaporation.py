import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Plasma Lightning Circle")

# Set up the colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the lightning parameters
num_segments = 50
circle_radius = 150
angle_change = 50  # Smaller angle change for smoother movement

def draw_lightning_circle(x, y, radius, segments):
    points = []
    angle = 0
    angle_increment = 180 / segments

    for i in range(segments + 1):  # +1 to close the circle
        x2 = x + radius * math.cos(math.radians(angle))
        y2 = y + radius * math.sin(math.radians(angle))
        points.append((x2, y2))
        angle += angle_increment + random.uniform(-angle_change, angle_change)

    pygame.draw.lines(screen, white, False, points, 2)

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(black)

        # Draw the lightning circle
        start_x = width // 2
        start_y = height // 2
        draw_lightning_circle(start_x, start_y, circle_radius, num_segments)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
