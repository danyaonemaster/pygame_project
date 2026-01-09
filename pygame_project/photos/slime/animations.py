import os

BASE_PATH = os.path.dirname(__file__)


idle_anim = [
    os.path.join(BASE_PATH, "slime_idle", f"slime_idle_{i}.png" if i >= 10 else f"slime_idle_0{i}.png")
    for i in range(15)
]

jump_anim = [
    os.path.join(BASE_PATH, "slime_jump", f"slime_jump_{i}.png" if i >= 10 else f"slime_jump_0{i}.png")
    for i in range(1,18)
]
