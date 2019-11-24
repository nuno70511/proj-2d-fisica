class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WeakTarget(Target):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 0
        self.hit_points = 1
        self.color = (255, 0, 0)

    def lose_hit_points(self, amount):
        if self.hit_points >= 1 : self.hit_points -= amount
        else : self.hit_points = 0

class ToughTarget(WeakTarget):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 1
        self.hit_points = 2
        self.color = (0, 255, 0)

class StrongTarget(WeakTarget):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 2
        self.hit_points = 3
        self.color = (255, 255, 0)

class KnockbackTarget(ToughTarget):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 3
        self.color = (0, 255, 255)
    
    def knockback(self, y):
        self.y -= y