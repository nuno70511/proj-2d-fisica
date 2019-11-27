import pygame

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def calc_top_left_x(self):
        return self.x - self.width / 2

    def calc_top_left_y(self):
        return self.y - self.height / 2

class WeakTarget(Target):   # alvos vermelhos (1 vida)
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.hit_points = 1
        self.sprites = [pygame.image.load("./assets/raider_vermelho.png").convert_alpha()]
        self.sprite = self.sprites[-1]

    def lose_hit_points(self, amount):
        if self.hit_points >= 1 : self.hit_points -= amount
        else : self.hit_points = 0

class ToughTarget(WeakTarget): # alvos verdes (2 vidas)
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.hit_points = 2
        self.sprites.append(pygame.image.load("./assets/raider_verde.png").convert_alpha())
        self.sprite = self.sprites[-1]

    def update_color(self):     # a lista onde as cores estão guardadas é lida da direita para esquerda
        self.sprite = self.sprites[self.hit_points - 1]

class StrongTarget(ToughTarget): # alvos amarelos (3 vidas)
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.hit_points = 3
        self.sprites.append(pygame.image.load("./assets/raider_amarelo.png").convert_alpha())
        self.sprite = self.sprites[-1]

class KnockbackTarget(ToughTarget): # alvos ciano (um knockback e +1 vida)
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.sprites.append(pygame.image.load("./assets/raider_ciano.png").convert_alpha())
        self.sprite = self.sprites[-1]
    
    def knockback(self, y):
        self.y -= y