import pygame

BASE_IMAGE_PATH = "photos/"

def load_image(filename):
    img = pygame.image.load(BASE_IMAGE_PATH + filename).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img
