import pygame

import config
from assets.hp import Health
from config import STATE_IDLE, STATE_JUMP, STATE_RUN, STATE_FALL,STATE_ATK2 ,STATE_ATK_AIR ,STATE_ATK_RUN ,STATE_ATK1, MOVE_DIRECTION_RIGHT, MOVE_DIRECTION_LEFT


class Player(pygame.sprite.Sprite):

    def __init__(self, xy_pairs, scale_size):
        super().__init__()

        self.state = STATE_IDLE
        self.animations = {}

        for name, paths in config.K_ANIMATIONS.items():
            frames = self.load_animation(paths, scale_size)
            self.animations[name] = {
                MOVE_DIRECTION_RIGHT: frames,
                MOVE_DIRECTION_LEFT: [pygame.transform.flip(f, True, False) for f in frames]
            }

        # ---- Анимация ----
        self.frame = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.state][MOVE_DIRECTION_RIGHT][self.frame]

        self.invulnerable = False
        self.invuln_time = 1000

        # ---- Физика ----
        self.rect = self.image.get_rect(midbottom=xy_pairs)
        self.mask = pygame.mask.from_surface(self.image)

        self.bottom = self.rect.bottom
        self.health = Health(20)
        self.gravity = 0
        self.attack_stage = 0
        self.combo_queued = False
        self.jumped = False
        self.moves = False
        self.attacking = False
        self.side = 1
        self.last_move_time = 0

        self.move_speed = config.WIDTH * 0.005
        self.jump_strength = -config.HEIGHT * 0.032
        self.gravity_speed = config.HEIGHT * 0.0015

    def load_animation(self, paths, scale):
        frames = []
        for path in paths:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, scale)
            frames.append(image)

        return frames

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame = 0

    # ---------- Gravity ----------
    def apply_gravity(self):
        self.gravity += self.gravity_speed
        self.rect.bottom += self.gravity

        if self.rect.bottom >= self.bottom:
            self.rect.bottom = self.bottom
            self.gravity = 0
            self.jumped = False

    def handle_input(self, current_time):
        keys = pygame.key.get_pressed()

        if self.attacking:
            return

        if keys[pygame.K_d]:
            self.rect.x += self.move_speed
            self.set_state(STATE_RUN)
            self.moves = True
            self.side = 1
            self.animate_run(self.animations[self.state][MOVE_DIRECTION_RIGHT])
            self.last_move_time = current_time

        elif keys[pygame.K_a]:
            self.rect.x -= self.move_speed
            self.set_state(STATE_RUN)
            self.moves = True
            self.side = 0
            self.animate_run(self.animations[self.state][MOVE_DIRECTION_LEFT])
            self.last_move_time = current_time

        if self.jumped:
            if self.gravity < 0:
                self.set_state(STATE_JUMP)
                self.animate(self.animations[self.state])
            else:
                self.set_state(STATE_FALL)
                self.animate(self.animations[self.state])

        if keys[pygame.K_SPACE] and not self.jumped:
            self.gravity = self.jump_strength
            self.jumped = True

        if current_time - self.last_move_time > 200:
            self.moves = False
            self.last_move_time = 0



    def handle_attack_input(self):
        if self.attack_stage == 0:
            self.start_attack(1)

        elif self.attack_stage == 1:
            self.combo_queued = True

    # ---------- Анимации ----------
    def animate(self, anim, slow_index = 0.0):
        self.frame += self.animation_speed - slow_index
        if self.frame >= len(anim):
            self.frame = 0

        if self.side == 1:
            self.image = anim[MOVE_DIRECTION_RIGHT][int(self.frame)]
        else:
            self.image = anim[MOVE_DIRECTION_LEFT][int(self.frame)]

        self.mask = pygame.mask.from_surface(self.image)

    def animate_run(self, anim):
        self.frame += self.animation_speed
        if self.frame >= len(anim):
            self.frame = 0

        self.image = anim[int(self.frame)]
        self.mask = pygame.mask.from_surface(self.image)

    def start_attack(self, stage):
        self.attacking = True
        self.attack_stage = stage
        self.frame = 0

        if self.jumped:
            self.set_state(STATE_ATK_AIR)
            if self.attack_stage == 2:
                self.set_state(STATE_ATK2)

        elif self.moves:
            self.set_state(STATE_ATK_RUN)
            if self.attack_stage == 2:
                self.set_state(STATE_ATK2)

        else:
            self.set_state(STATE_ATK1)
            if self.attack_stage == 2:
                self.set_state(STATE_ATK2)

    def end_attack(self):
        self.attacking = False
        self.attack_stage = 0
        self.combo_queued = False
        self.set_state(STATE_IDLE)

    def animate_attack(self):
        anim = self.animations[self.state]
        self.frame += self.animation_speed

        combo_window = len(anim[MOVE_DIRECTION_RIGHT]) * 0.7

        if self.attack_stage == 1 and self.frame >= combo_window:
            if self.combo_queued:
                self.combo_queued = False
                self.start_attack(2)
                return

        if self.frame >= len(anim[MOVE_DIRECTION_RIGHT]):
            self.end_attack()
            return

        if self.side == 1:
            self.image = anim[MOVE_DIRECTION_RIGHT][int(self.frame)]
        else:
            self.image = anim[MOVE_DIRECTION_LEFT][int(self.frame)]

        self.mask = pygame.mask.from_surface(self.image)

    def take_damage(self, amount, current_time, pos):
        if self.invulnerable:
            return False

        self.health.damage(amount, current_time)
        self.invulnerable = True

        if self.health.is_dead():
            self.die(pos)
            return True

        return False

    # ---------- Update ----------
    def update(self, event_list, current_time):
        self.apply_gravity()
        self.handle_input(current_time)

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.handle_attack_input()

        if self.invulnerable:
            if current_time - self.health.last_hit >= self.invuln_time:
                self.invulnerable = False

        if self.attacking:
            self.animate_attack()
            return


        if not self.moves and not self.jumped and not self.attacking:
                self.set_state(STATE_IDLE)
                self.animate(self.animations[self.state], 0.1)



    def die(self, pos):
        self.reset(pos)
        config.GAME_ACTIVE = False


    def reset(self, pos):
        self.rect.midbottom = pos
        self.gravity = 0

        self.health.hp = self.health.max_hp
        self.invulnerable = False
        self.invuln_time = 1000

        self.state = STATE_IDLE
        self.frame = 0

        self.attack_stage = 0
        self.combo_queued = False
        self.attacking = False

        self.moves = False
        self.jumped = False