import pygame
import math

# Setup
clock = pygame.time.Clock()
turn_angle_deg = 3
turn = math.radians(180-turn_angle_deg)
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Vacuum Robot Coverage Simulation")

# Robot state
x, y = 250.0, 250.0
dx, dy = -1.0, 0.0
just_collided = False

def rotate_vector(dx, dy, theta):
    new_dx = dx * math.cos(theta) - dy * math.sin(theta)
    new_dy = dx * math.sin(theta) + dy * math.cos(theta)
    return new_dx, new_dy

# Main loop
running = True
screen.fill((180, 255, 180))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x += dx
    y += dy

    # Check collision
    hit_wall = False
    if x >= 500 or x <= 0 or y >= 500 or y <= 0:
        hit_wall = True

    if hit_wall and not just_collided:
        dx, dy = rotate_vector(dx, dy, turn)
        just_collided = True
        # Move slightly inward to avoid immediate repeated collision
        x = max(0, min(500, x))
        y = max(0, min(500, y))
    elif not hit_wall:
        just_collided = False

    pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 15)
    pygame.display.update()
    clock.tick(3000)

pygame.quit()


