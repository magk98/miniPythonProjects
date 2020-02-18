import pygame, os

from model.Character import Character

dark_sky = (14, 15, 70)
red = (255, 10, 10)
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 200


class Ship(Character):
    def __init__(self, _x, _y, _speed, _gun_speed):
        super(Ship, self).__init__(_x, _y, _speed, _gun_speed)
        self.image_name = 'shiip.png'
        self.shots = []

    def shot(self, win):
        self.shots += [Ship.Shot(self.x + 8, self.y)]
        #pygame.draw.rect(win, red, (x, y, 4, 8))
        pygame.display.flip()
        self.draw(win)
        win.fill(dark_sky)

    class Shot:
        def __init__(self, _x, _y):
            self.x = _x
            self.y = _y

        def draw(self, win, ship):
            pygame.draw.rect(win, red, (self.x - 1, self.y, 4, 8))
            if self.y > SCREEN_HEIGHT:
                ship.shots.remove(self)

        def move(self):
            global SCREEN_HEIGHT, SCREEN_WIDTH
            x_diff, y_diff = 0, -8
            self.x += x_diff
            self.y += y_diff


