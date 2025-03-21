"""Constants for the game."""

import pygame

DEVELOPMENT = False

WIDTH, HEIGHT = 1000, 300
INITIAL_VEL = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

GROUND = HEIGHT

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")
