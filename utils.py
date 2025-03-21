"""Utility functions for the game."""

import pygame

from constants import BLACK, screen

sprites = pygame.image.load("assets/sprite.png")


def draw_grid():
    for x in range(0, screen.get_width(), 20):
        pygame.draw.line(screen, BLACK, (x, 0), (x, screen.get_height()))
    for y in range(0, screen.get_height(), 20):
        pygame.draw.line(screen, BLACK, (0, y), (screen.get_width(), y))


def get_sprite(sheet: pygame.Surface, x: int, y: int, width: int, height: int):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite
