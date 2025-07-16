# This code is for a game called endless race where there is a car racing past the enemy cars
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 225
screen_height = 375
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Endless Car Game")

# Load and scale car image
car_img = pygame.image.load("car.png")
car_width = 40
car_height = 80
car_img = pygame.transform.scale(car_img, (car_width, car_height))

# Player car position
car_x = screen_width // 2 - car_width // 2
car_y = screen_height - car_height - 20

# Enemy setup
enemy_img = car_img
num_enemies = 3
enemies = []
for _ in range(num_enemies):
    x = random.randint(0, screen_width - car_width)
    y = random.randint(-600, -car_height)
    enemies.append([x, y])

# Fonts and score/level
font = pygame.font.SysFont(None, 24)
score = 0
level = 1
last_level_up = 1
show_level_up_timer = 0

# Clock
clock = pygame.time.Clock()

# Game over display
def show_game_over():
    game_over_text = font.render("Crash! Game Over!", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 - 80, screen_height // 2 - 20))
    screen.blit(score_text, (screen_width // 2 - 50, screen_height // 2 + 10))
    pygame.display.update()
    pygame.time.delay(2000)

# Game loop
running = True
while running:
    clock.tick(60)
    score += 1
    level = 1 + (score // 300)
    enemy_speed = 5 + (level - 1)

    if level > last_level_up:
        show_level_up_timer = 60  # Show for 1 second (60 frames)
        last_level_up = level

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= 5
    if keys[pygame.K_RIGHT]:
        car_x += 5

    # Keep player on screen
    if car_x < 0:
        car_x = 0
    if car_x > screen_width - car_width:
        car_x = screen_width - car_width

    # Background
    screen.fill((50, 50, 50))

    # Move and draw enemies
    for i in range(len(enemies)):
        enemies[i][1] += enemy_speed
        if enemies[i][1] > screen_height:
            enemies[i][1] = -car_height
            enemies[i][0] = random.randint(0, screen_width - car_width)
        screen.blit(enemy_img, (enemies[i][0], enemies[i][1]))

    # Draw player
    screen.blit(car_img, (car_x, car_y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, screen_height - 30))

    # Draw level bar
    bar_width = 100
    bar_height = 8
    bar_x = screen_width // 2 - bar_width // 2
    bar_y = 10

    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))  # background bar
    progress = (score % 300) / 300
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))

    level_text = font.render(f"Level {level}", True, (255, 255, 0))
    screen.blit(level_text, (bar_x + bar_width + 10, bar_y - 2))

    # Show LEVEL UP! message
    if show_level_up_timer > 0:
        level_up_text = font.render("LEVEL UP!", True, (255, 255, 0))
        screen.blit(level_up_text, (screen_width // 2 - 60, screen_height // 2 - 100))
        show_level_up_timer -= 1

    # Collision detection (reduced hitboxes)
    shrink_x = 10
    shrink_y = 20
    player_rect = pygame.Rect(
        car_x + shrink_x // 2,
        car_y + shrink_y // 2,
        car_width - shrink_x,
        car_height - shrink_y)

    for enemy_x, enemy_y in enemies:
        enemy_rect = pygame.Rect
        (enemy_x + shrink_x // 2,
    enemy_y + shrink_y // 2,
    car_width - shrink_x,
    car_height - shrink_y)
            
        

        if player_rect.colliderect(enemy_rect):
            show_game_over()
            running = False

    # Update screen
    pygame.display.update()

# Quit game
pygame.quit()
sys.exit()
