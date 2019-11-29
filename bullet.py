class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SmallBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 0
        self.vy = 10
        self.radius = 6
        self.damage = 1
        self.color = (192, 192, 192)

    def to_imaginarium_rectangle(self):
        return {
            "left_x": self.x - self.radius,
            "top_y": self.y - self.radius,
            "width": self.radius << 1,
            "height": self.radius << 1
        }

class LargeBullet(SmallBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 1
        self.vy = 6.66
        self.radius = 12
        self.damage = 2

class MassiveBullet(SmallBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 2
        self.vy = 3.33
        self.radius = 24
        self.damage = 4

class FastBullet(SmallBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 3
        self.vy = 15
        self.radius = 8
        self.damage = 1