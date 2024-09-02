# Example file showing a basic pygame "game loop"
import pygame
import random
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
score = 0

# Colors
GREEN = pygame.Color(106, 156, 137, 1)
RED = pygame.Color(130, 17, 49, 1)
btn_color = pygame.Color(34, 123, 148, 1)
snake_color = pygame.Color(22, 66, 60, 1)
coconut_cream = pygame.Color(247, 238, 211, 1)
target_color = pygame.Color(160, 71, 71, 1)

# cube class
class Cube:
    def __init__(self):
        self.generate_position()
        
    def generate_position(self):
        self.x = random.randint(50, screen.get_width()-50)
        self.y = random.randint(50, screen.get_height()-50)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
    
    def draw(self):
        pygame.draw.rect(screen, target_color, self.rect)

# snake class
class Snake:
    def __init__(self):
        self.rect = pygame.Rect(screen.get_width() / 2, screen.get_height() / 2, 50, 50)
        self.directions = (0, 0)
        self.length = 1
        self.pixels = [self.rect.copy()]

    def add_pixel(self):
        tail = self.pixels[-1].copy()
        self.pixels.append(tail)

    def move(self):
        if self.directions != (0, 0):
            new_head = self.pixels[0].copy()
            new_head.move_ip(self.directions)
            self.pixels = [new_head] + self.pixels[:-1]

    def draw(self):
        for pixel in self.pixels:
            pygame.draw.rect(screen, snake_color, pixel)

    def reset(self):
        self.length = 1
        self.directions = (0, 0)
        self.rect = pygame.Rect(screen.get_width() / 2, screen.get_height() / 2, 50, 50)
        self.pixels = [self.rect.copy()]

# initialize cube and snake object
cube = Cube()
snake = Snake()

# method draw button
def draw_button(screen, color, rect, text):
    pygame.draw.rect(screen, color, rect, border_radius=20)
    font = pygame.font.SysFont('times new roman', 30)
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# method reset game
def reset_game():
    global score
    score = 0
    cube.generate_position()
    snake.reset()

# method to show score on the screen
def show_score():
    score_font = pygame.font.SysFont('times new roman', 20)
    score_surface = score_font.render('Score: ' + str(score), True, GREEN)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)

# method to show game over and reset button
def game_over():
    game_over_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = game_over_font.render('GAME OVER', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.center = (screen.get_width()/2, screen.get_height()/2)
    screen.blit(game_over_surface, game_over_rect)

    # reset button
    reset_button = pygame.Rect(screen.get_width()/2 - 100, screen.get_height()/2 + 40, 200, 40)
    draw_button(screen, btn_color, reset_button, "Reset")

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                time.sleep(2)
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    reset_game()
                    return
                
# method to manage out of bounds
def out_of_bounds(snake):
    width = screen.get_width()
    height = screen.get_height()

    if snake.pixels[0].left < 0:
        snake.pixels[0].x = width
    elif snake.pixels[0].right > width:
        snake.pixels[0].x = 0
    elif snake.pixels[0].top < 0:
        snake.pixels[0].y = height
    elif snake.pixels[0].bottom > height:
        snake.pixels[0].y = 0



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(coconut_cream)

    # game logic
    if snake.pixels[0].colliderect(cube.rect):
        cube.generate_position()
        snake.add_pixel()
        snake.length += 1
        score += 1

    # game over logic
    if len(snake.pixels) > 0:
        for pixel in snake.pixels[2:]:
            if snake.pixels[0].colliderect(pixel):
                game_over()
                break
        


    # generate cube in a random position
    cube.draw()

    # move the snake
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.KEYUP]:
        snake.directions = (0, -snake.rect.width)
    if keys[pygame.K_s] or keys[pygame.KEYDOWN]:
        snake.directions = (0, snake.rect.width)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        snake.directions = (-snake.rect.width, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        snake.directions = (snake.rect.width, 0)


    # update snake position
    snake.move()

    # generate snake
    snake.draw()

    # show score
    show_score()

    # check out of bounds
    out_of_bounds(snake)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(5)  / 1000 # limits FPS to 60

pygame.quit()