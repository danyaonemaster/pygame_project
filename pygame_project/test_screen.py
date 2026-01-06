import pygame
from test_player import Player
pygame.init()

screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Mario (D&D)")
clock = pygame.time.Clock()
screen_size = screen.get_size()

player = Player((300, 500), (300, 300))  # например
sprites = pygame.sprite.Group(player)

while True:
    dt = clock.tick(60)
    events = pygame.event.get()
    current_time = pygame.time.get_ticks()
    sprites.update(events, current_time)

    screen.fill((0,0,0))
    sprites.draw(screen)
    pygame.display.flip()
