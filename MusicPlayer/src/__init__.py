import pygame
from pathlib import Path
pygame.init()
win = pygame.display.set_mode((500, 400))

#Loading songs' names in "music" folder
pathList = Path('music').glob('**/*.mp3')
songs = []
for path in pathList:
    songs.append(str(path))
    print(str(path))

music = pygame.mixer.music.load(songs[0])
pygame.mixer.music.play()

running = True
paused = False
index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            paused = not paused
            if paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        if keys[pygame.K_r]:
            pygame.mixer.music.rewind()
        if keys[pygame.K_UP]:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
        if keys[pygame.K_DOWN]:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
        if keys[pygame.K_RIGHT]:
            index = (index + 1) % len(songs)
            pygame.mixer.music.load(songs[index])
            pygame.mixer.music.play()
        if keys[pygame.K_LEFT]:
            index = (index - 1) % len(songs)
            pygame.mixer.music.load(songs[index])
            pygame.mixer.music.play()


pygame.quit()
