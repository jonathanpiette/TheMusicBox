import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiple Waving Circles with Particles")

# Set up the colors
BG_COLOR = (42, 40, 38)
STROKE_COLOR = (230, 230, 230)
WHITE = (255, 255, 255)

# Set up the circle parameters
NUM_CIRCLES = 5  # Number of circles
N = 720  # Number of points for the circle
R = 165
t = 0

# Set up the particle parameters
PARTICLE_RADIUS = 2
PARTICLES_PER_FRAME = 1
MAX_DISTANCE = math.hypot(WIDTH // 2, HEIGHT // 2)
MIN_PARTICLE_SPEED = 0.5  # Minimum speed of particles
MAX_PARTICLE_SPEED = 2.0  # Maximum speed of particles

# Set up the invisible circle parameters
INVISIBLE_CIRCLE_RADIUS = R + 20
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)
CIRCLE_EDGE_DISTANCE_VARIATION = 20

particles = []

def create_particle():
    angle = random.uniform(0, 2 * math.pi)
    dx = math.cos(angle)
    dy = math.sin(angle)
    distance_from_edge = random.uniform(-CIRCLE_EDGE_DISTANCE_VARIATION, CIRCLE_EDGE_DISTANCE_VARIATION)
    x = CIRCLE_CENTER[0] + (INVISIBLE_CIRCLE_RADIUS + distance_from_edge) * dx
    y = CIRCLE_CENTER[1] + (INVISIBLE_CIRCLE_RADIUS + distance_from_edge) * dy
    particle_speed = random.uniform(MIN_PARTICLE_SPEED, MAX_PARTICLE_SPEED)
    life = random.uniform(MAX_DISTANCE / 2, MAX_DISTANCE) / particle_speed
    particles.append([x, y, dx, dy, 1.0, life, life, particle_speed])

def draw_particles():
    for particle in particles[:]:
        particle[0] += particle[2] * particle[7]
        particle[1] += particle[3] * particle[7]
        particle[5] -= 1
        if particle[5] > 0:
            particle[4] = particle[5] / particle[6]
            color = (*WHITE, int(particle[4] * 255))
            surface = pygame.Surface((PARTICLE_RADIUS * 2, PARTICLE_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, color, (PARTICLE_RADIUS, PARTICLE_RADIUS), PARTICLE_RADIUS)
            screen.blit(surface, (int(particle[0] - PARTICLE_RADIUS), int(particle[1] - PARTICLE_RADIUS)))
        else:
            particles.remove(particle)

def draw_circle(radius, offset_x, offset_y, color, stroke_weight, wave_amplitude, wave_frequency, wave_speed, direction):
    points = [(radius * math.sin(th) + offset_x, -radius * math.cos(th) + offset_y + math.sin(wave_frequency * th + wave_speed * t * direction) * wave_amplitude * radius) for th in (i * 2 * math.pi / N for i in range(N))]
    pygame.draw.lines(screen, color, True, points, stroke_weight)

def draw_circles(offset_x, offset_y):
    wave_amplitude = 0.05  # Constant wave amplitude for each circle
    wave_frequency = 3  # Constant wave frequency for each circle
    for i in range(NUM_CIRCLES):
        wave_speed = 5 + i  # Varying wave speed for each circle
        direction = 1 if i % 2 == 0 else -1  # Alternate directions for each circle
        draw_circle(R, offset_x, offset_y, STROKE_COLOR, 2, wave_amplitude, wave_frequency, wave_speed, direction)

def main():
    global t
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        t += 0.005
        if t > 1:
            t = 0

        draw_circles(WIDTH / 2, HEIGHT / 2)

        for _ in range(PARTICLES_PER_FRAME):
            create_particle()
        draw_particles()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
