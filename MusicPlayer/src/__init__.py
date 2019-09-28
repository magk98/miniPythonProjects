import pygame
pygame.init()
win = pygame.display.set_mode((500,480))
music = pygame.mixer.music.load('music/abc.mp3')
pygame.mixer.music.play(-1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
