import os

BASE_PATH = os.path.dirname(__file__)

background_images = [
    (
        os.path.join(BASE_PATH, "background", f"Background_{i}.png"),
        0.2 * (i + 1)
    )
    for i in range(2)
]
grass_background = [
    (
        os.path.join(BASE_PATH, "grass_background", f"Grass_background_{i}.png"),
        1 * (i + 1)
    )
    for i in range(2)
]

