import pygame
import random
import sys

#some modification

# Initialize pygame
pygame.init()

# Set the window size
window_size = (500, 500)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Snake")

# Set the dimensions of the snake
snake_block = 10
snake_speed = 30

# Set the colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Set the font
font = pygame.font.Font("freesansbold.ttf", 18)

# Create a function to draw the snake
def draw_snake(snake_list):
    for pos in snake_list:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], snake_block, snake_block))

# Create a function to display the score
def show_score(choice, color, font, size, x, y):
    score = font.render(choice, True, color)
    screen.blit(score, [x, y])

# Create a function to display the game over message
def game_over():
    show_score("Game Over", red, font, 20, (window_size[0]/3), (window_size[1]/3))
    pygame.display.update()
    pygame.time.delay(1000)
    pygame.quit()
    sys.exit()

# Create a function to create the initial snake
def create_snake():
    snake_initial = []
    for i in range(3):
        snake_initial.append([100-i*10, 100])
    return snake_initial

# Create a function to create the initial food
def create_food():
    x = random.randrange(1, (window_size[0]//snake_block)-4) * snake_block
    y = random.randrange(1, (window_size[1]//snake_block)-4) * snake_block

    food = [x, y]
    return food

# Set the initial direction of the snake
direction = 'RIGHT'
change_to = direction

# Create the initial snake
snake_list = create_snake()

# Create the initial food
food = create_food()

# Set the initial score to 0
score = 0

# Set the dimensions of the bricks
brick_size = 10

# Create a list to store the bricks
bricks = []

# Create a function to draw the bricks
def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(screen, red, pygame.Rect(brick[0], brick[1], brick_size, brick_size))

# Create a function to create the bricks
def create_bricks():
    # Set the gap size
    gap_size = 20

    # Create bricks along the top and bottom borders
    for i in range(0, window_size[0], brick_size + gap_size):
        bricks.append([i, 0])
        bricks.append([i, window_size[1] - brick_size])

    # Create bricks along the left and right borders
    for i in range(brick_size + gap_size, window_size[1] - brick_size, brick_size + gap_size):
        bricks.append([0, i])
        bricks.append([window_size[0] - brick_size, i])



# Create the bricks
create_bricks()

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If the new direction is not opposite to the current direction, change the direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Update the snake position
    if direction == 'UP':
        snake_list[0][1] -= 10
    if direction == 'DOWN':
        snake_list[0][1] += 10
    if direction == 'LEFT':
        snake_list[0][0] -= 10
    if direction == 'RIGHT':
        snake_list[0][0] += 10

    # If the snake has eaten the food, increase the score and create a new piece of food
    if snake_list[0] == food:
        score += 1
        food = create_food()
    else:
        snake_list.pop()

    # Check if the snake has collided with the wall or itself
    if snake_list[0][0] < 0:
        snake_list[0][0] = window_size[0] - snake_block
    elif snake_list[0][0] >= window_size[0]:
        snake_list[0][0] = 0
    elif snake_list[0][1] < 0:
        snake_list[0][1] = window_size[1] - snake_block
    elif snake_list[0][1] >= window_size[1]:
        snake_list[0][1] = 0

    for block in snake_list[1:]:
        if snake_list[0] == block:
            game_over()

    # Check if the snake has collided with a brick
    for brick in bricks:
        if snake_list[0] == brick:
            game_over()

    # Add the new snake position to the front of the snake
    snake_list.insert(0, list(snake_list[0]))

    # Clear the screen
    screen.fill(black)

    # Draw the bricks
    draw_bricks(bricks)

    # Draw the snake and the food
    draw_snake(snake_list)
    pygame.draw.rect(screen, white, pygame.Rect(food[0], food[1], snake_block, snake_block))

    # Display the score
    show_score("Score: " + str(score), white, font, 20, 0, 0)

    # Update the display
    pygame.display.update()

    # Set the frame rate
    pygame.time.delay(150 - (score*2))