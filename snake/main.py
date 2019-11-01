import pygame
import random, os

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 200
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
win.fill((255, 255, 255))

is_running = True
snake = [(40, 40)]
vel = 20
cherry = pygame.image.load(os.path.join('cherry.png'))
cherry_x, cherry_y = ((random.randint(0, SCREEN_WIDTH / vel - 1) * vel),
                      random.randint(0, SCREEN_HEIGHT / vel - 1) * vel)
direction = "east"


def draw_cherry():
    global cherry_x, cherry_y
    while (cherry_x, cherry_y) in snake:
        if (cherry_x, cherry_y) == snake[0]:
            eat_cherry()
        cherry_x, cherry_y = (random.randint(0, SCREEN_WIDTH / vel - 1) * vel,
                              random.randint(0, SCREEN_HEIGHT / vel - 1) * vel)
    win.blit(cherry, (cherry_x, cherry_y))


def eat_cherry():
    global cherry_x, cherry_y, snake
    x_dif, y_dif = 0, 0
    if direction == "east": x_dif = -vel
    if direction == "west": x_dif = vel
    if direction == "north": y_dif = vel
    if direction == "south": y_dif = -vel
    snake += [(cherry_x + x_dif, cherry_y + y_dif)]
    cherry_x, cherry_y = (random.randint(0, SCREEN_WIDTH / vel - 1) * vel,
                          random.randint(0, SCREEN_HEIGHT / vel - 1) * vel)


def move_snake(surface):
    global snake, direction, vel
    (x, y) = snake[0]
    if direction == "west":
        snake = [((x - vel) % SCREEN_WIDTH, y)] + snake
    if direction == "east":
        snake = [((x + vel) % SCREEN_WIDTH, y)] + snake
    if direction == "north":
        snake = [(x, (y - vel) % SCREEN_HEIGHT)] + snake
    if direction == "south":
        snake = [(x, (y + vel) % SCREEN_HEIGHT)] + snake
    del snake[-1]

    for (x, y) in snake:
        pygame.draw.rect(surface, (21, 126, 0), (x, y, vel, vel))
    pygame.draw.rect(surface, (21, 45, 0), (snake[0][0], snake[0][1], vel, vel))
    pygame.display.flip()
    win.fill((255, 255, 255))


def change_dir(arrow):
    global direction
    if arrow.key == pygame.K_RIGHT and direction not in ["west", "east"]:
        direction = "east"
    elif arrow.key == pygame.K_LEFT and direction not in ["west", "east"]:
        direction = "west"
    elif arrow.key == pygame.K_UP and direction not in ["north", "south"]:
        direction = "north"
    elif arrow.key == pygame.K_DOWN and direction not in ["north", "south"]:
        direction = "south"


def is_collision():
    global snake
    head = snake[0]
    times = 0
    for coords in snake:
        if coords == head: times += 1
    return True if times > 1 else False


def main():
    global win, is_running
    while is_running:
        pygame.time.delay(350)

        if is_collision():
            win.fill((255, 255, 255))
            font = pygame.font.SysFont('Arial', 20)
            text = 'game over :( {} points'.format(len(snake))
            txt_surface = font.render(text, True, (0, 0, 255))
            win.blit(txt_surface, (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 3))
            pygame.display.flip()
            pygame.time.delay(3000)
            is_running = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    change_dir(event)

            move_snake(win)
            draw_cherry()

    pygame.quit()


if __name__ == '__main__':
    main()
