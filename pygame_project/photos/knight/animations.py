import os

BASE_PATH = os.path.dirname(__file__)

idle_anim = [
    os.path.join(BASE_PATH, "knight_idle", f"idle_frame_{i}.png")
    for i in range(10)
]

run_anim = [
    os.path.join(BASE_PATH, "knight_run", f"run_frame_{i}.png")
    for i in range(10)
]