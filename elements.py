"""This module contains the classes for the game elements."""

import pygame

from constants import BLACK, DEVELOPMENT, GROUND, screen
from random_variables import generate_num_trees, generate_cloud_height
from utils import get_sprite, sprites


class Dino:
    """Visual representation of the dinosaur."""

    GRAVITY = 9.8
    JUMP_HEIGHT = 75

    def __init__(self):
        self.x = 0
        self.y = GROUND
        self.vel_y = 0
        self.on_ground = True
        self.original_frames = [
            get_sprite(sprites, 1514 + i * 88, 0, 88, 100) for i in range(3)
        ]
        scale_factor = 0.8
        self.frames = [
            pygame.transform.scale(
                frame,
                (
                    int(frame.get_width() * scale_factor),
                    int(frame.get_height() * scale_factor),
                ),
            )
            for frame in self.original_frames
        ]
        self.current_frame = 0
        self.running_frame_count = 2
        self.height = self.frames[0].get_height()

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.JUMP_HEIGHT
            self.on_ground = False

    def update(self, is_game_over: bool = False):
        if is_game_over:
            self.current_frame = 2
            return
        self.vel_y += self.GRAVITY
        self.y += self.vel_y
        if self.y >= GROUND:
            self.y = GROUND
            self.on_ground = True

        self.current_frame = (self.current_frame + 1) % self.running_frame_count

    def draw(self):
        current_image = self.frames[self.current_frame]
        screen.blit(current_image, (self.x, self.y - current_image.get_height()))
        if DEVELOPMENT:
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    self.x,
                    self.y - current_image.get_height(),
                    current_image.get_width(),
                    current_image.get_height(),
                ),
                1,
            )


class Floor:
    """Visual representation of the floor."""

    def __init__(self, speed: float):
        self.floor_img = get_sprite(sprites, 2, 104, 2400, 26)
        self.x = 0
        self.y = GROUND - self.floor_img.get_height()
        self.image = self.floor_img
        self.speed = speed

    def update(self):
        self.x -= self.speed
        if self.x < -self.image.get_width():
            self.x = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        screen.blit(self.image, (self.x + self.image.get_width(), self.y))


class Obstacle:
    """Base class for obstacles."""

    def __init__(
        self,
        sprite_x: int,
        sprite_y: int,
        sprite_max_elements: int,
        width: int,
        height: int,
        speed: float,
    ):
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.sprite_max_elements = sprite_max_elements
        self.width = width
        self.height = height
        self.speed = speed
        self.reset_tree()

    def reset_tree(self):
        num_trees = generate_num_trees(self.sprite_max_elements)
        offset = num_trees * self.width
        self.image = get_sprite(
            sprites, self.sprite_x, self.sprite_y, offset, self.height
        )
        self.x = screen.get_width()
        self.y = GROUND - self.image.get_height()

    def update(self):
        self.x -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        current_image = self.image
        if DEVELOPMENT:
            pygame.draw.rect(
                screen,
                BLACK,
                (self.x, self.y, current_image.get_width(), current_image.get_height()),
                1,
            )

    def get_rect(self):
        return pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height()
        )

    def get_next_rect(self):
        return pygame.Rect(
            self.x - self.speed, self.y, self.image.get_width(), self.image.get_height()
        )


class BigTree(Obstacle):
    """Big tree obstacle."""

    def __init__(self, speed: float):
        super().__init__(650, 0, 4, 50, 100, speed)


class SmallTree(Obstacle):
    """Small tree obstacle."""

    def __init__(self, speed: float):
        super().__init__(446, 0, 6, 34, 80, speed)


class Cloud:
    """Visual representation of a cloud."""

    def __init__(self, speed: float):
        self.image = get_sprite(sprites, 170, 0, 90, 54)
        self.x = screen.get_width()
        self.y = generate_cloud_height(screen.get_height())
        self.speed = speed // 2

    def update(self):
        self.x -= self.speed
        if self.x + self.image.get_width() < 0:
            self.reset_position()

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        if DEVELOPMENT:
            pygame.draw.rect(
                screen,
                BLACK,
                (
                    self.x,
                    self.y - self.image.get_height(),
                    self.image.get_width(),
                    self.image.get_height(),
                ),
                1,
            )

    def reset_position(self):
        """Reset the cloud to the right side of the screen with a new vertical position."""
        self.x = screen.get_width()
        self.y = screen.get_height() // 2


class GameOver:
    """Visual representation of the game over text."""

    def __init__(self):
        self.image = get_sprite(sprites, 953, 25, 380, 48)
        self.x = (screen.get_width() - self.image.get_width()) // 2
        self.y = (screen.get_height() - self.image.get_height()) // 2

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Restart:
    """Visual representation of the restart button."""

    def __init__(self):
        self.image = pygame.transform.scale(
            get_sprite(sprites, 0, 0, 75, 67), (75 // 2, 67 // 2)
        )
        self.x = (screen.get_width() - self.image.get_width()) // 2
        self.y = (screen.get_height() - self.image.get_height()) // 2 + 30

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
