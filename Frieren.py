import pygame
import random
import ctypes

# Initialize Pygame
pygame.init()

# Get the screen width and height of the monitor
user32 = ctypes.windll.user32
SCREEN_WIDTH, SCREEN_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Frieren's Snake Game")

# Load background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop the music

# Load Frieren image
frieren_img = pygame.image.load("frieren.png")
frieren_img = pygame.transform.scale(frieren_img, (70, 70))  # Double the size

# Load anime cover art
anime_cover_art = pygame.image.load("anime_cover_art.png")
anime_cover_art = pygame.transform.scale(anime_cover_art, (90, 90))  # Double the size

# Snake variables
block_size = 40  # Double the size
snake_speed = 15
clock = pygame.time.Clock()

# Define font
font = pygame.font.Font(None, 36)

def draw_snake(snake_list):
    for block in snake_list:
        screen.blit(frieren_img, block)

def draw_food(food_pos):
    screen.blit(anime_cover_art, food_pos)

def game_loop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2

    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    # Initial position of the food
    food_x = random.randrange(0, SCREEN_WIDTH - block_size, block_size)
    food_y = random.randrange(0, SCREEN_HEIGHT - block_size, block_size)
    food_pos = (food_x, food_y)

    while not game_over:
        while game_close:
            # Game over screen
            screen.fill((0, 0, 0))
            game_over_text = font.render("Frieren is Mid! Press Q to Quit or C to Play Again", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0

        # Move the snake
        x += x_change
        y += y_change

        # Check boundaries
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True

        # Draw the snake and food
        screen.fill((0, 0, 0))
        draw_snake(snake_list)
        draw_food(food_pos)
        pygame.display.update()

        # Update snake list
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake eats food
        if (food_pos[0] <= x < food_pos[0] + block_size) and (food_pos[1] <= y < food_pos[1] + block_size):
            food_x = random.randrange(0, SCREEN_WIDTH - block_size, block_size)
            food_y = random.randrange(0, SCREEN_HEIGHT - block_size, block_size)
            food_pos = (food_x, food_y)
            snake_length += 1

        # Check if snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
