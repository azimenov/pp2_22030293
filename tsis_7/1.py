import pygame
import datetime
import os

CURRENT_TIME = datetime.datetime.now()

pygame.display.set_caption("MICKEY TIMER")
WIDTH, HEIGHT = 900, 650

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'micky.png')), (WIDTH, HEIGHT))

CLOCK_FOR_MINUTES = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'minutes.png')), (WIDTH, HEIGHT))

CLOCK_FOR_SECONDS = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'seconds.png')), (WIDTH, HEIGHT))

clock = pygame.time.Clock()
run = True
while run:
    WIN.blit(SPACE, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    CURRENT_TIME = datetime.datetime.now()
    
    ROT_CLOCK_FOR_MINUTES = pygame.transform.rotate(CLOCK_FOR_MINUTES, - CURRENT_TIME.minute * 6)
    new_rect = ROT_CLOCK_FOR_MINUTES.get_rect(center = CLOCK_FOR_MINUTES.get_rect(center = (WIDTH//2, HEIGHT//2)).center)
    WIN.blit(ROT_CLOCK_FOR_MINUTES, new_rect)

    ROT_CLOCK_FOR_SECONDS = pygame.transform.rotate(CLOCK_FOR_SECONDS, - 6 * CURRENT_TIME.second)
    new_rect_Sec = ROT_CLOCK_FOR_SECONDS.get_rect(center = CLOCK_FOR_SECONDS.get_rect(center = (WIDTH//2, HEIGHT//2)).center)
    WIN.blit(ROT_CLOCK_FOR_SECONDS, new_rect_Sec)
    
    clock.tick(1)
    pygame.display.flip()

pygame.quit()