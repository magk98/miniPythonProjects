import pygame, os

dark_sky = (14, 15, 70)
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 200


class Character:
    def __init__(self, _x, _y, _speed, _gun_speed):
        self.x = _x
        self.y = _y
        self.speed = _speed
        self.gun = _gun_speed
        self.image_name = ''

    def move(self, x_diff, y_diff):
        global SCREEN_HEIGHT, SCREEN_WIDTH
        if 0 <= self.x + x_diff < SCREEN_WIDTH - 15 and 0 <= self.y + y_diff < SCREEN_HEIGHT - 15:
            self.x += x_diff
            self.y += y_diff

    def draw(self, win):
        image = pygame.image.load(os.path.join('images', self.image_name))
        win.blit(image, (self.x, self.y))
        pygame.display.flip()
        win.fill(dark_sky)
