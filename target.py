import pygame, random
from powerup import LB, MB, FB, BR
    
class WeakTarget(pygame.sprite.Sprite):   # alvos vermelhos (1 vida)
    def __init__(self, x, y, width, height, vx):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.hit_points = 1
        self.sprites = [pygame.image.load("./assets/raider_vermelho.png").convert_alpha()]
        self.sprite = self.sprites[-1]

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
    
    def move_right(self, dt):
        self.x += self.vx * dt * 0.1
    
    def move_left(self, dt):
        self.x -= self.vx * dt * 0.1

    def move_down(self, amount):
        self.y += amount

    def hit_border(self, WIN_WIDTH, margin_of_error):
        if self.x + self.width >= WIN_WIDTH - margin_of_error or self.x <= margin_of_error : return True
        return False
    
    def hit_tank(self, tx, ty, twidth):
        if self.y >= ty and self.x >= tx and self.x <= tx + twidth : return True
        return False
    
    def update(self, targets):
        self.update_color()                                           # a cor altera
        if hasattr(self, "knockback"): self.knockback(50, targets)    # e procura por outras reações do alvo

    def lose_hit_points(self, amount):
        if self.hit_points - amount >= 1 : self.hit_points -= amount
        else : self.hit_points = 0
    
    def create_powerup(self):
        # dicionário dos powerups e respetivas probabilidades
        powerup_dict = {
            None               : 15,   # não gerar powerup
            LB(self.x, self.y) : 5,
            MB(self.x, self.y) : 2,
            FB(self.x, self.y) : 5,
            BR(self.x, self.y) : 3
        }

        # escolher um powerup aleatoriamente (ou nenhum)
                                        # multiplicar cada key do dicionário pelo número de vezes do seu value
        random_powerup = random.choice([key for key in powerup_dict for i in range(powerup_dict[key])])
        
        return random_powerup

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

def instantiate_targets(amount, rows, ini_x, ini_y, incr_x, incr_y, vx, win_width):
    target_list = []    # retorno da função

    pos_x = ini_x; pos_y = ini_y # definir posições de colocação do alvo
                                 # inicialmente serão iguais às posições do primeiro alvo, passadas como argumento

    for i in range(amount):
        # escolher um tipo de alvo aleatoriamente
        random_target_type = random.choice([
            WeakTarget(pos_x, pos_y, 20, 20, vx),
            ToughTarget(pos_x, pos_y, 20, 20, vx),
            StrongTarget(pos_x, pos_y, 20, 20, vx),
            KnockbackTarget(pos_x, pos_y, 20, 20, vx)
        ])

        # adicioná-lo à lista de alvos
        target_list.append(random_target_type)

        # distribuir o número de alvos pelo número de filas
        # se a nova pos do x for >= ao x do último elemento da fila  ou  a nova pos do x não está contida na janela
        if pos_x + incr_x >= ini_x + incr_x * (amount / rows) or pos_x + incr_x >= win_width:
            pos_x = ini_x        # a posição do x volta ao valor inicial
            pos_y += incr_y      # atualiza o valor de y para uma nova fila de alvos abaixo
        else:
            pos_x += incr_x      # atualiza o valor de x para a posição do próximo alvo

    return target_list