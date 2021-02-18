import pygame
import os
import sys

pygame.font.init()
pygame.mixer.init()  # sound effects library

# Global Vars
WIDTH, HEIGHT = 1200, 600  # game resolution
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # main surface
pygame.display.set_caption("SpaceWars")  # window title

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 3, 0, 6, HEIGHT)  # middle border line

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 50
VELOCITY = 6
BULLET_VELOCITY = 11
MAX_BULLETS = 3  # max bullets at a time

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(sys.path[0], "Assets", "Collide.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join(sys.path[0], "Assets", "Shoot.mp3"))

RED_HIT = pygame.USEREVENT + 1  # custom event
YELLOW_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join(sys.path[0], "Assets", "spaceship_yellow.png"))  # import yellow spaceship
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))  # scale down and rotated
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 270)  # rotated to fix angle

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join(sys.path[0], "Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 90)

SPACE_IMAGE = pygame.image.load(
    os.path.join(sys.path[0], "Assets", "space.png"))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))


def main():  
    red = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()  # to cap fps
    run = True
    while run:
        clock.tick(FPS)  # fps cap

        for event in pygame.event.get():  # event checks
            if event.type == pygame.QUIT:  # cross button was clicked
                run = False

            if event.type == pygame.KEYDOWN:  # bullet was fired
                # red fired
                red_bullets_check = len(red_bullets) < MAX_BULLETS # condition
                if event.key == pygame.K_LALT and red_bullets_check:
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # yellow fired
                yellow_bullets_check = len(yellow_bullets) < MAX_BULLETS
                if event.key == pygame.K_RALT and yellow_bullets_check:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # bullet hit
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        draw_board(red, yellow, red_bullets, yellow_bullets,
                   red_health, yellow_health)

        # check winner
        winner_text = ""
        if red_health == 0:
            winner_text = "Yellow Wins!"
        if yellow_health == 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            main()  # restarts the game everytime someone wins

        keys_pressed = pygame.key.get_pressed()
        handle_red_movement(keys_pressed, red)
        handle_yellow_movement(keys_pressed, yellow)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)
    pygame.quit()


def draw_board(
        red: pygame.Rect, yellow: pygame.Rect, red_bullets: list, yellow_bullets: list, red_health: int, yellow_health: int):
    """Draws and updates the main surface.

    Args:
        red (pygame.Rect): Red spaceship rectangle object.
        yellow (pygame.Rect): Yellow spaceship rectangle object.
        red_bullets (list): Red bullets list that contains bullet rectangle objects.
        yellow_bullets (list): Yellow bullets list that contains bullet rectangle objects.
        red_health (int): Amount of health red spaceship has.
        yellow_health (int): Amount of health red spaceship has.
    """    
    WIN.blit(SPACE, (0, 0))  # background
    pygame.draw.rect(WIN, BLACK, BORDER)  # middle border

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text,
             (WIDTH - yellow_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(winner_text: str):
    """Draws winner text on screen and creates a delay for X seconds.

    Args:
        winner_text (str): Text that contains the spaceship (red/yellow) that has won.
    """      
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    x_position = WIDTH // 2 - draw_text.get_width() // 2
    y_position = HEIGHT // 2 - draw_text.get_height() // 2
    WIN.blit(draw_text, (x_position, y_position))
    pygame.display.update()
    pygame.time.delay(4000)


def handle_red_movement(keys_pressed: pygame.key, red: pygame.Rect):
    """Handles the movement of red spaceship when the respective keys (W, A, S or D) are pressed.

    Args:
        keys_pressed (pygame.key): Keys object that contains information of the keys being pressed.
        red (pygame.Rect): Rectangle object of red spaceship.
    """       
    # left
    if keys_pressed[pygame.K_a] and (red.x - VELOCITY >= 0):
        red.x -= VELOCITY

    # right
    if keys_pressed[pygame.K_d] and ((red.x + SPACESHIP_WIDTH) + VELOCITY < BORDER.x):
        red.x += VELOCITY

    # up
    if keys_pressed[pygame.K_w] and (red.y - VELOCITY >= 0):
        red.y -= VELOCITY

    # down
    if keys_pressed[pygame.K_s] and ((red.y + SPACESHIP_HEIGHT) + VELOCITY < HEIGHT):
        red.y += VELOCITY


def handle_yellow_movement(keys_pressed: pygame.key, yellow: pygame.Rect):
    """Handles the movement of yellow spaceship when the respective keys (left, right, up or down arrow) are pressed.

    Args:
        keys_pressed (pygame.key): Keys object that contains information of the keys being pressed.
        yellow (pygame.Rect): Rectangle object of yellow spaceship.
    """    
    # left
    if keys_pressed[pygame.K_LEFT] and ((yellow.x) - VELOCITY > (BORDER.x + BORDER.width)):
        yellow.x -= VELOCITY

    # right
    if keys_pressed[pygame.K_RIGHT] and (((yellow.x + SPACESHIP_WIDTH) + VELOCITY) <= WIDTH):
        yellow.x += VELOCITY

    # up
    if keys_pressed[pygame.K_UP] and (yellow.y - VELOCITY >= 0):
        yellow.y -= VELOCITY

    # down
    if keys_pressed[pygame.K_DOWN] and ((yellow.y + SPACESHIP_HEIGHT) + VELOCITY < HEIGHT):
        yellow.y += VELOCITY


def handle_bullets(red_bullets: list, yellow_bullets: list, red: pygame.Rect, yellow: pygame.Rect):
    """Handles bullets by moving them across the screen in right or left direction for respective spaceships. If a bullet is hit, a custom hit event is posted in pygame.event queue.

    Args:
        red_bullets (list): Red bullets list that contains bullet rectangle objects.
        yellow_bullets (list): Yellow bullets list that contains bullet rectangle objects.
        red (pygame.Rect): Red spaceship rectangle object.
        yellow (pygame.Rect): Yellow spaceship rectangle object.
    """      
    for bullet in red_bullets:
        bullet.x += BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))  # posts custom hit event
            red_bullets.remove(bullet)
        elif bullet.x >= WIDTH:  # bullet goes out of screen
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x <= 0:
            yellow_bullets.remove(bullet)


if __name__ == "__main__":
    main()
