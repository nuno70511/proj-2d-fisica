import pygame, time, sys, math, random, os
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_RETURN, K_UP, K_DOWN
from bullet import *
from target import *
from powerup import LB, MB, FB, BR
from tank import Tank

# definir posição da janela no ecrã ao abrir o jogo
pos_x, pos_y = 100, 50
os.environ["SDL_VIDEO_WINDOW_POS"] = "{},{}".format(pos_x, pos_y)

pygame.init()
pygame.display.set_caption("Pixel Raiders")

WIN_WIDTH = 900; WIN_HEIGHT = 675
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

dt = 3                              #   delta tempo
bullets = []                        #   guarda as instâncias das balas
powerups = []                       #   guarda as instâncias dos powerups
targets = []                        #   guarda as instâncias dos alvos
targets_moving_right = True         #   condição de os alvos estarem a mover-se para a direita
targets_move_down = False           #   condição de os alvos moverem-se para baixo

tank = Tank((WIN_WIDTH >> 1) - 31, WIN_HEIGHT - 48, 62, 48, dt, 4, 4, 2)     # instancializar o tanque

# instancializar 10 alvos
targets.extend(instantiate_targets(18, 3, 20, 40, 40, 50, 6, WIN_WIDTH))

while True:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP and dt != 0 and tank.clip > 0:
            if event.key == pygame.K_SPACE: # ao premir espaço, instanciar uma bala a partir da posição do tanque
                bullets.extend(tank.shoot())

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_LEFT] and dt != 0: # mover o tanque para a esquerda
        tank.move_left()
    if key_pressed[K_RIGHT]  and dt != 0: # mover o tanque para a direita
        tank.move_right(WIN_WIDTH)
    if key_pressed[K_SPACE] and tank.bullet_type == "br":
        tank.charge_bullet()
    if key_pressed[K_UP] and tank.bullet_type == "br":
        tank.incr_ang()
    if key_pressed[K_DOWN] and tank.bullet_type == "br":
        tank.decr_ang()
    if key_pressed[K_ESCAPE]:   # se ESC premido, sair do jogo
        pygame.quit()
        sys.exit()
    if key_pressed[K_RETURN] and dt == 0:   # se ENTER premido e o jogo estiver terminado, começar novo jogo
        bullets = []
        powerups = []
        targets = []
        targets_moving_right = True
        tank.x = (WIN_WIDTH >> 1) - 20
        tank.clip = 4
        tank.reload_timer = 0
        tank.bullet_type = "sb"
        tank.powerup_desc = ""
        targets.extend(instantiate_targets(18, 3, 20, 40, 40, 50, 6, WIN_WIDTH))
        dt = 3


    # desenhar o tanque
    tank.draw(win)

    # comportamento das balas
    for bullet in bullets:

        bullet.draw(win) # desenhar as balas

        if not targets : break  # se não houver alvos, o jogo está parado e as balas ficarão estáticas
                                # logo, não interessa estudar o seu comportamento e o ciclo é quebrado

        bullet.move(dt) # mover as balas

        # devolve o índice do alvo de contacto ou -1 se não houver interseção
        contact_index_of_target = bullet.look_for_contact(bullet, targets)

        if contact_index_of_target != -1:
            target = targets[contact_index_of_target]

            if bullet.pierce == 0 : bullets.remove(bullet) # se a bala estiver desgastada, desaparece

            if target.hit_points == 0:                              # caso o alvo perca toda a sua vida,
                targets.remove(target)                              # é removido da lista de alvos
                random_powerup = target.create_powerup()            # e é gerada uma probabilidade de aparecer powerup
                if random_powerup: powerups.append(random_powerup)  # se aparecer, é adicionado à lista de powerups
                if len(targets) == 1 :                              # se agora houver apenas um alvo,
                    targets[0].vx = targets[0].vx << 1              # a sua velocidade duplica
                break
        
            # o alvo continua ativo
            target.update(targets)
            break

        # apagar as balas que saem da janela
        if bullet.is_out_of_bounds(WIN_HEIGHT, WIN_WIDTH) : bullets.remove(bullet)

    # comportamento dos alvos
    for target in targets:

        # desenhar alvos
        target.draw(win)

        # mover os alvos
        if targets_moving_right : target.move_right(dt)
        else : target.move_left(dt)

        # se houver colisão entre um alvo e o tanque, apresentar mensagem de jogo perdido
        if target.hit_tank(tank.x, tank.y, tank.width):
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

        # quando os alvos chegam a um extremo da janela
        if target.hit_border(WIN_WIDTH, 20):
            targets_move_down = True

    # se um alvo chegou a um extremo, aumentar ordenadas de todos os alvos e mudar a sua direção
    if targets_move_down:
        for target in targets: target.move_down(50)
        targets_move_down = False
        targets_moving_right = not targets_moving_right
    
    # comportamento dos powerups
    for powerup in powerups:

        # desenhar powerups
        powerup.draw(win)

        powerup.move_down(2) # mover os powerups

        # contacto entre um powerup e o tanque
        if powerup.collected(tank.x, tank.y, tank.width):
            tank.bullet_type = powerup.bullet_type
            tank.powerup_desc = powerup.desc # atualizar texto do indicador de powerup na interface
            powerups.remove(powerup)
            break
        
        if powerup.is_out_of_bounds(WIN_HEIGHT): powerups.remove(powerup) # apagar os powerups que saem da janela

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

    #   apresentar powerup equipado (se houver)
    if tank.bullet_type != "sb":
        MSG_POWERUP = get_font(10).render("POWERUP: {}".format(tank.powerup_desc), True, WHITE, BLACK)
        win.blit(MSG_POWERUP, [4, WIN_HEIGHT - 14])

        if tank.bullet_type == "br":
            MSG_CHARGE = get_font(14).render("CHARGE: {}% ANG: {}".format((int)(tank.power), tank.ang), True, WHITE, BLACK)
            win.blit(MSG_CHARGE, [304, WIN_HEIGHT - 14])

    #   instrução de fechar o pgm
    win.blit(MSG_QUIT, [4, 4])

    #   se o jogo estiver em andamento, incrementar o timer de reload do tanque
    if dt != 0 : tank.incr_timer(0.015)

    time.sleep(0.015)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()