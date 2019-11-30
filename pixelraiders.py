import pygame, time, sys, math, random, os
from pygame import K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_RETURN
from bullet import SmallBullet, LargeBullet, MassiveBullet, FastBullet
from target import WeakTarget, ToughTarget, StrongTarget, KnockbackTarget, instantiate_targets
from powerup import LB, MB, FB
from tank import Tank

# definir posição da janela no ecrã ao abrir o jogo
pos_x = pos_y = 100
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

tank = Tank((WIN_WIDTH >> 1) - 31, WIN_HEIGHT - 48, 62, 48, 10, 4, 4, 2)     # instancializar o tanque

# instancializar 10 alvos
targets.extend(instantiate_targets(21, 3, 20, 40, 40, 50, 6, WIN_WIDTH))

while True:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP and dt != 0 and tank.clip > 0:
            if event.key == pygame.K_SPACE: # ao premir espaço, instanciar uma bala a partir da posição do tanque
                x = math.ceil((int)(tank.x) + ((int)(tank.width) >> 1)) # centro do canhão
                y = tank.y - 10 # dar ligeiro avanço à bala

                tank.clip -= 1  # remover a bala do clip

                if   tank.bullet_type == "sb" : bullets.append(SmallBullet(x, y)); break
                elif tank.bullet_type == "lb" : bullets.append(LargeBullet(x, y))
                elif tank.bullet_type == "mb" : bullets.append(MassiveBullet(x, y))
                elif tank.bullet_type == "fb" : bullets.append(FastBullet(x, y))

                tank.bullet_type = "sb"     # repor as balas simples depois do powerup ser usado
                tank.powerup_desc = ""      # limpar powerup da interface

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
        targets_moving_right = True
        tank.x = (WIN_WIDTH >> 1) - 20
        tank.clip = 6
        tank.reload_timer = 0
        targets.extend(instantiate_targets(21, 3, 20, 40, 40, 50, 6, WIN_WIDTH))
        dt = 3


    # desenhar o tanque
    win.blit(tank.sprite, (tank.x, tank.y))

    # comportamento das balas
    for bullet in bullets:

        pygame.draw.circle(win, BLUE, ((int)(bullet.x), (int)(bullet.y)), bullet.radius, 0) # desenhar as balas

        if not targets : break  # se não houver alvos, o jogo está parado e as balas ficarão estáticas
                                # logo, não interessa estudar o seu comportamento e o ciclo é quebrado

        bullet.y -= bullet.vy * dt * 0.1 # mover as balas

        for target in targets:

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
            bullets.remove(bullet)                                          # remover a bala
            target.lose_hit_points(1)                                       # retirar um ponto de vida ao alvo
            if target.hit_points == 0:                                      # caso não lhe reste mais vida,
                targets.remove(target)                                      # remove-o da lista de alvos
                random_powerup = target.create_powerup()                    # gerar probabilidade de aparecer powerup
                if random_powerup: powerups.append(random_powerup)          # se aparecer, é adicionado à lista de powerups
                if len(targets) == 1 :                                      # se agora houver apenas um alvo,
                    targets[0].vx = targets[0].vx << 1                      # a sua velocidade duplica
                break                                   # como o alvo deixa de existir, não vê mais nenhuma condição

            # o alvo continua ativo
            target.update_color()                                           # a cor altera
            if hasattr(target, "knockback"): target.knockback(50, targets)  # e procura por outras reações do alvo
            break

        if bullet.y + bullet.radius <= 0: bullets.remove(bullet) # apagar as balas que saem da janela

    # comportamento dos alvos
    for target in targets:

        # desenhar alvos
        win.blit(target.sprite, (target.x, target.y))

        # mover os alvos
        if targets_moving_right : target.x += target.vx * dt * 0.1
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
        targets_moving_right = not targets_moving_right
    
    # comportamento dos powerups
    for powerup in powerups:

        # desenhar powerups
        win.blit(powerup.sprite, (powerup.x, powerup.y))

        powerup.move_down(2) # mover os powerups

        # contacto entre um powerup e o tanque
        if powerup.y >= tank.y and powerup.x >= tank.x and powerup.x <= tank.x + tank.width:
            tank.bullet_type = powerup.bullet_type
            tank.powerup_desc = powerup.desc # atualizar texto do indicador de powerup na interface
            powerups.remove(powerup)
            break
        
        if powerup.y + 10 <= 0: powerups.remove(powerup) # apagar os powerups que saem da janela

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

    #   instrução de fechar o pgm
    win.blit(MSG_QUIT, [4, 4])

    #   se o jogo estiver em andamento, incrementar o timer de reload do tanque
    if dt != 0 : tank.incr_timer(0.015)

    time.sleep(0.015)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()