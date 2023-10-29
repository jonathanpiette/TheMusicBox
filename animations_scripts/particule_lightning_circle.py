import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Merged Animation")

# Set up the colors
bg_color = (42, 40, 38)
stroke_color = (230, 230, 230)
shadow_color = (int(bg_color[0] * 1.15), int(bg_color[1] * 1.15), int(bg_color[2] * 1.15))
white = (255, 255, 255)

# Set up the circle parameters
N = 360
n = 7
R = 165
t = 0

# Set up the particle parameters
particle_radius = 2
particle_speed = 1
particles_per_frame = 2
max_distance = math.hypot(width // 2, height // 2)

# Set up the invisible circle parameters
invisible_circle_radius = R + 20
circle_center = (width // 2, height // 2)
circle_edge_distance_variation = 20  # Variable distance from the circle edge

particles = []

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

def create_particle():
    angle = random.uniform(0, 2 * math.pi)
    dx = math.cos(angle)
    dy = math.sin(angle)
    distance_from_edge = random.uniform(-circle_edge_distance_variation, circle_edge_distance_variation)
    x = circle_center[0] + (invisible_circle_radius + distance_from_edge) * dx
    y = circle_center[1] + (invisible_circle_radius + distance_from_edge) * dy
    life = random.uniform(max_distance / 2, max_distance) / particle_speed
    particles.append([x, y, dx, dy, 1.0, life, life])  # x, y, dx, dy, alpha, life, initial_life

def draw_particles():
    for particle in particles[:]:
        particle[0] += particle[2] * particle_speed  # Move in x direction
        particle[1] += particle[3] * particle_speed  # Move in y direction
        particle[5] -= 1  # Decrease life
        if particle[5] > 0:
            particle[4] = particle[5] / particle[6]  # Calculate alpha based on remaining life
            color = (white[0], white[1], white[2], int(particle[4] * 255))
            surface = pygame.Surface((particle_radius * 2, particle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (particle_radius, particle_radius), particle_radius)
            screen.blit(surface, (int(particle[0] - particle_radius), int(particle[1] - particle_radius)))
        else:
            particles.remove(particle)

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

        # Create and draw particles
        for _ in range(particles_per_frame):
            create_particle()
        draw_particles()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
