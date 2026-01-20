# utils.py
import config

def scale_pos(pos: tuple[float, float]) -> tuple[int, int]:
    return int(config.WIDTH * pos[0]), int(config.HEIGHT * pos[1])

def scale_size(size: tuple[float, float]) -> tuple[int, int]:
    return int(config.WIDTH * size[0]), int(config.HEIGHT * size[1])

def draw_group(group, screen, camera):
    for sprite in group:
        screen.blit(
            sprite.image,
            sprite.rect.topleft - camera.offset
        )


