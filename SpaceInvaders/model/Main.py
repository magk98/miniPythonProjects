import random

import pygame

from model import Level
from model.Character import Character
from model.Ship import Ship

#game variables
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
dark_sky = (14, 15, 70)
red = (255, 10, 10)
green = (10, 255, 10)
#window init
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders')
win.fill(dark_sky)
font = pygame.font.Font('freesansbold.ttf', 32)


is_running = True
alien_left_move = False


def main():
    global is_running, alien_left_move
    ship = Ship(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30, 10, 10)
    ship.draw()
    shot_counter = 0
    level = Level.Level(1)
    while is_running:
        pygame.time.delay(40)
        shot_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                is_running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            ship.move(10, 0)
        if keys[pygame.K_LEFT]:
            ship.move(-10, 0)
        if keys[pygame.K_UP]:
            ship.move(0, -10)
        if keys[pygame.K_DOWN]:
            ship.move(0, 10)

        level.draw_components(ship)

        if level.alive_aliens:
            if shot_counter % 10 == 0:
                ship.shot()
            if shot_counter % 20 == 5:
                level.move_aliens(alien_left_move, False)
                alien_left_move = not alien_left_move
            if shot_counter % 40 == 20:
                alien = random.choice(level.alive_aliens)
                level.alien_shots += [Character.Shot(alien.x + SCREEN_WIDTH // 40, alien.y + SCREEN_HEIGHT // 30)]
            if shot_counter % 50 == 0:
                level.move_aliens(False, True)
        if not level.alive_aliens:
            level = Level.Level(level.number + 1, level.score)

        level.check_collision(ship)

    pygame.quit()


if __name__ == '__main__':
    main()
