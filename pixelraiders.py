import pygame, time, sys, math, random
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_RETURN
from bullet import SmallBullet, LargeBullet, MassiveBullet, FastBullet
from target import WeakTarget, ToughTarget, StrongTarget, KnockbackTarget, instantiate_targets
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

tank = Tank((WIN_WIDTH >> 1) - 20, WIN_HEIGHT - 20, 31, 24, 10, 6, 6, 1.5)     # instancializar o tanque

# instancializar 10 alvos
targets.extend(instantiate_targets(10, 20, 40, 40, 50, WIN_WIDTH, WIN_HEIGHT, 6))

while True:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP and dt != 0 and tank.clip > 0:
            if event.key == pygame.K_SPACE: # ao premir espaço, instanciar uma bala a partir da posição do tanque
                x = math.ceil((int)(tank.x) + ((int)(tank.width) >> 1)) # centro do canhão
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
        tank.x = (WIN_WIDTH >> 1) - 20
        tank.clip = 6
        tank.reload_timer = 0
        targets.extend(instantiate_targets(10, 20, 40, 40, 50, WIN_WIDTH, WIN_HEIGHT, 6))
        dt = 3


    # desenhar o tanque
    win.blit(tank.sprite, (tank.x, tank.y))

    # comportamento das balas
    for bullet in bullets:

        pygame.draw.circle(win, BLUE, ((int)(bullet.x), (int)(bullet.y)), bullet.radius, 0) # desenhar as balas

        if not targets : break  # se não houver alvos, o jogo está parado e as balas ficarão estáticas
                                # logo, não interessa estudar o seu comportamento e o ciclo é quebrado

        bullet.y -= bullet.vy * dt * 0.1 # mover as balas

        for target in targets:                                                  # para cada alvo
            if (bullet.y >= target.y and bullet.y <= target.y + target.height   # se uma bala está à mesma altitude dos alvos
            and bullet.x >= target.x and bullet.x <= target.x + target.width):  # verifica se a bala se sobrepõe a algum
                bullets.remove(bullet)                                          # se sim, remove a bala
                target.lose_hit_points(1)                                       # e retira um ponto de vida ao alvo
                if target.hit_points == 0:                                      # caso não reste mais vida ao alvo,
                    targets.remove(target)                                      # remove-o
                    if len(targets) == 1 : targets[0].vx = targets[0].vx << 1   # se só sobrar um alvo, duplica o seu vx
                    break                                                       # e não vê mais nenhuma condição
                target.update_color()                                           # caso contrário, a cor altera
                if hasattr(target, "knockback"): target.knockback(50, targets)  # e procura por outras reações do alvo
                break

        if bullet.y <= 0: bullets.remove(bullet) # apagar as balas que saem da janela

    # comportamento dos alvos
    for target in targets:

        # desenhar alvos
        win.blit(target.sprite, (target.x, target.y))

        # mover os alvos
        if targets_move_right : target.x += target.vx * dt * 0.1
        else : target.x -= target.vx * dt * 0.1

        # se houver colisão entre um alvo e o tanque, apresentar mensagem de jogo perdido
        if target.y >= tank.y and target.x >= tank.x and target.x <= tank.x + tank.width:
            dt = 0
            win.blit(
                MSG_GAMEOVER,
                # centrar na janela
                [ (WIN_WIDTH >> 1) - (MSG_GAMEOVER.get_width() >> 1), (WIN_HEIGHT >> 1) - (MSG_GAMEOVER.get_height() >> 1) ]
            )
            win.blit(
                MSG_NEWGAME,
                # centrar no eixo dos x                         centrar no eixo dos y e empurrar para baixo 50px
                [ (WIN_WIDTH >> 1) - (MSG_NEWGAME.get_width() >> 1), (WIN_HEIGHT >> 1) - (MSG_NEWGAME.get_height() >> 1) + 50 ]
            )

        border = 20    # afastamento das paredes laterais da janela

        # quando os alvos chegam ao extremo direito do ecrã
        if target.x + target.width >= WIN_WIDTH - border:
            targets_move_down = True

        # quando os alvos chegam ao extremo esquerdo do ecrã
        if target.x <= border:
            targets_move_down = True

    # se um alvo chegou a um extremo, aumentar ordenadas de todos os alvos e mudar a sua direção
    if targets_move_down:
        for target in targets: target.y += 50
        targets_move_down = False
        targets_move_right = not targets_move_right

    if not targets:     # se não houver alvos, apresentar mensagem de jogo ganho
        dt = 0
        win.blit(
            MSG_YOUWIN,
            [ (WIN_WIDTH >> 1) - (MSG_YOUWIN.get_width() >> 1), (WIN_HEIGHT >> 1) - (MSG_YOUWIN.get_height() >> 1) ] # centrar na janela
        )
        win.blit(
            MSG_NEWGAME,
            # centrar no eixo dos x                         centrar no eixo dos y e empurrar para baixo 50px
            [ (WIN_WIDTH >> 1) - (MSG_NEWGAME.get_width() >> 1), (WIN_HEIGHT >> 1) - (MSG_NEWGAME.get_height() >> 1) + 50 ]
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