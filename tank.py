import pygame

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vx, clip, clip_size, reload_duration):
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
        self.powerup_desc = ""   # a mostrar na interface
        self.reload_duration = reload_duration
        self.reload_timer = 0
        self.sprite = pygame.image.load("./assets/tanque.png").convert_alpha()

    def incr_timer(self, seconds):
        self.reload_timer += seconds
        if self.reload_timer > self.reload_duration:
            self.reload_timer = 0
            if self.clip < self.clip_size : self.clip += 1