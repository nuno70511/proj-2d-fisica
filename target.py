class Target:
    _targets = []

    def __init__(self, x, y):
        self._targets.append(self)
        self.x = x
        self.y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    def x(self, x):
        self._x = x

    def y(self, y):
        self._y = y