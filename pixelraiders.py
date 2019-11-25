import pygame, time, sys, math, random
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_RETURN
from bullet import SmallBullet, LargeBullet, MassiveBullet, FastBullet
from target import WeakTarget, ToughTarget, StrongTarget, KnockbackTarget
from tank import Tank

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

dt = 3
bullets = []                        #   guarda as instâncias das balas
targets = []                        #   guarda as instâncias dos alvos
targets_move_right = True           #   condição de os alvos estarem a mover-se para a direita
targets_move_down = False           #   condição de os alvos moverem-se para baixo

tank = Tank(WIN_WIDTH / 2 - 20, WIN_HEIGHT - 20, 40, 20, 10, 4, 4, 2)     # instancializar o tanque

# instancializar 10 alvos
targets.extend([
    StrongTarget(20, 40), ToughTarget(70, 40), KnockbackTarget(120, 40), ToughTarget(170, 40), StrongTarget(220, 40),
    WeakTarget(20, 90),   WeakTarget(70, 90),  WeakTarget(120, 90),      WeakTarget(170, 90),  WeakTarget(220, 90)
])

while True:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP and dt != 0 and tank.clip > 0:
            if event.key == pygame.K_SPACE: # ao premir espaço, instanciar uma bala a partir da posição do tanque
                x = tank.x + tank.width / 2 - 4 # centro do canhão
                y = tank.y - 10
                bullets.append(SmallBullet(x, y))
                tank.clip -= 1

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT] and dt != 0: # mover o tanque para a esquerda
        if tank.x <= 1 : tank.x = 1
        else : tank.x -= dt
    if key_pressed[K_RIGHT]  and dt != 0: # mover o tanque para a direita
        if tank.x + tank.width + 1 >= WIN_WIDTH : tank.x = WIN_WIDTH - tank.width - 1
        else : tank.x += dt
    if key_pressed[K_ESCAPE]:   # se ESC premido, sair do jogo
        pygame.quit()
        sys.exit()
    if key_pressed[K_RETURN] and dt == 0:   # se ENTER premido e o jogo estiver terminado, começar novo jogo
        bullets = []
        targets = []
        targets_move_right = True
        tank.x = WIN_WIDTH / 2 - 20
        tank.clip = 4
        tank.reload_timer = 0
        targets.extend([
            StrongTarget(20, 40), ToughTarget(70, 40), KnockbackTarget(120, 40), ToughTarget(170, 40), StrongTarget(220, 40),
            WeakTarget(20, 90),   WeakTarget(70, 90),  WeakTarget(120, 90),      WeakTarget(170, 90),  WeakTarget(220, 90)
        ])
        dt = 3


    # desenhar o tanque
    pygame.draw.rect(win, WHITE, (tank.x, tank.y, tank.width, tank.height), 0)

    # comportamento das balas
    for bullet in bullets:

        pygame.draw.circle(win, BLUE, ((int)(bullet.x), (int)(bullet.y)), bullet.radius, 0) # desenhar as balas

        if not targets : break  # se não houver alvos, o jogo está parado e as balas ficarão estáticas
                                # logo, não interessa estudar o seu comportamento e o ciclo é quebrado

        bullet.y -= bullet.vy * dt * 0.1 # mover as balas

        for target in targets:                                              # para cada alvo,
            if (bullet.y >= target.y - 10 and bullet.y <= target.y + 10     # se uma bala está à mesma altitude dos alvos
            and bullet.x >= target.x - 10 and bullet.x <= target.x + 10):   # verifica se a bala se sobrepõe a algum
                bullets.remove(bullet)                                      # se sim, remove a bala
                target.lose_hit_points(1)                                   # e retira um ponto de vida ao alvo
                if target.hit_points == 0:                                  # caso não reste mais vida ao alvo,
                    targets.remove(target)                                  # remove-o
                    break                                                   # e não vê mais nenhuma condição
                target.update_color()                                       # caso contrário, a cor altera
                if hasattr(target, "knockback") : target.knockback(50)      # e procura por outras reações do alvo
                break

        if bullet.y <= 0: bullets.remove(bullet) # apagar as balas que saem da janela

    # comportamento dos alvos
    for target in targets:

        # desenhar alvos
        pygame.draw.circle(win, target.color, ((int)(target.x), (int)(target.y)), 10, 0)

        # mover os alvos
        if targets_move_right : target.x += tank.vx * dt * 0.1
        else : target.x -= tank.vx * dt * 0.1

        # se houver colisão entre um alvo e o tanque, apresentar mensagem de jogo perdido
        if target.y >= tank.y and target.x >= tank.x and target.x <= tank.x + tank.width:
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

    #   apresentar número de balas no clip
    MSG_BULLETS = get_font(10).render("BULLETS: {}".format(tank.clip), True, WHITE, BLACK)
    win.blit(MSG_BULLETS, [WIN_WIDTH - 124, WIN_HEIGHT - 14])

    #   instrução de fechar o pgm
    win.blit(MSG_QUIT, [4, 4])

    #   se o jogo estiver em andamento, incrementar o timer de reload do tanque
    if dt != 0 : tank.inc_timer(0.015)

    time.sleep(0.015)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()