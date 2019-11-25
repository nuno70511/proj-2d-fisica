class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WeakTarget(Target):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hit_points = 1
        self.color = (255, 0, 0)

    def lose_hit_points(self, amount):
        if self.hit_points >= 1 : self.hit_points -= amount
        else : self.hit_points = 0

class ToughTarget(WeakTarget):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hit_points = 2
        self.colors = [(255, 0, 0), (0, 255, 0)]
        self.color = self.colors[-1]

    def update_color(self):
        self.color = self.colors[1 - self.hit_points]

class StrongTarget(ToughTarget):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hit_points = 3
        self.colors.append((255, 255, 0))
        self.color = self.colors[-1]

class KnockbackTarget(ToughTarget):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.colors = [(255, 0, 0), (0, 255, 255)]
        self.color = self.colors[-1]
    
    def knockback(self, y):
        self.y -= y