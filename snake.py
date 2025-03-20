import pygame
import time
import random


pygame.init()


width = 600
height = 400


black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)


snake_block = 10

snake_speed = 15

font = pygame.font.SysFont("bahnschrift", 20)

# Create game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snakes By Eklavya")


try:
    icon = pygame.image.load("Electra.png")
    pygame.display.set_icon(icon)
except pygame.error:
    print("Favicon not found! Make sure 'favicon.png' is in the same directory.")

# Clock
clock = pygame.time.Clock()

try:
    with open("highscore.txt", "r") as f:
        highest_score = int(f.read())  # Read the stored highest score
except FileNotFoundError:
    highest_score = 0  # If no file exists, start with 0


def show_score(score, highest_score):
    score_value = font.render(f"Score: {score}", True, white)
    high_score_value = font.render(f"Highest Score: {highest_score}", True, white)
    screen.blit(score_value, [10, 10])
    screen.blit(high_score_value, [10, 30])


def draw_snake(snake_block, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], snake_block, snake_block])

# Game loop
def game_loop():
    global highest_score  # Use the global highest_score variable
    game_over = False
    game_close = False

    # Initial snake position
    x = width / 2
    y = height / 2

    # Movement direction
    dx = 0
    dy = 0

    # Snake body
    snake_list = []
    length_of_snake = 1

    # Food position
    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            screen.fill(black)
            msg = font.render("Game Over! Press R to Restart or Q to Quit", True, red)
            screen.blit(msg, [width / 6, height / 3])
            show_score(length_of_snake - 1, highest_score)
            pygame.display.update()

            # Update highest score if current score is greater
            if (length_of_snake - 1) > highest_score:
                highest_score = length_of_snake - 1
                with open("highscore.txt", "w") as f:
                    f.write(str(highest_score))  # Save the new highest score

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()  # Restart the game

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -snake_block
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = snake_block
                    dy = 0
                elif event.key == pygame.K_UP:
                    dx = 0
                    dy = -snake_block
                elif event.key == pygame.K_DOWN:
                    dx = 0
                    dy = snake_block

        # Boundary conditions (if the snake hits the walls)
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += dx
        y += dy
        screen.fill(black)

        # Draw food
        pygame.draw.rect(screen, red, [food_x, food_y, snake_block, snake_block])

        # Update snake body
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if snake collides with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        show_score(length_of_snake - 1, highest_score)
        pygame.display.update()

        # Check if the snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        # Set speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
game_loop()
