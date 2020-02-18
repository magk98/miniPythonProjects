import os

import pygame

from model import Main
from model.Character import Character


class Ship(Character):
    def __init__(self, _x, _y, _speed, _gun_speed):
        super(Ship, self).__init__(_x, _y, _speed, _gun_speed)
        self.image_name = 'ship.png'
        self.shots = []
        self.health = 3

    def shot(self):
        self.shots += [Character.Shot(self.x + Main.SCREEN_WIDTH // 40, self.y)]
        self.draw()

    def draw_health(self):
        image = pygame.image.load(os.path.join('images', self.image_name))
        image = pygame.transform.scale(image, (Main.SCREEN_WIDTH // 40, Main.SCREEN_HEIGHT // 40)).convert_alpha()
        for i in range(0, self.health):
            Main.win.blit(image, (Main.SCREEN_WIDTH - (i + 2) * (Main.SCREEN_WIDTH // 40), 10))

