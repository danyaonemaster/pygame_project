import pygame
import random
import pygame_project.config as config
from pygame_project.utils import scale_pos, scale_size


class Enemy(pygame.sprite.Sprite):
    """
    Base Enemy class.

    This class defines shared logic for all enemies:
    - Animation handling
    - Gravity and ground logic
    - Respawn system
    - State & direction control

    Child classes (e.g. Slime, Bat, Skeleton) should override:
    - move()
    - attack()
    - behavior()
    """

    def __init__(self, xy_pairs, size_scale, enemy_animations):
        super().__init__()

        # ---------------- BASIC STATE ----------------
        self.alive = True          # Is enemy alive (health > 0)
        self.active = True         # Is enemy currently active in the world
        self.state = config.STATE_IDLE
        self.side = config.MOVE_DIRECTION_LEFT

        # ---------------- ANIMATIONS ----------------
        self.animations = {}

        # Load animations from provided dictionary
        for name, paths in enemy_animations.items():
            frames = self.load_animation(paths, scale_size(size_scale))
            self.animations[name] = {
                config.MOVE_DIRECTION_RIGHT: frames,
                config.MOVE_DIRECTION_LEFT: [
                    pygame.transform.flip(f, True, False) for f in frames
                ]
            }

        # ---------------- ANIMATION CONTROL ----------------
        self.frame = 0
        self.animation_speed = 0.15

        self.image = self.animations[self.state][config.MOVE_DIRECTION_RIGHT][self.frame]
        self.side = config.MOVE_DIRECTION_LEFT

        # ---------------- GRAPHICS & COLLISION ----------------
        self.rect = self.image.get_rect(midbottom=scale_pos(xy_pairs))
        self.mask = pygame.mask.from_surface(self.image)

        # ---------------- RESPAWN POSITION ----------------
        # Used to reset enemy after death
        self.start_pos = scale_pos(xy_pairs)

        # ---------------- GRAVITY / PHYSICS ----------------
        self.gravity = 0
        self.gravity_speed = config.HEIGHT * 0.00075

        self.is_jumping = False
        self.on_ground = True

        # ---------------- RESPAWN LOGIC ----------------
        self.respawn_time = 0
        self.respawn_delay = (2000, 5000)  # respawn after 2–5 seconds

        # ---------------- DROP LOGIC (optional) ----------------
        # self.drop_chance = 0.02

    # ==================================================
    # GENERAL FUNCTIONS
    # ==================================================

    @staticmethod
    def load_animation(paths, scale):
        """
        Load and scale animation frames.
        """
        frames = []
        for path in paths:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, scale)
            frames.append(image)
        return frames

    def animate(self, anim):
        """
        Play animation based on current direction.
        """
        frames = anim[self.side]

        self.frame += self.animation_speed
        if self.frame >= len(frames):
            self.frame = 0

        self.image = frames[int(self.frame)]
        self.mask = pygame.mask.from_surface(self.image)

    def set_state(self, new_state):
        """
        Safely change animation state.
        """
        if self.state != new_state:
            self.state = new_state
            self.frame = 0

    # ==================================================
    # PHYSICS
    # ==================================================

    def apply_gravity(self):
        """
        Simple gravity logic.
        Enemy falls down until reaching its start Y position.
        """
        self.gravity += self.gravity_speed
        self.rect.bottom += self.gravity

        # Stop falling at initial ground level
        if self.rect.bottom >= self.start_pos[1]:
            self.rect.bottom = self.start_pos[1]
            self.gravity = 0
            self.is_jumping = False
            self.on_ground = True
        else:
            self.on_ground = False

    # ==================================================
    # LIFE CYCLE
    # ==================================================

    def die(self, current_time):
        """
        Kill enemy and schedule respawn.
        """
        self.active = False
        self.alive = False
        self.respawn_time = current_time + random.randint(*self.respawn_delay)

    def respawn(self, current_time):
        """
        Respawn enemy after delay.
        """
        if not self.active and current_time >= self.respawn_time:
            self.rect.midbottom = self.start_pos
            self.alive = True
            self.active = True
            self.gravity = 0

    # ==================================================
    # METHODS FOR CHILD CLASSES
    # ==================================================

    def move(self, current_time):
        """
        Enemy movement logic.
        Override in child class.
        """
        pass

    def attack(self, player):
        """
        Enemy attack logic.
        Override in child class.
        """
        pass

    def behavior(self, current_time):
        """
        Base behavior logic.
        Can be extended in child classes.
        """
        self.move(current_time)

    # ==================================================
    # MAIN UPDATE
    # ==================================================

    def update(self, current_time):
        """
        Update enemy behavior every frame.
        """
        if not self.active:
            self.respawn(current_time)
            return
