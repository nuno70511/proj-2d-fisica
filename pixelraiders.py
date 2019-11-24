import pygame, time, sys, math, random
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_RETURN
from bullet import Bullet
from target import Target

pygame.init()
pygame.display.set_caption("Pixel Raiders")

WIN_WIDTH = 700; WIN_HEIGHT = 500
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def get_font(size) : return pygame.font.Font("./assets/PressStart2P-Regular.ttf", size)
MSG_YOUWIN = get_font(48).render("YOU WIN!", True, WHITE, BLACK)
MSG_GAMEOVER = get_font(48).render("GAME OVER!", True, RED, BLACK)
MSG_NEWGAME = get_font(12).render("PRESS [ENTER] TO PLAY A NEW GAME", True, WHITE, BLACK)
MSG_QUIT = get_font(8).render("PRESS [ESC] AT ANY TIME TO QUIT THE GAME", True, WHITE, BLACK)

PADDLE_WIDTH = 30                   #   largura do tanque
PADDLE_Y = WIN_HEIGHT - 10          #   o valor das ordenadas do topo do tanque
paddle_x = 0                        #   o valor das abcissas do lado esquerdo do tanque
vx = 10
vy = 10
dt = 3
bullets = []                        #   guarda as instâncias das balas
targets = []                        #   guarda as instâncias dos alvos
targets_move_right = True           #   condição de os alvos estarem a mover-se para a direita
targets_move_down = False           #   condição de os alvos moverem-se para baixo
# instancializar 10 alvos
targets.extend([
    Target(20, 40), Target(70, 40), Target(120, 40), Target(170, 40), Target(220, 40),
    Target(20, 90), Target(70, 90), Target(120, 90), Target(170, 90), Target(220, 90)
])

while True:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP and dt != 0:
            if event.key == pygame.K_SPACE: # ao premir espaço, instanciar uma bala a partir da posição do tanque
                x = paddle_x + PADDLE_WIDTH / 2
                y = PADDLE_Y - 10 
                bullets.append(Bullet(x, y))

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT] and dt != 0: # mover o tanque para a esquerda
        if paddle_x <= 1: paddle_x = 1
        else: paddle_x -= dt
    if key_pressed[K_RIGHT]  and dt != 0: # mover o tanque para a direita
        if paddle_x + PADDLE_WIDTH + 1 >= WIN_WIDTH: paddle_x = WIN_WIDTH - PADDLE_WIDTH - 1
        else: paddle_x += dt
    if key_pressed[K_ESCAPE]:   # se ESC premido, sair do jogo
        pygame.quit()
        sys.exit()
    if key_pressed[K_RETURN] and dt == 0:   # se ENTER premido e o jogo estiver terminado, começar novo jogo
        bullets = []
        targets = []
        targets_move_right = True
        targets.extend([
            Target(20, 40), Target(70, 40), Target(120, 40), Target(170, 40), Target(220, 40),
            Target(20, 90), Target(70, 90), Target(120, 90), Target(170, 90), Target(220, 90)
        ])
        dt = 3
    

    # desenhar o tanque
    pygame.draw.rect(win, WHITE, (paddle_x, PADDLE_Y, PADDLE_WIDTH, 10), 0)

    # comportamento das balas
    for bullet in bullets:

        pygame.draw.circle(win, BLUE, ((int)(bullet.x), (int)(bullet.y)), 10, 0) # desenhar as balas

        if not targets : break  # se não houver alvos, o jogo está parado e as balas ficarão estáticas
                                # logo, não interessa estudar o seu comportamento e o ciclo é quebrado

        bullet.y -= 10 * dt * 0.1 # mover as balas

        for target in targets:                                              # para cada alvo,
            if (bullet.y >= target.y - 10 and bullet.y <= target.y + 10     # se uma bala está à mesma altitude dos alvos
            and bullet.x >= target.x - 10 and bullet.x <= target.x + 10):   # verificar se a bala se sobrepõe a algum
                bullets.remove(bullet)                                      # se sim, remover a bala e o alvo
                targets.remove(target)
                break

        if bullet.y <= 0: bullets.remove(bullet) # apagar as balas que saem da janela

    # comportamento dos alvos
    for target in targets:

        # desenhar alvos
        pygame.draw.circle(win, RED, ((int)(target.x), target.y), 10, 0)

        # mover os alvos
        if targets_move_right : target.x += vx * dt * 0.1
        else : target.x -= vx * dt * 0.1

        # se houver colisão entre um alvo e o tanque, apresentar mensagem de jogo perdido
        if target.y >= PADDLE_Y and target.x >= paddle_x and target.x <= paddle_x + PADDLE_WIDTH:
            dt = 0
            win.blit(
                MSG_GAMEOVER,
                # centrar na janela
                [ WIN_WIDTH / 2 - MSG_GAMEOVER.get_width() / 2, WIN_HEIGHT / 2 - MSG_GAMEOVER.get_height() / 2 ]
            )
            win.blit(
                MSG_NEWGAME,
                # centrar no eixo dos x                         centrar no eixo dos y e empurrar para baixo 50px
                [ WIN_WIDTH / 2 - MSG_NEWGAME.get_width() / 2, WIN_HEIGHT / 2 - MSG_NEWGAME.get_height() / 2 + 50 ]
            )

        # quando os alvos chegam ao extremo direito do ecrã
        if target.x >= WIN_WIDTH - 20:
            targets_move_right = False
            targets_move_down = True

        # quando os alvos chegam ao extremo esquerdo do ecrã
        if target.x <= 20:
            targets_move_right = True
            targets_move_down = True

    # se um alvo chegou a um extremo, aumentar ordenadas de todos os alvos
    if targets_move_down:
        for target in targets: target.y += 50
        targets_move_down = False

    if not targets:     # se não houver alvos, apresentar mensagem de jogo ganho
        dt = 0
        win.blit(
            MSG_YOUWIN,
            [ WIN_WIDTH / 2 - MSG_YOUWIN.get_width() / 2, WIN_HEIGHT / 2 - MSG_YOUWIN.get_height() / 2 ] # centrar na janela
        )
        win.blit(
            MSG_NEWGAME,
            # centrar no eixo dos x                         centrar no eixo dos y e empurrar para baixo 50px
            [ WIN_WIDTH / 2 - MSG_NEWGAME.get_width() / 2, WIN_HEIGHT / 2 - MSG_NEWGAME.get_height() / 2 + 50 ]
        )

    #   instrução de fechar o pgm
    win.blit(MSG_QUIT, [4, 4])

    time.sleep(0.015)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()