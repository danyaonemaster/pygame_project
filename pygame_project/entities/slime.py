from pygame_project.assets.enemy import Enemy
import pygame
import pygame_project.config as config
import random

class Slime(Enemy):
    def __init__(self, pos, size):
        super().__init__("photos/slime.png", pos, size)

        # оригинал
        self.original_image = self.image

        # переворачиваем по горизонтали
        self.flipped_image = pygame.transform.flip(self.image, True, False)

        self.jump_strength = -12
        self.jump_cooldown = 0
        self.move_speed = config.HEIGHT * 0.006
        self.is_jumping = False


    def random_way(self):
        random_num = random.randint(0, 1)
        if random_num == 0:
            self.start_pos = [config.WIDTH * 0.065, self.start_pos[1]]
            self.move_speed = config.HEIGHT * 0.006
            self.image = self.original_image

        elif random_num == 1:
            self.start_pos = [config.WIDTH * 0.935, self.start_pos[1]]
            self.move_speed = -config.HEIGHT * 0.006
            self.image = self.flipped_image

        self.mask = pygame.mask.from_surface(self.image)

    def move(self, current_time):
        if self.rect.left > config.WIDTH * 1.065:
            self.random_way()
            self.rect.midbottom = self.start_pos

        elif self.rect.right < config.WIDTH * -0.065:
            self.random_way()
            self.rect.midbottom = self.start_pos


        if not self.is_jumping and self.jump_cooldown <= current_time:
            self.gravity = self.jump_strength
            self.jump_cooldown = current_time + random.randint(1000, 2000)
            self.is_jumping = True

        if self.is_jumping:
            self.rect.left += self.move_speed

        self.apply_gravity()


    def restart(self):
        self.rect.midbottom = self.start_pos
        self.is_jumping = False
        self.gravity = 0
        self.jump_cooldown = 0





