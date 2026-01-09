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

jump_anim = [
    os.path.join(BASE_PATH, "knight_jump", f"jump_frame_{i}.png")
    for i in range(3)
]

jump_fall_anim = [
    os.path.join(BASE_PATH, "knight_fall", f"fall_frame_{i}.png")
    for i in range(2)
]

fall_anim = [
    os.path.join(BASE_PATH, "knight_fall", f"fall_frame_{i}.png")
    for i in range(3)
]

atk_idle_and_atk2_anim = [
    os.path.join(BASE_PATH, "knight_atk_idle", f"atk_idle_{i}.png")
    for i in range(6)
]

atk1_anim = [
    os.path.join(BASE_PATH, "knight_atk1", f"atk1_{i}.png")
    for i in range(4)
]

death_anim = [
    os.path.join(BASE_PATH, "knight_atk1", f"atk1_{i}.png")
    for i in range(4)
]