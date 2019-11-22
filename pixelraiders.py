import pygame, time, sys, math, random
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE

pygame.init()
pygame.display.set_caption("Pixel Raiders")

class Bullet:
    _bullets = []

    def __init__(self, x, y):
        self._bullets.append(self)
        self.x = x
        self.y = y

class Target:
    _targets = []

    def __init__(self, x):
        self._targets.append(self)
        self.x = x


WIN_WIDTH = 700; WIN_HEIGHT = 500
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PADDLE_WIDTH = 30
paddle_x = 0
vx = 10
vy = 10
dt = 3
movesRight = True
target_y = 50

Target(20)
Target(70)
Target(120)
Target(170)
Target(220)

while True:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE: # ao premir espaço, instanciar uma bala a partir da posição do tanque
                x = paddle_x + PADDLE_WIDTH / 2
                y = WIN_HEIGHT - 20
                Bullet(x, y)

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT]: # mover o tanque para a esquerda
        if paddle_x <= 1: paddle_x = 1
        else: paddle_x -= dt
    if key_pressed[K_RIGHT]: # mover o tanque para a direita
        if paddle_x + PADDLE_WIDTH + 1 >= WIN_WIDTH: paddle_x = WIN_WIDTH - PADDLE_WIDTH - 1
        else: paddle_x += dt
    if key_pressed[K_ESCAPE]:   # se ESC premido, sair do jogo
        pygame.quit()
        sys.exit()
            

    # desenhar o tanque
    pygame.draw.rect(win, WHITE, (paddle_x, WIN_HEIGHT - 10, PADDLE_WIDTH, 10), 0)

    for bullet in Bullet._bullets:
        pygame.draw.circle(win, BLUE, ((int)(bullet.x), (int)(bullet.y)), 10, 0) # desenhar as balas
        bullet.y -= 10 * dt * 0.1
        if bullet.y >= target_y - 10 and bullet.y <= target_y + 10:     # se uma bala estiver à mesma altitude dos alvos
                                                                        # verificar se esta se sobrepõe a algum
                                                                        # e remover a bala e o alvo
            for target in Target._targets:
                if bullet.x >= target.x - 10 and bullet.x <= target.x + 10:
                    Bullet._bullets.remove(bullet)
                    Target._targets.remove(target)
                    break
        if bullet.y <= 0: Bullet._bullets.remove(bullet) # apagar as balas que saem da janela

    # comportamento dos inimigos
    for target in Target._targets:

        if movesRight: target.x += vx * dt * 0.1
        if not movesRight: target.x -= vx * dt * 0.1

        # desenhar inimigo
        pygame.draw.circle(win, RED, ((int)(target.x), target_y), 10, 0)

        if (target.x >= WIN_WIDTH - 20):
            movesRight = False
            target_y += 50

        if (target.x <= 20):
            movesRight = True
            target_y += 50

    time.sleep(0.015)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()