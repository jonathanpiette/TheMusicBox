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
num_segments = 100
circle_radius = 150
angle_change = 20
particle_radius = 2
num_particles = 500

particles = []

def create_particles(x, y, radius, segments):
    angle = 0
    angle_increment = 360 / segments

    for _ in range(segments):
        angle_radians = math.radians(angle)
        x2 = x + radius * math.cos(angle_radians)
        y2 = y + radius * math.sin(angle_radians)
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        life = random.randint(2, 5)
        particles.append([x2, y2, dx, dy, life])
        angle += angle_increment

def draw_lightning_circle(x, y, radius, segments):
    points = []
    angle = 0
    angle_increment = 360 / segments

    for i in range(segments + 1):  # +1 to close the circle
        angle_radians = math.radians(angle)
        offset = random.uniform(-angle_change, angle_change)
        x2 = x + (radius + offset) * math.cos(angle_radians)
        y2 = y + (radius + offset) * math.sin(angle_radians)
        points.append((x2, y2))
        angle += angle_increment

    pygame.draw.lines(screen, white, False, points, 2)

def draw_particles():
    for particle in particles[:]:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 0.05  # Decrease the life of the particle
        if particle[4] > 0:
            pygame.draw.circle(screen, white, (int(particle[0]), int(particle[1])), particle_radius)
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

        # Draw the lightning circle
        start_x = width // 2
        start_y = height // 2
        draw_lightning_circle(start_x, start_y, circle_radius, num_segments)
        draw_particles()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    create_particles(width // 2, height // 2, circle_radius, num_particles)
    main()
