import pygame
import random
import pygame_project.config as config
from pygame_project.utils import scale_pos, scale_size


class Enemy(pygame.sprite.Sprite):
    def __init__(self, xy_pairs, size_scale, enemy_animations):
        super().__init__()

        # state
        self.alive = True
        self.active = True
        self.state = config.STATE_IDLE
        self.side = config.MOVE_DIRECTION_LEFT
        self.animations = {}

        for name, paths in enemy_animations.items():
            frames = self.load_animation(paths, scale_size(size_scale))
            self.animations[name] = {
                config.MOVE_DIRECTION_RIGHT: frames,
                config.MOVE_DIRECTION_LEFT: [pygame.transform.flip(f, True, False) for f in frames]
            }

        # ---- Animation ----
        self.frame = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.state][config.MOVE_DIRECTION_RIGHT][self.frame]
        self.side = config.MOVE_DIRECTION_LEFT

        # graphic
        self.image = self.animations[self.state][config.MOVE_DIRECTION_RIGHT][self.frame]
        self.rect = self.image.get_rect(midbottom=scale_pos(xy_pairs))
        self.mask = pygame.mask.from_surface(self.image)

        # respawn position
        self.start_pos = scale_pos(xy_pairs)

        # gravity (can be turned off in the child class)
        self.gravity = 0
        self.gravity_speed = config.HEIGHT * 0.00075
        self.is_jumping = False
        self.on_ground = True

        # respawn
        self.respawn_time = 0
        self.respawn_delay = (2000, 5000)  # по умолчанию 2–5 сек

        # # drop chance
        # self.drop_chance = 0.02

    # ------------------------------
    # General functions
    # ------------------------------

    @staticmethod
    def load_animation(paths, scale):
        frames = []
        for path in paths:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, scale)
            frames.append(image)

        return frames

    def animate(self, anim):
        frames = anim[self.side]

        self.frame += self.animation_speed
        if self.frame >= len(frames):
            self.frame = 0

        self.image = frames[int(self.frame)]
        self.mask = pygame.mask.from_surface(self.image)

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame = 0

    def apply_gravity(self):
        self.gravity += self.gravity_speed
        self.rect.bottom += self.gravity

        if self.rect.bottom >= self.start_pos[1]:
            self.rect.bottom = self.start_pos[1]
            self.gravity = 0
            self.is_jumping = False
            self.on_ground = True
        else:
            self.on_ground = False

    def die(self, current_time):
        self.active = False
        self.alive = False
        self.respawn_time = current_time + random.randint(*self.respawn_delay)

    def respawn(self, current_time):
        if not self.active and current_time >= self.respawn_time:
            self.rect.midbottom = self.start_pos
            self.alive = True
            self.active = True
            self.gravity = 0

    # ------------------------------
    # Methods that inheritors OVERRIDE
    # ------------------------------

    def move(self, current_time):
        """Override in child class"""
        pass

    def attack(self, player):
        """Override in child"""
        pass

    def behavior(self, current_time):
        """The Enemy's Basic Logic"""
        self.move(current_time)

    # ------------------------------
    #  Main update
    # ------------------------------

    def update(self, current_time):
        self.behavior(current_time)
