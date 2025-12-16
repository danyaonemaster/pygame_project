# utils.py
import config

def scale_pos(pos: tuple[float, float]) -> tuple[int, int]:
    """Преобразует доли экрана (0–1) в пиксели под текущее разрешение."""
    return int(config.WIDTH * pos[0]), int(config.HEIGHT * pos[1])

def scale_size(size: tuple[float, float]) -> tuple[int, int]:
    """Масштабирует размеры в зависимости от экрана."""
    return int(config.WIDTH * size[0]), int(config.HEIGHT * size[1])
