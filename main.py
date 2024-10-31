import pygame
from sys import exit
import random

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 40)

# Load graphics
background_surf = pygame.Surface((800, 600)).convert()
paddle_surf = pygame.image.load('graphics/paddle.png').convert_alpha()
paddle_surf = pygame.transform.rotozoom(paddle_surf, 0, 1.5)
paddle_rect = paddle_surf.get_rect(midbottom=(400, 580))
ball_surf = pygame.image.load('graphics/ball.png').convert_alpha()
ball_surf = pygame.transform.rotozoom(ball_surf, 0, 2)
ball_rect = ball_surf.get_rect(center=(400, 545))
text_surf = font.render('000', False, (99, 155, 255))
text_rect = text_surf.get_rect(center=(200, 40))
heart_surf = pygame.image.load('graphics/heart.png').convert_alpha()
heart_surf = pygame.transform.rotozoom(heart_surf, 0, 0.9)
heart_rect = heart_surf.get_rect(center=(600, 40))


# Load brick graphics
brick_colors = ['dark', 'green', 'orange', 'purple', 'yellow', 'red']
bricks = {}
for color in brick_colors:
    brick_surf = pygame.image.load(f'graphics/brick_{color}.png').convert_alpha()
    brick_surf = pygame.transform.rotozoom(brick_surf, 0, 1.5)
    bricks[color] = brick_surf


# Game variables
paddle_speed = 10
ball_velocity = [0, 0]
ball_speed = 5
ball_moving = False
score = 0
lives = 3
game_over = False

def reset_ball():
    ball_rect.center = (paddle_rect.midtop)
    ball_velocity[0] = 0
    ball_velocity[1] = 0

reset_ball()

def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_rect.x -= paddle_speed
    if keys[pygame.K_RIGHT]:
        paddle_rect.x += paddle_speed
    paddle_rect.clamp_ip(screen.get_rect())

def move_ball():
    global ball_moving, lives
    ball_rect.x += ball_velocity[0]
    ball_rect.y += ball_velocity[1]

    if ball_rect.left <= 0 or ball_rect.right >= 800:
        ball_velocity[0] = -ball_velocity[0]
    if ball_rect.top <= 0:
        ball_velocity[1] = -ball_velocity[1]

    if ball_rect.colliderect(paddle_rect) and ball_velocity[1] > 0:
        ball_velocity[1] = -ball_velocity[1]

    if ball_rect.bottom >= 600:
        ball_moving = False
        lives -=1
        reset_ball()

def check_ball_brick_collision():
    global ball_velocity, score, text_surf
    for brick_row in brick_grid:
        for brick in brick_row:
            brick_type, brick_rect = brick
            if ball_rect.colliderect(brick_rect):
                brick_row.remove(brick)  # Remove brick upon collision

                # Bounce ball on collision
                ball_velocity[1] = -ball_velocity[1]
                score += 1  # Increase score by 1
                # Update the score display, formatted as three digits
                text_surf = font.render(f'{score:03}', False, (99, 155, 255))
                return  # Exit after first collision to prevent multiple hits in one frame


# Create a list of brick rects
brick_width = bricks['red'].get_width()
brick_height = bricks['red'].get_height()
brick_rows = 8
brick_cols = 15
brick_padding = 5
brick_grid = []

for row in range(brick_rows):
    brick_row = []
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_padding)
        brick_y = row * (brick_height + brick_padding) + 70
        brick_type = random.choice(brick_colors)
        brick_rect = bricks[brick_type].get_rect(topleft=(brick_x, brick_y))
        brick_row.append((brick_type, brick_rect))
    brick_grid.append(brick_row)

def draw_lives():
    """Draws the remaining lives (hearts) on the screen."""
    for i in range(lives):
        heart_x = 600 + (i * (heart_surf.get_width() + 10))  # Spacing between hearts
        heart_y = 15
        screen.blit(heart_surf, (heart_x, heart_y))


def display_game_over_message():
    """Displays 'GAME OVER' message."""
    game_over_text = font.render('GAME OVER', True, (99, 155, 255))
    game_over_rect = game_over_text.get_rect(center=(400, 250))  # Centered on the screen
    screen.blit(game_over_text, game_over_rect)

    score_text = font.render(f'SCORE: {score}', True, (99, 155, 255))
    score_rect = score_text.get_rect(center=(400, 350))  # Centered below Game Over
    screen.blit(score_text, score_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_moving:
                ball_velocity = [ball_speed, -ball_speed]
                ball_moving = True

    if lives == 0 and not game_over:
        game_over = True

    if game_over:
        # Clear screen and display the 'Game Over' message
        screen.fill((0, 0, 0))  # Clear screen
        display_game_over_message()  # Display the game over message
        pygame.display.update()
        clock.tick(60)
        continue

    move_paddle()

    if not ball_moving:
        ball_rect.center = paddle_rect.midtop
    else:
        move_ball()
        check_ball_brick_collision()

    screen.blit(background_surf, (0, 0))
    screen.blit(paddle_surf, paddle_rect)
    screen.blit(ball_surf, ball_rect)

    for brick_row in brick_grid:
        for brick_type, brick_rect in brick_row:
            screen.blit(bricks[brick_type], brick_rect)

    screen.blit(text_surf, text_rect)
    draw_lives()

    pygame.display.update()
    clock.tick(60)
