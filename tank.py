class Tank:
    def __init__(self, x, y, width, height, vx, clip, clip_size, reload_duration):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.clip = clip
        self.clip_size = clip_size
        self.reload_duration = reload_duration
        self.reload_timer = 0

    def inc_timer(self, seconds):
        self.reload_timer += seconds
        if self.reload_timer > self.reload_duration:
            self.reload_timer = 0
            if self.clip < self.clip_size : self.clip += 1