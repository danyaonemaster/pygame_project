import pygame
from pygame_project.photos.knight.animations import *
import pygame_project.config as config


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite: str, xy_pairs, scale_size):
        super().__init__()

        # --- Настройки ---
        self.image = [pygame.transform.scale(
            pygame.image.load(i),
            scale_size
        ).convert_alpha() for i in idle_anim]
        self.rect = [_.get_rect(midbottom=xy_pairs) for _ in self.image]
        self.mask = [pygame.mask.from_surface(i) for i in self.image]

        self.bottom = self.rect.bottom

        self.moved = False
        self.gravity = 0
        self.jumped = False
        self.move_speed = config.WIDTH * 0.005
        self.jump_strength = -config.HEIGHT * 0.032
        self.gravity_speed = config.HEIGHT * 0.0015
        self.frame = 0

    def apply_gravity(self):
        self.gravity += self.gravity_speed
        self.rect.bottom += self.gravity

        if self.rect.bottom >= self.bottom:
            self.rect.bottom = self.bottom
            self.gravity = 0
            self.jumped = False

    # def handle_input(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_d]:
    #         self.rect.x += self.move_speed
    #     if keys[pygame.K_a]:
    #         self.rect.x -= self.move_speed

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.move_speed
        if keys[pygame.K_a]:
            self.rect.x -= self.move_speed

    def jump(self, event):
        if self.jumped:
            return

        # Прыжок пробелом
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.gravity = self.jump_strength
            self.jumped = True

    def update(self, event_list):
        for event in event_list:
            self.jump(event)
            pass
        self.apply_gravity()
        self.handle_input()

    def reset_game(self, pos):
        self.rect.midbottom = pos
        self.gravity = 0
        self.jumped = False
