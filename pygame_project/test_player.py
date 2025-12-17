import pygame
from pygame_project.photos.knight.animations import *
import pygame_project.config as config


class Player(pygame.sprite.Sprite):
    def __init__(self, xy_pairs, scale_size):
        super().__init__()

        self.idle_frames = [
            pygame.transform.scale(
                pygame.image.load(i).convert_alpha(),
                scale_size
            ) for i in idle_anim
        ]

        self.run_frames =[
            pygame.transform.scale(
                pygame.image.load(i).convert_alpha(),
                scale_size
            ) for i in run_anim
        ]


        self.flipped_run = [
            pygame.transform.flip(frame, True, False)
            for frame in self.run_frames
        ]

        self.flipped_idle = [
            pygame.transform.flip(frame, True, False)
            for frame in self.idle_frames
        ]

        # ---- Анимация ----
        self.frame = 0
        self.animation_speed = 0.15
        self.image = self.idle_frames[self.frame]

        self.original_image = self.image
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        # ---- Физика ----
        self.rect = self.image.get_rect(midbottom=xy_pairs)
        self.mask = pygame.mask.from_surface(self.image)

        self.bottom = self.rect.bottom
        self.gravity = 0
        self.jumped = False
        self.moves = False
        self.side = 1
        self.last_move_time = 0

        self.move_speed = config.WIDTH * 0.005
        self.jump_strength = -config.HEIGHT * 0.032
        self.gravity_speed = config.HEIGHT * 0.0015

    # ---------- Гравитация ----------
    def apply_gravity(self):
        self.gravity += self.gravity_speed
        self.rect.bottom += self.gravity

        if self.rect.bottom >= self.bottom:
            self.rect.bottom = self.bottom
            self.gravity = 0
            self.jumped = False

    def handle_input(self, current_time):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.move_speed
            self.moves = True
            self.side = 1
            self.animate_run(self.run_frames)
            self.last_move_time = current_time

        elif keys[pygame.K_a]:
            self.rect.x -= self.move_speed
            self.moves = True
            self.side = 0
            self.animate_run(self.flipped_run)
            self.last_move_time = current_time


        if current_time - self.last_move_time > 200:
            self.moves = False
            self.last_move_time = 0



    # ---------- Анимация Idle ----------
    def animate_idle(self):
        self.frame += self.animation_speed
        if self.frame >= len(self.idle_frames):
            self.frame = 0

        if self.side == 1:
            self.image = self.idle_frames[int(self.frame)]
        else:
            self.image = self.flipped_idle[int(self.frame)]

        self.mask = pygame.mask.from_surface(self.image)  # если нужна маска

    def animate_run(self, run):
        self.frame += self.animation_speed
        if self.frame >= len(run):
            self.frame = 0

        self.image = run[int(self.frame)]
        self.mask = pygame.mask.from_surface(self.image)

    # ---------- Update ----------
    def update(self, event_list, current_time):
        self.apply_gravity()
        self.handle_input(current_time)

        if not self.moves:
            self.animate_idle()


    # ---------- Reset ----------
    def reset_game(self, pos):
        self.rect.midbottom = pos
        self.gravity = 0
        self.jumped = False
