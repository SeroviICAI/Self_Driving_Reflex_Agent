import random

import pygame
import os
import math

pygame.init()

FPS = 60

SCREEN_WIDTH = 593
SCREEN_HEIGHT = 950
BLUE = (0, 0, 255)
RED = (255, 0, 0)
IMAGE_PATH = os.path.join('images')

clock = pygame.time.Clock()
obstacle_speed = 2

# create game window
SCREEN = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

# load image
background = pygame.image.load(IMAGE_PATH + r'\map.png').convert()
background_height = background.get_height()

# game variables
scroll = 0
tiles = math.ceil(SCREEN_HEIGHT / background_height) + 1


class Car(object):
    DEFAULT_WIDTH = 60
    DEFAULT_HEIGHT = 100
    MOVE_LEFT = pygame.USEREVENT + 0
    MOVE_RIGHT = pygame.USEREVENT + 1
    BRAKE = pygame.USEREVENT + 2

    def __init__(self):
        super().__init__()
        self.x = 340
        self.y = 800
        self.rect = [self.x, self.y, 60, 100]
        self.check = None
        self.rradars = False
        self.lradars = False

    def update(self, check_radars: bool = True, x_change: int = 0, y_change: int = 0) -> object:
        car.x += x_change
        car.y += y_change

        self.rradars = False
        for radar_angle in ([90, 60, 45, 0]):
            if self.radar(radar_angle):
                break

        if check_radars:
            self.check_radars()

        self.rect = [self.x, self.y, 60, 100]
        return self

    def check_radars(self):
        if not self.check and self.rradars:
            for radar_angle in [110, 130, 150, 180]:
                if self.radar(radar_angle):
                    break

            if not self.lradars:
                pygame.event.post(pygame.event.Event(self.MOVE_LEFT))
                self.check = True
                return
            self.rradars = False
            pygame.event.post(pygame.event.Event(self.BRAKE))
            return

        if (self.check and not self.rradars) or self.x < 200:
            pygame.event.post(pygame.event.Event(self.MOVE_RIGHT))
            self.check = False
            return
        return

    def radar(self, radar_angle: int):
        length = 0
        x = self.x + 30
        y = self.y + 50

        if radar_angle <= 90:
            max_length = (110 if radar_angle == 0 else 150)
            while not SCREEN.get_at((x, y)) == pygame.Color(255, 0, 0) and length < max_length:
                length += 1
                x = int(self.x + 30 + math.cos(math.radians(radar_angle)) * length)
                y = int(self.y + 50 - math.sin(math.radians(radar_angle)) * length)

            dist = int(math.sqrt(math.pow(self.x + 30 - x, 2)
                                 + math.pow(self.y + 50 - y, 2)))

            if dist != max_length:
                self.rradars = True
            # Draw Radar
            pygame.draw.line(SCREEN, (255, 255, 255), (self.x + 30, self.y + 50), (x, y), 1)
            pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), 3)
            return self.rradars
        else:
            max_length = (350 if radar_angle == 110 else 190)
            while not SCREEN.get_at((x, y)) == pygame.Color(255, 0, 0) and length < max_length:
                length += 1
                x = int(self.x + 30 + math.cos(math.radians(radar_angle)) * length)
                y = int(self.y + 50 - math.sin(math.radians(radar_angle)) * length)

            dist = int(math.sqrt(math.pow(self.x + 30 - x, 2)
                                 + math.pow(self.y + 50 - y, 2)))

            # Draw Radar
            pygame.draw.line(SCREEN, (255, 255, 255), (self.x + 30, self.y + 50), (x, y), 1)
            pygame.draw.circle(SCREEN, (0, 255, 0), (x, y), 3)

            if dist != max_length:
                self.lradars = True
            return self.lradars


# game loop
car = Car()
run = True

# axis x change variable
x_change = 0
y_change = 0
active = False
active_car = False
obstacle_position_right = random.randint(0, 500)
obstacle_position_left = random.randint(0, 500)
temp_time = 0

while run:
    if not active:
        obstacle_position_right = random.randint(0, 500)
        obstacle_position_left = random.randint(0, 500)
        active = True

    if not active_car:
        car = Car()
        active_car = True

    clock.tick(FPS)
    # draw scrolling background
    for i in range(0, tiles):
        SCREEN.blit(background, (0, (i - 1) * background_height + scroll))

    # scroll background
    scroll += 5

    # reset scroll
    if scroll > background_height:
        scroll = 0

    # update obstacle position
    obstacle_position_right += obstacle_speed
    obstacle_position_left += obstacle_speed

    car_rect = pygame.draw.rect(SCREEN, BLUE, car.rect)
    obstacle_right = pygame.draw.rect(SCREEN, RED, [340, obstacle_position_right, 60, 100])
    obstacle_left = pygame.draw.rect(SCREEN, RED, [200, obstacle_position_left, 60, 100])

    car = car.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == Car.MOVE_LEFT:
            x_change = -2

        if event.type == Car.MOVE_RIGHT:
            x_change = 2

        if event.type == Car.BRAKE:
            y_change = obstacle_speed

    if active:
        if car_rect.colliderect(obstacle_right) or car_rect.colliderect(obstacle_left):
            run = False
        if obstacle_position_right >= SCREEN_HEIGHT and obstacle_position_left >= SCREEN_HEIGHT:
            active = False
        if car.y > (SCREEN_HEIGHT - 100):
            active = False
            active_car = False

    if car.x == 340 and not car.check:
        x_change = 0

    if 137 <= car.x <= 400:
        car = car.update(False, x_change=x_change, y_change=y_change)
        y_change = 0
    elif car.x < 137:
        car = car.update(False, x_change=0)
    elif car.x > 400:
        car = car.update(False, x_change=0)

    pygame.display.update()

pygame.quit()
