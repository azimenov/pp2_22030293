       
import pygame
import os

WIDTH, HEIGHT = 600, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BALL")
ball_radius = 25
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_color = (255, 0, 0)

WHITE = (255,255,255)

FPS = 60
VEL = 20

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a] and ball_x - VEL > 0:  # LEFT
        ball_x -= VEL
    if keys_pressed[pygame.K_d] and ball_x + VEL + ball_radius < WIDTH:  # RIGHT
        ball_x += VEL
    if keys_pressed[pygame.K_w] and ball_y - VEL> 0:  # UP
        ball_y -= VEL
    if keys_pressed[pygame.K_s] and ball_y + VEL - ball_radius//2 < HEIGHT - 15:  # DOWN
        ball_y += VEL
        
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()