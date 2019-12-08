import pygame, math
from bullet import *

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vx, clip, clip_size, reload_duration, sprite):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.clip = clip
        self.clip_size = clip_size
        self.power = 0
        self.ang = 90
        self.bullet_type = "sb"  # small bullet
        self.reload_duration = reload_duration
        self.reload_timer = 0
        self.sprite = sprite
    
    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
    
    def shoot(self):
        x = math.ceil((int)(self.x) + ((int)(self.width) >> 1)) # centro do canhão
        y = self.y - 10 # dar ligeiro avanço à bala

        new_bullet = None

        if self.bullet_type == "sb" : new_bullet = SmallBullet(x, y)
        else:
            if   self.bullet_type == "lb" : new_bullet = LargeBullet(x, y)
            elif self.bullet_type == "mb" : new_bullet = MassiveBullet(x, y)
            elif self.bullet_type == "fb" : new_bullet = FastBullet(x, y)
            elif self.bullet_type == "br" : new_bullet = Boomerang(x, y, self.ang, self.power)

            self.bullet_type = "sb"     # repor as balas simples depois do powerup ser usado
            self.powerup_desc = ""      # limpar powerup da interface
            self.power = 0
            self.ang = 90

        self.clip -= 1  # remover a bala do clip

        return new_bullet
    
    def move_left(self):
        if self.x <= 1 : self.x = 1
        else : self.x -= self.vx
    
    def move_right(self, WIN_WIDTH):
        if self.x + self.width + 1 >= WIN_WIDTH : self.x = WIN_WIDTH - self.width - 1
        else : self.x += self.vx

    def charge_bullet(self):
        if self.power >= 100 : self.power = 100
        else : self.power += 2
    
    def incr_ang(self):
        if self.ang != 135 : self.ang += 1
    
    def decr_ang(self):
        if self.ang != 45 : self.ang -= 1

    def incr_timer(self, seconds):
        self.reload_timer += seconds
        if self.reload_timer > self.reload_duration:
            self.reload_timer = 0
            if self.clip < self.clip_size : self.clip += 1