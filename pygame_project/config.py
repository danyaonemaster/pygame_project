# config.py
import photos.knight.animations as knight
import photos.slime.animations as slime

WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False
GAME_ACTIVE = False
FPS = 60
animation_fps = 6

START_TIME = 0
CURRENT_TIME = 0
LAST_TIME = 0

PLAYER_POS = (0.25, 0.79)
SLIME_POS = (0.0625, 0.8125)
SUN_POS = (0.85, 0.075)
SCORE_POS = (0.075, 0.0375)
FINAL_SCORE_POS = (0.5, 0.6)
GAME_NAME_POS = (0.5, 0.25)
BUTTON_POS = (0.5, 0.75)

SLIME_SIZE = (0.200, 0.200)
SUN_SIZE = (0.125, 0.25)
PLAYER_SIZE = (0.33, 0.3)
BACKGROUND_SIZE = (0.6, 0.9)

# --- Цвета ---
BG_COLOR = "black"
TEXT_COLOR = "darkgreen"

GRAVITY = 0.0015 * HEIGHT

# Move speed
PLAYER_MOVE_SPEED = 0.05
SNAIL_MOVE_SPEED = 0.025

PlAYER_JUMP_STRENGTH = 0.032
SNAIL_JUMP_STRENGTH = 0.1

STATE_IDLE = 1
STATE_RUN = 2
STATE_JUMP = 3
STATE_FALL = 4
STATE_ATK2 = 5
STATE_ATK1 = 6
STATE_ATK_AIR = 7
STATE_ATK_RUN = 8
STATE_DEATH = 9

S_ANIMATIONS = {
    STATE_IDLE: slime.idle_anim,
    STATE_JUMP: slime.jump_anim
}

K_ANIMATIONS = {
    STATE_IDLE: knight.idle_anim,
    STATE_RUN: knight.run_anim,
    STATE_JUMP: knight.jump_anim,
    STATE_FALL: knight.fall_anim,
    STATE_ATK2: knight.atk_idle_and_atk2_anim,
    STATE_ATK1: knight.atk1_anim,
    STATE_ATK_AIR: knight.atk1_anim,
    STATE_ATK_RUN: knight.atk1_anim,
    STATE_DEATH: knight.death_anim
}

## sates describe figure moveset (ie. state)

MOVE_DIRECTION_LEFT = 0
MOVE_DIRECTION_RIGHT = 1


