import pygame
from bullet import SmallBullet, LargeBullet, MassiveBullet, FastBullet

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move_down(self, incr_y):
        self.y += incr_y

class LB(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = pygame.image.load("./assets/powerup_lb.png").convert_alpha()
        self.bullet_type = "lb"
        self.desc = "LARGE BULLET"

class MB(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = pygame.image.load("./assets/powerup_mb.png").convert_alpha()
        self.bullet_type = "mb"
        self.desc = "MASSIVE BULLET"

class FB(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = pygame.image.load("./assets/powerup_fb.png").convert_alpha()
        self.bullet_type = "fb"
        self.desc = "FAST BULLET"