import pygame
from bullet import *

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
    
    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
    
    def collected(self, tx, ty, twidth):
        if self.y >= ty and self.x >= tx and self.x <= tx + twidth : return True
        return False
    
    def is_out_of_bounds(self, WIN_HEIGHT):
        if self.y >= WIN_HEIGHT : return True
        return False
    
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

class BR(Powerup):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = pygame.image.load("./assets/powerup_br.png").convert_alpha()
        self.bullet_type = "br"
        self.desc = "BOOMERANG"