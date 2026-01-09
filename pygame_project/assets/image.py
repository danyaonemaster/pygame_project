import pygame
from pygame.sprite import Sprite


class GameSprite(Sprite):
    def __init__(self, position=(0, 0), scale=None, image_folder=None, is_parallax=False):
        super().__init__()

        self.position = position
        self.scale = scale
        self.is_parallax = is_parallax

        self.layers = []   # [(image, speed)]
        self.scroll = 0

        if is_parallax and image_folder:
            for path, speed in image_folder:
                img = pygame.image.load(path).convert_alpha()
                if scale:
                    img = pygame.transform.scale(img, scale)
                self.layers.append((img, speed))

            self.width = self.layers[0][0].get_width()

    # ===== ДВИЖЕНИЕ ФОНА =====
    def move(self, direction):
        if direction[pygame.K_d]:
            self.scroll += 3
        if direction[pygame.K_a]:
            self.scroll -= 3

    # ===== ОТРИСОВКА =====
    def draw(self, surface):
        if not self.is_parallax:
            return

        for img, speed in self.layers:
            x = -self.scroll * speed
            for i in range(10):
                surface.blit(img, (x + i * self.width, 0))
