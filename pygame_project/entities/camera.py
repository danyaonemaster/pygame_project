import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def follow(self, target):
        self.offset.x = max(
            0,
            min(
                target.rect.centerx - self.width // 2,
                6400*16 - self.width
            )
        )


