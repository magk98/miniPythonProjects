import pygame, os

#alien = pygame.image.load(os.path.join('images', 'alien.png'))
from model.Character import Character

dark_sky = (14, 15, 70)
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 200


class Alien(Character):
    def __init__(self, _x, _y, _speed, _gun_speed):
        super(Alien, self).__init__(_x, _y, _speed, _gun_speed)
        self.image_name = 'alien.png'

    def move(self, x_diff, y_diff):
        global SCREEN_HEIGHT, SCREEN_WIDTH
        if 0 <= self.x + x_diff < SCREEN_WIDTH - 15 and 0 <= self.y + y_diff < SCREEN_HEIGHT - 15:
            self.x += x_diff
            self.y += y_diff

