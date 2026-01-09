import os

BASE_PATH = os.path.dirname(__file__)

background_images = [
    (
        os.path.join(BASE_PATH, "background", f"dark_forest_{i}.png"),
        0.5 * (i + 1)
    )
    for i in range(5)
]

