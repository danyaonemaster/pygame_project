import sys

import pygame

from assets.image import Image
from config import *
from photos.loader import *
from assets.tilemap import TileMap
from test_player import *
from utils import *


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Mario D&D")
        self.screen = pygame.display.set_mode((1200, 720))

        self.clock = pygame.time.Clock()

        self.background = Image(is_parallax=True, scale=scale_size(BACKGROUND_SIZE), image_folder=background_images)
        self.player = Player(PLAYER_POS, PLAYER_SIZE)
        self.player_group = pygame.sprite.Group(self.player)

        self.tilemap = TileMap("level/test_world.tmx")

    def run(self):

        while True:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()
            current_time = current_time // 1000

            self.background.move(keys)
            self.background.draw(self.screen)

            self.tilemap.tilemap.draw(self.screen)
            self.tilemap.offgrid_tiles.draw(self.screen)

            self.player.update(events, current_time, self.tilemap.tilemap)
            self.player_group.draw(self.screen)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)


Game().run()
