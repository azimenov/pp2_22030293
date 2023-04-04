import pygame
import os

pygame.init()
pygame.mixer.init()
pygame.font.init()


WIDTH, HEIGHT = 400, 400

BLACK = (0, 0, 0)

songs = []

pygame.display.set_caption("MUSIC PLAYER")
os.chdir('Assets')
for song in os.listdir():
    if song.endswith('mp3'):
        songs.append(song)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

current_song = 0
music = pygame.mixer.Sound(songs[current_song])
music.play()
run = True
playing = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE] and playing:
        music.stop()
        playing = False
    elif keys_pressed[pygame.K_s] and not playing:
        music.play()
        playing = True
    elif keys_pressed[pygame.K_LEFT] :
        music.stop()
        current_song -= 1
        current_song = current_song % len(songs)
        music = pygame.mixer.Sound(songs[current_song])
        music.play()
    elif keys_pressed[pygame.K_RIGHT]:
        music.stop()
        current_song += 1
        current_song = current_song % len(songs)
        music = pygame.mixer.Sound(songs[current_song])
        music.play()
    
    WIN.fill(BLACK)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
     