import pygame
import config
from assets.image import GameSprite
from test_player import Player
from assets.text import Text
from utils import scale_pos, scale_size
from entities.slime import Slime

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Mario (D&D)")
pygame.display.set_icon(pygame.image.load('photos/icon.png'))
clock = pygame.time.Clock()

slime = Slime(config.SLIME_POS, config.SLIME_SIZE)
enemy_group = pygame.sprite.Group(slime)

player = Player(scale_pos(config.PLAYER_POS), scale_size(config.PLAYER_SIZE))
sprites = pygame.sprite.Group(player)

# --- Score ---
score = Text("0", int(config.HEIGHT * 0.075), scale_pos(config.SCORE_POS), config.TEXT_COLOR)
score_group = pygame.sprite.Group(score)

# --- Game screens ---
game_name = Text("Mario (D&D)", int(config.HEIGHT * 0.25), scale_pos(config.GAME_NAME_POS), "purple")
start_game = Text("Start Game", int(config.HEIGHT * 0.125), scale_pos(config.BUTTON_POS), "lightyellow")
game_start_group = pygame.sprite.Group(game_name, start_game)

game_over_text = Text("Game Over", int(config.HEIGHT * 0.225), scale_pos(config.GAME_NAME_POS), "darkred")
retry_text = Text("Retry", int(config.HEIGHT * 0.125), scale_pos(config.BUTTON_POS), "darkred")
game_over_screen_group = pygame.sprite.Group(game_over_text, retry_text)

# --- State ---
game_start = True
running = True

while running:
    dt = clock.tick(60) / 1000  # seconds per frame (float)
    now_ms = pygame.time.get_ticks()
    elapsed_sec = (now_ms - config.START_TIME) // 1000 if not game_start and config.START_TIME else 0

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                config.FULLSCREEN = not config.FULLSCREEN
                if config.FULLSCREEN:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1280, 720))

    screen.fill(config.BG_COLOR)

    # --- Start Screen ---
    if game_start:
        game_start_group.draw(screen)

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_game.rect.collidepoint(event.pos):
                    game_start = False
                    config.GAME_ACTIVE = True
                    config.START_TIME = pygame.time.get_ticks()
                    config.LAST_TIME = 0

    # --- Game Active ---
    if config.GAME_ACTIVE and not game_start:

        # --- Score ---
        current_time = (pygame.time.get_ticks() - config.START_TIME)
        score.update_text(f"Score: {current_time // 1000}")
        score_group.draw(screen)
        config.LAST_TIME = current_time // 1000

        # --- Player ---
        sprites.update(event_list, current_time)
        sprites.draw(screen)

        # --- Slime ---
        enemy_group.update(current_time)
        enemy_group.draw(screen)


        offset = (player.rect.x - slime.rect.x, player.rect.y - slime.rect.y)

        if slime.mask.overlap(player.mask, offset) and  not player.attacking:
            died = player.take_damage(10, current_time, scale_pos(config.PLAYER_POS))
            if died:
                config.GAME_ACTIVE = False

    # --- Game Over Screen ---
    if not config.GAME_ACTIVE and not game_start:
        game_over_screen_group.draw(screen)
        final_score = Text(f"Score: {config.LAST_TIME}", int(config.HEIGHT * 0.1), scale_pos(config.FINAL_SCORE_POS), config.TEXT_COLOR)
        screen.blit(final_score.image, final_score.rect)

        # click processing Retry
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_text.rect.collidepoint(event.pos):
                    player.reset(scale_pos(config.PLAYER_POS))
                    config.GAME_ACTIVE = True
                    slime.restart()
                    config.START_TIME = pygame.time.get_ticks()

    pygame.display.flip()

pygame.quit()
