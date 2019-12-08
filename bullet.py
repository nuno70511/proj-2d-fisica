import pygame, math

class SmallBullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 10
        self.radius = 6
        self.damage = 1
        self.color = (250, 250, 250)
        self.pierce = 1
        self.piercedTargets = []
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, ((int)(self.x), (int)(self.y)), self.radius, 0)
    
    def move(self, dt):
        self.y -= self.vy * dt * 0.1
    
    def is_out_of_bounds(self, WIN_HEIGHT, WIN_WIDTH):
        if (
            self.y + self.radius <= 0               # sair pelo topo
         or self.y - self.radius >= WIN_HEIGHT      # sair pelo fundo
         or self.x + self.radius <= 0               # sair pela esquerda
         or self.x - self.radius >= WIN_WIDTH       # sair pela direita
        ):
            return True
        return False

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
    
    def look_for_contact(self, bullet, targets):
        for i in range(len(targets)):
            target = targets[i]
            
            # imaginar a bala como um retangulo para poder comparar posições com os alvos
            bullet_rect = bullet.to_imaginary_rectangle()

            # verificar se não há sobreposição
            if (
                bullet_rect["top_y"] > target.y + target.height          # a bala está abaixo do alvo
                or bullet_rect["top_y"] + bullet_rect["height"] < target.y  # a bala está acima do alvo
                or bullet_rect["left_x"] + bullet_rect["width"] < target.x  # a bala está mais à esquerda
                or bullet_rect["left_x"] > target.x + target.width          # a bala está mais à direita
            ): continue
        
            # há contacto
            self.handle_contact(bullet, target)
            return i
            
        return -1

    def handle_contact(self, bullet, target):
        if target not in bullet.piercedTargets:                 # (impedir que a bala perfure o mesmo alvo entre frames)
            target.lose_hit_points(bullet.damage)               # retirar vida ao alvo
            bullet.pierced(target)                              # retirar poder de perfuração à bala

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
        self.theta = 180 - theta    # inverter o angulo de modo a que a sua amplitude aumente para a direita
        self.x0 = x
        self.y0 = y
        self.v0_x = v0 * math.cos(math.radians((float) (self.theta)))
        self.v0_y = v0 * math.sin(math.radians((float) (self.theta)))
        self.color = (170, 100, 40)
        self.pierce = 7
    
    def move(self, dt):
        self.x = self.x0 + self.v0_x * self.t
        self.y = self.y0 - self.v0_y * self.t + 0.5 * self.g * self.t**2
        self.t += dt * 0.02
    
    def got_collected(self, tx, ty, twidth):
        if self.y >= ty and self.x - self.radius >= tx and self.x + self.radius <= tx + twidth : return True
        return False