import pygame, time, sys, math, random
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_RETURN

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

def get_font(size) : return pygame.font.Font("./assets/PressStart2P-Regular.ttf", size)
MSG_WIN = get_font(48).render("YOU WIN!", True, WHITE, BLACK)
MSG_NEWGAME = get_font(12).render("PRESS [ENTER] TO PLAY A NEW GAME.", True, WHITE, BLACK)

PADDLE_WIDTH = 30
paddle_x = 0
vx = 10
vy = 10
dt = 3
targets_move_right = True
target_y = 50

# instancializar 5 alvos
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
    if key_pressed[K_RETURN] and dt == 0:   # se ENTER premido e o jogo estiver terminado, começar novo jogo
        Target(20)
        Target(70)
        Target(120)
        Target(170)
        Target(220)
        Bullet._bullets = []
        targets_move_right = True
        target_y = 50
        dt = 3
    

    # desenhar o tanque
    pygame.draw.rect(win, WHITE, (paddle_x, WIN_HEIGHT - 10, PADDLE_WIDTH, 10), 0)

    # comportamento das balas
    for bullet in Bullet._bullets:
        pygame.draw.circle(win, BLUE, ((int)(bullet.x), (int)(bullet.y)), 10, 0) # desenhar as balas
        bullet.y -= 10 * dt * 0.1 # mover as balas
        if bullet.y >= target_y - 10 and bullet.y <= target_y + 10: # verificar se uma bala está à mesma altitude dos alvos
            for target in Target._targets:                                  # para cada alvo,
                if bullet.x >= target.x - 10 and bullet.x <= target.x + 10: # verificar se a bala se sobrepõe a algum
                    Bullet._bullets.remove(bullet)                          # se sim, remover a bala e o alvo
                    Target._targets.remove(target)
                    break
        if bullet.y <= 0: Bullet._bullets.remove(bullet) # apagar as balas que saem da janela

    # comportamento dos alvos
    for target in Target._targets:

        # desenhar alvos
        pygame.draw.circle(win, RED, ((int)(target.x), target_y), 10, 0)

        # mover os alvos
        if targets_move_right: target.x += vx * dt * 0.1
        if not targets_move_right: target.x -= vx * dt * 0.1

        # quando os alvos chegam ao extremo direito do ecrã
        if (target.x >= WIN_WIDTH - 20):
            targets_move_right = False
            target_y += 50

        # quando os alvos chegam ao extremo esquerdo do ecrã
        if (target.x <= 20):
            targets_move_right = True
            target_y += 50

    if not Target._targets:     # se não houver alvos, apresentar mensagem de jogo ganho
        dt = 0
        win.blit(
            MSG_WIN,
            [ WIN_WIDTH / 2 - MSG_WIN.get_width() / 2, WIN_HEIGHT / 2 - MSG_WIN.get_height() / 2 ] # centrar na janela
        )
        win.blit(
            MSG_NEWGAME,
            # centrar no eixo dos x                         centrar no eixo dos y e empurrar para baixo 50px
            [ WIN_WIDTH / 2 - MSG_NEWGAME.get_width() / 2, WIN_HEIGHT / 2 - MSG_NEWGAME.get_height() / 2 + 50 ]
        )

    time.sleep(0.015)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()