# Importing the library
import pygame

# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((400, 300))

# Initialing Color
color = (255, 0, 0)

# Drawing Rectangle
is_running = True

pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60))
#pygame.display.flip()

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False