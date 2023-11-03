import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Falling Particles")

# Set up the colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the particle parameters
particle_radius = 2
particle_speed = 1
particles_per_frame = 2
max_distance = math.hypot(width // 2, height // 2)

# Set up the circle parameters
circle_radius = 100
circle_center = (width // 2, height // 2)
circle_edge_distance_variation = 20  # Variable distance from the circle edge

particles = []

def create_particle():
    angle = random.uniform(0, 2 * math.pi)
    dx = math.cos(angle)
    dy = math.sin(angle)
    distance_from_edge = random.uniform(-circle_edge_distance_variation, circle_edge_distance_variation)
    x = circle_center[0] + (circle_radius + distance_from_edge) * dx
    y = circle_center[1] + (circle_radius + distance_from_edge) * dy
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
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(black)
        pygame.draw.circle(screen, black, circle_center, circle_radius)

        for _ in range(particles_per_frame):
            create_particle()
        draw_particles()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
