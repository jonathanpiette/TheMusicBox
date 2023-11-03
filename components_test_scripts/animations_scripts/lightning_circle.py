import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Python Animation")

# Set up the colors
bg_color = (42, 40, 38)
stroke_color = (230, 230, 230)
shadow_color = (int(bg_color[0] * 1.15), int(bg_color[1] * 1.15), int(bg_color[2] * 1.15))

# Set up the circle parameters
N = 360
n = 7
R = 165
t = 0

def ease(q):
    return 3 * q * q - 2 * q * q * q

def draw_circle(q, offset_x, offset_y, color, stroke_weight):
    points = []
    for i in range(N):
        th = i * 2 * math.pi / N
        os = math.cos(th - 2 * math.pi * t)
        os = (os + 1) / 2  # Map from -1,1 to 0,1
        os = 0.125 * os ** 2.75
        r = R * (1 + os * math.cos(n * th + 1.5 * math.pi * t + q))
        x = r * math.sin(th) + offset_x
        y = -r * math.cos(th) + offset_y
        points.append((x, y))
    pygame.draw.lines(screen, color, True, points, stroke_weight)

def draw_circles(offset_x, offset_y):
    draw_circle(0, offset_x + 2, offset_y + 3, shadow_color, 8)
    draw_circle(math.pi, offset_x + 2, offset_y + 3, shadow_color, 8)
    draw_circle(0, offset_x, offset_y, stroke_color, 6)
    draw_circle(math.pi, offset_x, offset_y, stroke_color, 6)

def main():
    global t
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(bg_color)

        # Update time for automatic rotation
        t += 0.005
        if t > 1:
            t = 0

        # Draw the circles
        draw_circles(width / 2, height / 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
