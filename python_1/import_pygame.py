import pygame
import sys
import random
import os

pygame.init()

# Screen setup
screen_width = 261
screen_height = 375
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Endless Car Game")

# Load and scale car image
car_img = pygame.image.load("car.png")
car_width = 40
car_height = 80
car_img = pygame.transform.scale(car_img, (car_width, car_height))

# Lane setup
num_lanes = 3
lane_width = screen_width // num_lanes
lane_color = (255, 255, 255)
lane_line_height = 20
lane_line_spacing = 30

# Fonts
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 36)

# High score load
high_score = 0
if os.path.exists("highscore.txt"):
    try:
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    except:
        high_score = 0

# Clock
clock = pygame.time.Clock()

# Function to reset game
def reset_game():
    global car_x, car_y, enemies, score, level, last_level_up, show_level_up_timer
    car_x = screen_width // 2 - car_width // 2
    car_y = screen_height - car_height - 20
    enemies = []
    for _ in range(3):
        lane = random.randint(0, num_lanes - 1)
        x = lane * lane_width + lane_width // 2 - car_width // 2
        y = random.randint(-600, -car_height)
        enemies.append([x, y])
    score = 0
    level = 1
    last_level_up = 1
    show_level_up_timer = 0

reset_game()
paused = False
game_over = False

# Game loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if replay_button.collidepoint(mouse_x, mouse_y):
                game_over = False
                reset_game()

    if paused or game_over:
        # Display paused or game over screen
        screen.fill((30, 30, 30))
        if paused:
            pause_text = big_font.render("Paused", True, (255, 255, 0))
            screen.blit(pause_text, (screen_width // 2 - 50, screen_height // 2 - 20))
        elif game_over:
            game_over_text = big_font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - 70, screen_height // 2 - 60))

            hs_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
            screen.blit(hs_text, (screen_width // 2 - 60, screen_height // 2 - 20))

            # Draw Replay button
            replay_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 10, 100, 35)
            pygame.draw.rect(screen, (0, 200, 0), replay_button, border_radius=6)
            replay_text = font.render("Replay", True, (255, 255, 255))
            screen.blit(replay_text, (replay_button.x + 25, replay_button.y + 8))

        pygame.display.update()
        continue

    # --- Game running ---
    score += 1
    level = 1 + (score // 300)
    enemy_speed = 5 + (level - 1)

    if level > last_level_up:
        show_level_up_timer = 60
        last_level_up = level
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= 5
    if keys[pygame.K_RIGHT]:
        car_x += 5

    car_x = max(0, min(screen_width - car_width, car_x))
    screen.fill((50, 50, 50))

    # Draw lanes
    for i in range(1, num_lanes):
        lane_x = i * lane_width
        for y in range(0, screen_height, lane_line_height + lane_line_spacing):
            pygame.draw.rect(screen, lane_color, (lane_x - 2, y, 4, lane_line_height))

    # Enemies
    for i in range(len(enemies)):
        enemies[i][1] += enemy_speed
        if enemies[i][1] > screen_height:
            lane = random.randint(0, num_lanes - 1)
            x = lane * lane_width + lane_width // 2 - car_width // 2
            enemies[i] = [x, -car_height]
        screen.blit(car_img, (enemies[i][0], enemies[i][1]))

    # Player
    screen.blit(car_img, (car_x, car_y))

    # Score + high score
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, screen_height - 30))
    screen.blit(font.render(f"High: {high_score}", True, (255, 255, 0)), (screen_width - 90, screen_height - 30))

    # Level bar
    bar_width = 100
    bar_height = 8
    bar_x = screen_width // 2 - bar_width // 2
    bar_y = 10
    pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
    progress = (score % 300) / 300
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
    screen.blit(font.render(f"Level {level}", True, (255, 255, 0)), (bar_x + bar_width + 10, bar_y - 2))

    # Level up message
    if show_level_up_timer > 0:
        screen.blit(font.render("LEVEL UP!", True, (255, 255, 0)), (screen_width // 2 - 60, screen_height // 2 - 100))
        show_level_up_timer -= 1

    # Collision detection
    shrink_x = 10
    shrink_y = 20
    player_rect = pygame.Rect(car_x + shrink_x // 2, car_y + shrink_y // 2, car_width - shrink_x, car_height - shrink_y)

    for enemy_x, enemy_y in enemies:
        enemy_rect = pygame.Rect(enemy_x + shrink_x // 2, enemy_y + shrink_y // 2, car_width - shrink_x, car_height - shrink_y)
        if player_rect.colliderect(enemy_rect):
            game_over = True
            paused = False
            if score > high_score:
                high_score = score
                with open("highscore.txt", "w") as file:
                    file.write(str(high_score))
            break

    pygame.display.update()

pygame.quit()
sys.exit()
