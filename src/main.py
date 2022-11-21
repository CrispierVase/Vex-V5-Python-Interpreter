#!/usr/bin/python3

import pygame
import time

SECONDS = '\x53'
FORWARD = '\x46'
REVERSE = '\x42'
MM = '\x4D\x4D'
INCHES = '\x49\x4E'
DEGREES = '\x44'
RIGHT = '\x52'
LEFT = '\x4C'
GREEN = '\x67'
RED = '\x72'
YELLOW = '\x79'


# set up graphics
pygame.init()
grid_size = [5, 5]
desired_size = [16 * 8 * grid_size[0], 16 * 8 * grid_size[1]]
tile_size = ((desired_size[0] / grid_size[0]) - grid_size[0],
            (desired_size[1] / grid_size[1]) - grid_size[1])
size = [(tile_size[0] * grid_size[0]) - grid_size[0],
        (tile_size[1] * grid_size[1]) - grid_size[1]]
if size[0] < tile_size[0]:
    size[0] = tile_size[0]
if size[1] < tile_size[1]:
    size[1] = tile_size[1]


win = pygame.display.set_mode(size)


class Tile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        if self.color == GREEN:
            self.image = pygame.image.load('graphics/tile-green.png')
        elif self.color == RED:
            self.image = pygame.image.load('graphics/tile-red.png')
        elif self.color == YELLOW:
            self.image = pygame.image.load('graphics/tile-yellow.png')
        self.image = pygame.transform.scale(
            self.image, (tile_size[0] - 6, tile_size[1] - 6))

    def draw(self, win=win):
        win.blit(
            self.image, ((self.x * tile_size[0]), (self.y * tile_size[1])))
        return


tiles = [[Tile(x, y, GREEN)for x in range(grid_size[0])]
         for y in range(grid_size[1])]

def draw_tiles(tiles=tiles):
    for row in tiles:
        for tile in row:
            tile.draw()


def draw():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit()
    pygame.quit()


def wait(seconds, SECONDS=SECONDS):
    time.sleep(seconds)


class Screen:
    def __init__(self):
        return

    def print(self, value):
        print(value, end='')

    def next_row(self):
        print('\n')

    def clear_screen(self):
        print('PROGRAM MESSAGE: SCREEN CLEARED')

    def set_cursor(self, row, col):
        # this feature is not supported in this interpreter.
        return

    def clear_row(self, row):
        print(f'PROGRAM MESSAGE: ROW {row} CLEARED')


class Brain:
    def __init__(self):
        self.screen = Screen()


class Drivetrain:
    def __init__(self, x=0, y=0, direction=3):
        self.x = x  # this is 0 tiles moved left or right
        self.y = y  # this is 0 tiles moved up or down
        self.direction = direction  # since this will only need to be 90 degree values,
        # it will not be a full 36 as this is not very useful with the grid system of this program.
        # left = 0, up = 1, right = 2, down = 3
        self.image = pygame.image.load('graphics/robot-icon.png')
        self.wait_duration = 1

    def in_valid_position(self):
        return 0 <= self.x <= grid_size[0] - 1 and 0 <= self.y <= grid_size[1] - 1

    def drive(self, direction=FORWARD):
        # this function will only move in tiles. Distance is not used.
        while True:
            if not self.in_valid_position():
                raise Exception('The Robot Has Exited the Grid. ')
            if direction == FORWARD:
                if self.direction == 0:
                    self.x -= 1
                    self.y += 0
                if self.direction == 1:
                    self.x += 0
                    self.y += 1
                elif self.direction == 2:
                    self.x += 1
                    self.y += 0
                elif self.direction == 3:
                    self.x += 0
                    self.y -= 1
            elif direction == REVERSE:
                if self.direction == 0:
                    self.x += 1
                    self.y += 0
                if self.direction == 1:
                    self.x += 0
                    self.y -= 1
                elif self.direction == 2:
                    self.x -= 1
                    self.y += 0
                elif self.direction == 3:
                    self.x += 0
                    self.y += 1
            self.draw()
            time.sleep(self.wait_duration)

    def drive_for(self, direction, distance, unit):
        for _ in range(distance):
            if not self.in_valid_position():
                raise Exception('The Robot Has Exited the Grid. ')
            if direction == REVERSE:
                if self.direction == 0:
                    self.x -= 1
                    self.y += 0
                if self.direction == 1:
                    self.x += 0
                    self.y += 1
                elif self.direction == 2:
                    self.x += 1
                    self.y += 0
                elif self.direction == 3:
                    self.x += 0
                    self.y -= 1
            elif direction == FORWARD:
                if self.direction == 0:
                    self.x += 1
                    self.y += 0
                if self.direction == 1:
                    self.x += 0
                    self.y -= 1
                elif self.direction == 2:
                    self.x -= 1
                    self.y += 0
                elif self.direction == 3:
                    self.x += 0
                    self.y += 1
            self.draw()
            time.sleep(self.wait_duration)


    def turn_for(self, direction, angle, DEGREES):
        if direction == RIGHT:
            for _ in range(int(angle / 90)):
                self.direction -= 1
        elif direction == LEFT:
            for _ in range(int(angle / 90)):
                self.direction += 1
        self.direction %= 4
        self.draw()
        time.sleep(self.wait_duration)
    
    def turn(self, direction):
        while True:
            self.turn_for(90, direction)

    def draw(self, win=win):
        middle = (self.x * tile_size[0]) - 3, (self.y * tile_size[1])
        win.fill((0, 0, 0))
        draw_tiles()
        win.blit(pygame.transform.scale(pygame.transform.rotate(self.image, ((
            self.direction - 1) % 4) * 90), (tile_size[0], tile_size[1])), middle)
        pygame.display.flip()


drivetrain = Drivetrain()
brain = Brain()
