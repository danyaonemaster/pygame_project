# config.py
from photos.knight.animations import *

# --- Основные настройки ---
WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False
FPS = 60
animation_fps = 6

# --- Время ---
START_TIME = 0
CURRENT_TIME = 0
LAST_TIME = 0

# --- Позиции (в долях экрана, от 0 до 1) ---
PLAYER_POS = (0.25, 0.8125)        # 25% ширины, 81% высоты
SLIME_POS = (0.0625, 0.8125)       # чуть за экраном справа
SUN_POS = (0.85, 0.075)            # справа сверху
SCORE_POS = (0.075, 0.0375)        # левый верхний угол
FINAL_SCORE_POS = (0.5, 0.6)
GAME_NAME_POS = (0.5, 0.25)
BUTTON_POS = (0.5, 0.75)

# --- Размеры (в долях от ширины/высоты) ---
SLIME_SIZE = (0.1, 0.16)       # 6.25% ширины, 12.5% высоты
SUN_SIZE = (0.125, 0.25)           # 12.5% ширины, 25% высоты
PLAYER_SIZE = (0.125, 0.225)

# --- Цвета ---
BG_COLOR = "black"
TEXT_COLOR = "darkgreen"

GRAVITY = 0.0015 * HEIGHT

# Move speed
PLAYER_MOVE_SPEED = 0.05
SNAIL_MOVE_SPEED = 0.025

PlAYER_JUMP_STRENGTH = 0.032
SNAIL_JUMP_STRENGTH = 0.1

ANIMATIONS = {
    1: idle_anim,
    2: run_anim,
    3: jump_anim,
    4: fall_anim,
    5: atk_idle_and_atk2_anim,
    6: atk1_anim,
    7: atk1_anim,
    8: atk1_anim
}

## sates describe figure moveset (ie. state)
STATE_IDLE = 1
STATE_RUN = 2
STATE_JUMP = 3
STATE_FALL = 4
STATE_ATK2 = 5
STATE_ATK1 = 6
STATE_ATK_AIR = 7
STATE_ATK_RUN = 8

MOVE_DIRECTION_LEFT = 0
MOVE_DIRECTION_RIGHT = 1


