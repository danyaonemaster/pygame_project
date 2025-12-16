from pygame_project.assets.enemy import Enemy
import pygame
import pygame_project.config as config
import random

class Bat(Enemy):
    def __init__(self, pos, size):
        super().__init__("photos/bat.png", pos, size)

        self.original_image = self.image

        self.flipped_image = pygame.transform.flip(self.image, True, False)

        # --- Настройки ---
        self.bottom = self.rect.bottom

        self.is_target = False
        self.target_x = 0
        self.target_y = 0


    def move(self, target):
        if not self.is_target:
            self.target_x = target.rect.x
            self.target_y = target.rect.y



    def restart(self):
        self.rect.midbottom = self.start_pos
        self.is_target = True
        self.target_x = 0
        self.target_y = 0

