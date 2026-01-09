import pygame
from photos.loader import *
from assets.image import GameSprite
from test_player import Player
import config
import utils
from utils import scale_pos, scale_size

pygame.init()

screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Mario (D&D)")
clock = pygame.time.Clock()
screen_size = screen.get_size()

player = Player(scale_pos(config.PLAYER_POS), scale_size(config.PLAYER_SIZE))  # например
sprites = pygame.sprite.Group(player)

background = GameSprite(scale=utils.scale_size(config.BACKGROUND_SIZE), image_folder= background_images, is_parallax=True)

running = True
while running:
    dt = clock.tick(60)
    events = pygame.event.get()
    current_time = pygame.time.get_ticks()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    background.move(pygame.key.get_pressed())
    background.draw(screen)

    sprites.update(events, current_time)
    sprites.draw(screen)

    pygame.display.flip()

pygame.quit()