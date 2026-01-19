import pygame
from pygame_project.assets.tiles import Tileset
import pytmx
from pygame_project.config import TILE_SIZE

class TileMap(pygame.sprite.Sprite):
    def __init__(self, filepath):
        super().__init__()
        self.tilemap = pygame.sprite.Group()
        self.offgrid_tiles = pygame.sprite.Group()
        self.level_data = pytmx.util_pygame.load_pygame(filepath)
        self.load_tile_map()


    def load_tile_map(self):
        for layer in self.level_data.visible_layers:

            if not isinstance(layer, pytmx.TiledTileLayer):
                continue

            if layer.name == "platforms":
                for x, y, surface in layer.tiles():
                    Tileset((x * TILE_SIZE, y * TILE_SIZE), surface, self.tilemap)

            else:
                for x, y, surface in layer.tiles():
                    Tileset((x * TILE_SIZE, y * TILE_SIZE), surface, self.offgrid_tiles)








