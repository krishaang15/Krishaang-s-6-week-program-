import pygame 
import sys

# Initialize Pygame 
pygame.init()

# Set screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Endless Car Game")

# Load the car image 
car_img = pygame.image.load("car.png")
car_width = 50
car_height = 100
car_img = pygame.transform.scale(car_img, (car_width, car_height))

# Player car starting position 
car_x = screen_width // 2 - car_width // 2 
car_y = screen_height - car_height - 20  # Near bottom 

# Enemy car setup (✅ moved OUTSIDE the loop!)
enemy_img = car_img
enemy_width = car_width 
enemy_height = car_height
enemy_x = 200
enemy_y = -enemy_height
enemy_speed = 5

# Clock for FPS 
clock = pygame.time.Clock()

# Game loop 
running = True
while running:
    clock.tick(60)

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # Player movement
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

    # Enemy movement
    enemy_y += enemy_speed
    if enemy_y > screen_height:
        enemy_y = -enemy_height
        enemy_x = 200  # You can randomize this later

    # Fill background
    screen.fill((50, 50, 50))

    # Draw cars
    screen.blit(car_img, (car_x, car_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))

    # Collision detection
    player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    if player_rect.colliderect(enemy_rect):
        print("💥 Crash! Game Over!")
        running = False

    # Update screen
    pygame.display.update()

# Quit
pygame.quit()
sys.exit()
