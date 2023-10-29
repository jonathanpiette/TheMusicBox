import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multiple Waving Circles")

# Set up the colors
bg_color = (42, 40, 38)
stroke_color = (230, 230, 230)
white = (255, 255, 255)

# Set up the circle parameters
num_circles = 5  # Number of circles
N = 720  # Number of points for the circle
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
circle_edge_distance_variation = 20

particles = []

def create_particle():
    angle = random.uniform(0, 2 * math.pi)
    dx = math.cos(angle)
    dy = math.sin(angle)
    distance_from_edge = random.uniform(-circle_edge_distance_variation, circle_edge_distance_variation)
    x = circle_center[0] + (invisible_circle_radius + distance_from_edge) * dx
    y = circle_center[1] + (invisible_circle_radius + distance_from_edge) * dy
    life = random.uniform(max_distance / 2, max_distance) / particle_speed
    particles.append([x, y, dx, dy, 1.0, life, life])

def draw_particles():
    for particle in particles[:]:
        particle[0] += particle[2] * particle_speed
        particle[1] += particle[3] * particle_speed
        particle[5] -= 1
        if particle[5] > 0:
            particle[4] = particle[5] / particle[6]
            color = (white[0], white[1], white[2], int(particle[4] * 255))
            surface = pygame.Surface((particle_radius * 2, particle_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (particle_radius, particle_radius), particle_radius)
            screen.blit(surface, (int(particle[0] - particle_radius), int(particle[1] - particle_radius)))
        else:
            particles.remove(particle)

def draw_circle(radius, offset_x, offset_y, color, stroke_weight, wave_amplitude, wave_frequency, wave_speed, direction):
    points = []
    for i in range(N):
        th = i * 2 * math.pi / N
        wave = math.sin(wave_frequency * th + wave_speed * t * direction) * wave_amplitude
        r = radius * (1 + wave)
        x = r * math.sin(th) + offset_x
        y = -r * math.cos(th) + offset_y
        points.append((x, y))
    pygame.draw.lines(screen, color, True, points, stroke_weight)

def draw_circles(offset_x, offset_y):
    for i in range(num_circles):
        wave_amplitude = 0.05  # Constant wave amplitude for each circle
        wave_frequency = 3  # Constant wave frequency for each circle
        wave_speed = 5 + i  # Varying wave speed for each circle
        direction = 1 if i % 2 == 0 else -1  # Alternate directions for each circle
        draw_circle(R, offset_x, offset_y, stroke_color, 2, wave_amplitude, wave_frequency, wave_speed, direction)

def main():
    global t
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(bg_color)

        t += 0.005
        if t > 1:
            t = 0

        draw_circles(width / 2, height / 2)

        for _ in range(particles_per_frame):
            create_particle()
        draw_particles()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
