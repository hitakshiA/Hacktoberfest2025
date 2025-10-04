import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

gravity = 0.5
bird_movement = 0
game_active = True
score = 0
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency

font = pygame.font.SysFont("Arial", 32)

bird = pygame.Rect(100, SCREEN_HEIGHT // 2, 34, 24)
pipes = []

def draw_bird():
    pygame.draw.rect(win, RED, bird)

def create_pipe():
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(SCREEN_WIDTH, height - pipe_gap - 400, 52, 400)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height, 52, 400)
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(win, GREEN, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return False
    if bird.top <= 0 or bird.bottom >= SCREEN_HEIGHT:
        return False
    return True

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird.center = (100, SCREEN_HEIGHT // 2)
                bird_movement = 0
                score = 0

    win.fill(BLUE)

    if game_active:
        bird_movement += gravity
        bird.centery += int(bird_movement)
        draw_bird()
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            last_pipe = time_now
            pipes.extend(create_pipe())
        pipes = move_pipes(pipes)
        draw_pipes(pipes)
        game_active = check_collision(pipes)
        for pipe in pipes:
            if pipe.centerx == bird.centerx:
                score += 0.5
        display_score(int(score))
    else:
        game_over_text = font.render("Game Over! Press SPACE to Restart", True, WHITE)
        win.blit(game_over_text, (25, SCREEN_HEIGHT // 2))

    pygame.display.update()
    clock.tick(60)
