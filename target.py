import pygame, random

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vx):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx

class WeakTarget(Target):   # alvos vermelhos (1 vida)
    def __init__(self, x, y, width, height, vx):
        super().__init__(x, y, width, height, vx)
        self.hit_points = 1
        self.sprites = [pygame.image.load("./assets/raider_vermelho.png").convert_alpha()]
        self.sprite = self.sprites[-1]

    def lose_hit_points(self, amount):
        if self.hit_points >= 1 : self.hit_points -= amount
        else : self.hit_points = 0

class ToughTarget(WeakTarget): # alvos verdes (2 vidas)
    def __init__(self, x, y, width, height, vx):
        super().__init__(x, y, width, height, vx)
        self.hit_points = 2
        self.sprites.append(pygame.image.load("./assets/raider_verde.png").convert_alpha())
        self.sprite = self.sprites[-1]

    def update_color(self):     # a lista onde as cores estão guardadas é lida da direita para esquerda
        self.sprite = self.sprites[self.hit_points - 1]

class StrongTarget(ToughTarget): # alvos amarelos (3 vidas)
    def __init__(self, x, y, width, height, vx):
        super().__init__(x, y, width, height, vx)
        self.hit_points = 3
        self.sprites.append(pygame.image.load("./assets/raider_amarelo.png").convert_alpha())
        self.sprite = self.sprites[-1]

class KnockbackTarget(ToughTarget): # alvos ciano (um knockback e +1 vida)
    def __init__(self, x, y, width, height, vx):
        super().__init__(x, y, width, height, vx)
        self.sprites.append(pygame.image.load("./assets/raider_ciano.png").convert_alpha())
        self.sprite = self.sprites[-1]

    def knockback(self, knockback_distance, targets):
        is_searching_vacancy = True
        while is_searching_vacancy:
            is_above_occupied = False
            for target in targets:
                if target.x == self.x and target.y == self.y - knockback_distance:
                    knockback_distance += knockback_distance
                    is_above_occupied = True
                    break
            if not is_above_occupied:
                self.y -= knockback_distance
                is_searching_vacancy = False

def instantiate_targets(amount, ini_x, ini_y, spacing_x, spacing_y, win_width, win_height, vx):
    targets = []

    pos_x = ini_x; pos_y = ini_y

    for i in range(amount):
        num = random.randint(0, 3)
        if num == 0   : targets.extend([WeakTarget(pos_x, pos_y, 20, 20, vx)])
        elif num == 1 : targets.extend([ToughTarget(pos_x, pos_y, 20, 20, vx)])
        elif num == 2 : targets.extend([StrongTarget(pos_x, pos_y, 20, 20, vx)])
        elif num == 3 : targets.extend([KnockbackTarget(pos_x, pos_y, 20, 20, vx)])

        if pos_x + spacing_x >= ini_x + spacing_x * (amount >> 1):
            pos_x = ini_x
            pos_y += spacing_y
        else:
            pos_x += spacing_x

    return targets