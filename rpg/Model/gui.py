import pygame
import os, sys
import random
from Characters import Character
from Places import Map

#pygame initialization
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 240, 240
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("RPG")
font = pygame.font.SysFont('Arial', 20)

#animation images
background_image = pygame.image.load(os.path.join('images', 'map1.png'))
battle_image = pygame.image.load(os.path.join('images', 'battle.png'))
standing = pygame.image.load(os.path.join('images', 'dawn', 'standing.png'))
walk_right = [pygame.image.load(os.path.join('images', 'dawn', 'R1.png')), pygame.image.load(os.path.join('images', 'dawn', 'R2.png')), pygame.image.load(os.path.join('images', 'dawn', 'R3.png')), pygame.image.load(os.path.join('images', 'dawn', 'R1.png'))]
walk_left = [pygame.image.load(os.path.join('images', 'dawn', 'L1.png')), pygame.image.load(os.path.join('images', 'dawn', 'L2.png')), pygame.image.load(os.path.join('images', 'dawn', 'L3.png')), pygame.image.load(os.path.join('images', 'dawn', 'L1.png'))]
walk_up = [pygame.image.load(os.path.join('images', 'dawn', 'U3.png')), pygame.image.load(os.path.join('images', 'dawn', 'U1.png')), pygame.image.load(os.path.join('images', 'dawn', 'U2.png')), pygame.image.load(os.path.join('images', 'dawn', 'U3.png'))]
walk_down = [pygame.image.load(os.path.join('images', 'dawn', 'standing.png')), pygame.image.load(os.path.join('images', 'dawn', 'D1.png')), pygame.image.load(os.path.join('images', 'dawn', 'D2.png')), pygame.image.load(os.path.join('images', 'dawn', 'standing.png'))]


#map variables
trees = [(0, 0), (40, 200), (200, 0)]
bushes = [(0, 40), (0, 80), (0, 120), (0, 160), (40, 40), (40, 80), (40, 120), (40, 160)]
enemies = [Character.Enemy("Pikachu", 20, 5, 2, exp=10), Character.Enemy("Rattata", 10, 2, 1, exp=4)]


#program variables
is_running = True
x, y = 40, 0
vel = 40
left = False
right = False
up = False
down = False
walkCount = 0
battle = False


def encounter(enemy):
    global win, battle, battle_image
    text = font.render('Wild {} appeared!'.format(enemy.name), True, (0, 0, 0))
    for j in range(12):
        for i in range(0, 12, 2):
            pygame.draw.rect(win, (0, 0, 0), (j * 20, i * 20, 20, 20))
            pygame.draw.rect(win, (0, 0, 0), (220 - j * 20, (i + 1) * 20, 20, 20))
            pygame.display.update()
            pygame.time.delay(30)
    win.blit(battle_image, (0, 0))
    win.blit(pygame.image.load(os.path.join('images', 'pokemon', enemy.name + '.png')), (145, 60))
    win.blit(text, (20, 190))
    pygame.display.update()
    pygame.time.delay(50)



def redrawGameWindow():
    global walkCount
    global x, y

    for i in range(4):
        pygame.display.update()
        win.blit(background_image, (0, 0))
        if walkCount + 1 >= 4:
            walkCount = 0
        if left:
            win.blit(walk_left[walkCount], (x, y))
            walkCount += 1
            if (x - vel, y) not in trees:
                x -= 0.25 * vel
        elif right:
            win.blit(walk_right[walkCount], (x, y))
            walkCount += 1
            if (x + vel, y) not in trees:
                x += 0.25 * vel
        elif up:
            win.blit(walk_up[walkCount], (x, y))
            walkCount += 1
            if (x, y - vel) not in trees:
                y -= 0.25 * vel
        elif down:
            win.blit(walk_down[walkCount], (x, y))
            walkCount += 1
            if (x, y + vel) not in trees:
                y += 0.25 * vel
        else:
            win.blit(standing, (x, y))
            walkCount = 0
            pygame.display.update()


def main():
    global win, is_running, battle
    global x, y
    global left, right, up, down, walkCount
    rand = 0

    is_running = True

    while is_running:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
                elif event.button == 3:
                    pass

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            encounter()
            battle = not battle

        if keys[pygame.K_LEFT] and x >= vel:
            left = True
            right = False
            down = False
            up = False
            rand = random.randint(0, 10)
        elif keys[pygame.K_RIGHT] and x <= SCREEN_WIDTH - 2 * vel:
            left = False
            right = True
            down = False
            up = False
            rand = random.randint(0, 10)
        elif keys[pygame.K_UP] and y >= vel:
            left = False
            right = False
            down = False
            up = True
            rand = random.randint(0, 10)
        elif keys[pygame.K_DOWN] and y <= SCREEN_HEIGHT - 2 * vel:
            left = False
            right = False
            down = True
            up = False
            rand = random.randint(0, 10)
        else:
            left = False
            right = False
            down = False
            up = False
            walkCount = 0

        if not battle and (x, y) in bushes and rand <= 2:
            battle = True
            encounter(random.choices(enemies, k=1, weights=[0.2, 0.8])[0])
            rand = random.randint(0, 10)

        if not battle:
            redrawGameWindow()
        pygame.time.delay(120)

    pygame.quit()


if __name__ == '__main__':
    main()
