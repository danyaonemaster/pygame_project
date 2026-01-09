class Health:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.hp = max_hp
        self.last_hit = 0

    def damage(self, amount, current_time):
        self.last_hit = current_time
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_dead(self):
        return self.hp <= 0
