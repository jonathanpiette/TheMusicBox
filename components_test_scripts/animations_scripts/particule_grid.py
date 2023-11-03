import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Random Particles")

# Set up the colors
bg_color = (42, 40, 38)

# Define a list of 20 tones of orange to white
color_palette = color_palette = [
    (255, 105, 98),   # Pastel Red
    (255, 135, 118),  # Congo Pink
    (255, 176, 146),  # Macaroni And Cheese
    (255, 224, 142),  # Flavescent
    (255, 208, 80),   # Mustard
    (255, 179, 70)    # Pastel Orange
]

# Particle settings
grid_size = 8
cell_size = min(width, height) // grid_size
particle_lifetime = 7  # seconds
spawn_rate = 0.5  # seconds

# Store the particles
particles = {}

def generate_color_from_palette():
    return random.choice(color_palette)

def spawn_particle():
    empty_cells = [(x, y) for x in range(grid_size) for y in range(grid_size) if (x, y) not in particles]
    if not empty_cells:
        return
    
    x, y = random.choice(empty_cells)
    color = generate_color_from_palette()
    timestamp = time.time()
    particles[(x, y)] = {'color': color, 'timestamp': timestamp}

def draw_particles():
    current_time = time.time()
    particles_to_remove = []
    for (x, y), particle in particles.items():
        elapsed_time = current_time - particle['timestamp']
        if elapsed_time < particle_lifetime:
            # Calculate alpha based on elapsed time
            alpha = int((1 - elapsed_time / particle_lifetime) * 255)
            draw_color = particle['color']
            square = pygame.Surface((cell_size, cell_size))
            square.fill(draw_color)
            square.set_alpha(alpha)
            screen.blit(square, (x * cell_size, y * cell_size))
        else:
            particles_to_remove.append((x, y))
    
    # Remove particles that have finished fading
    for pos in particles_to_remove:
        del particles[pos]

def main():
    running = True
    clock = pygame.time.Clock()
    last_spawn_time = 0

    while running:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(bg_color)

        # Spawn new particle based on spawn rate
        if current_time - last_spawn_time > spawn_rate:
            spawn_particle()
            last_spawn_time = current_time

        # Draw and update particles
        draw_particles()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
