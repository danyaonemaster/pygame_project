import pygame
import os

class Tileset(pygame.sprite.Sprite):
    def __init__(self, pos, image, group):
        super().__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

