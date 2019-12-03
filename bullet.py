import math

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SmallBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vy = 10
        self.radius = 6
        self.damage = 1
        self.color = (250, 250, 250)
        self.pierce = 1
        self.piercedTargets = []

    def pierced(self, target):
        self.pierce -= 1
        self.piercedTargets.append(target)

    def to_imaginary_rectangle(self):
        return {
            "left_x": self.x - self.radius,
            "top_y": self.y - self.radius,
            "width": self.radius << 1,
            "height": self.radius << 1
        }

class LargeBullet(SmallBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vy = 9
        self.radius = 8
        self.damage = 2
        self.color = (0, 0, 255)

class MassiveBullet(SmallBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vy = 7
        self.radius = 12
        self.damage = 4
        self.color = (255, 0, 255)
        self.pierce = 3

class FastBullet(SmallBullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vy = 18
        self.color = (255, 0, 0)
        self.pierce = 2

class Boomerang(SmallBullet):
    def __init__(self, x, y, theta, v0):
        super().__init__(x, y)
        self.g = 9.8
        self.t = 0
        self.theta = theta
        self.x0 = x
        self.y0 = y
        self.v0_x = v0 * math.cos(math.radians((float) (self.theta)))
        self.v0_y = v0 * math.sin(math.radians((float) (self.theta)))
        self.pierce = 7
    
    def update_pos(self, dt):
        self.x = self.x0 + self.v0_x * self.t
        self.y = self.y0 - self.v0_y * self.t + 0.5 * self.g * self.t**2
        self.t += dt * 0.02