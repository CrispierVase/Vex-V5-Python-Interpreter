#!/usr/bin/python3

import pygame
import time
import math
import asyncio

# this is just for user input. It can be removed if desired, and constants can be set. This is recomended.
import sys

SECONDS = '\x53'
FORWARD = '\x46'
BACKWARD = '\x42'
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

args = sys.argv[1:]
print(args)

grid_size = [5, 5]
desired_size = [16 * 8 * grid_size[0], 16 * 8 * grid_size[1]]

try:
    program = args[0]
    starting_x = int(args[1])
    starting_y = int(args[2])
    starting_direction = int(args[3])
    if '.v5python' not in program:
        raise Exception(
            'You must provide a ".v5python" file as the first argument. ')
    try:
        with open(program, 'r') as program_file:
            program_contents = program_file.read()
    except Exception:
        raise Exception(
            'The program you provided does not exist in the local directory. You must navigate there. This process is described in the documentation. ')
except Exception:
    raise Exception('You must provide a program to run, the starting x position, the starting y position of the robot, and starting direction. This is described in the documentation. ')
if len(args) == 6:
    grid_size[0] = int(args[4])
    grid_size[1] = int(args[5])

tile_size = ((desired_size[0] / grid_size[0]) - grid_size[0],
             (desired_size[1] / grid_size[1]) - grid_size[1])
size = [(tile_size[0] * grid_size[0]) - grid_size[0],
        (tile_size[1] * grid_size[1]) - grid_size[1]]

if size[0] < tile_size[0]:
    size[0] = tile_size[0]
if size[1] < tile_size[1]:
    size[1] = tile_size[1]

win = pygame.display.set_mode(size)


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
    def __init__(self):
        self.x = 0  # this is 0 tiles moved left or right
        self.y = 0  # this is 0 tiles moved up or down
        self.direction = 3  # since this will only need to be 90 degree values,
        # it will not be a full 36 as this is not very useful with the grid system of this program.
        # left = 0, up = 1, right = 2, down = 3
        self.image = pygame.image.load('robot-icon.png')

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
            elif direction == BACKWARD:
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

    def drive_for(self, direction, distance, unit):
        for _ in range(distance):
            if not self.in_valid_position():
                raise Exception('The Robot Has Exited the Grid. ')
            if direction == BACKWARD:
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
            time.sleep(1)

    def turn_for(self, direction, angle, DEGREES=DEGREES):
        if direction == RIGHT:
            for _ in range(int(angle / 90)):
                self.direction += 1
        elif direction == LEFT:
            for _ in range(int(angle / 90)):
                self.direction -= 1
        self.direction %= 4

    def draw(self, win=win):
        middle = (self.x * tile_size[0]) - 3, (self.y * tile_size[1])
        win.blit(pygame.transform.scale(pygame.transform.rotate(self.image, ((
            self.direction - 1) % 4) * 90), (tile_size[0], tile_size[1])), middle)


class Tile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        if self.color == GREEN:
            self.image = pygame.image.load('tile-green.png')
        elif self.color == RED:
            self.image = pygame.image.load('tile-red.png')
        elif self.color == YELLOW:
            self.image = pygame.image.load('tile-yellow.png')
        else:
            print('Please provide a correct color for tiles. ')
            quit()
        self.image = pygame.transform.scale(
            self.image, (tile_size[0] - 6, tile_size[1] - 6))

    def draw(self, win=win):
        win.blit(
            self.image, ((self.x * tile_size[0]), (self.y * tile_size[1])))
        return


tiles = [[Tile(x, y, GREEN)for x in range(grid_size[0])]
         for y in range(grid_size[1])]

running = True
code_run = False



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    win.fill((0, 0, 0))

    # draw stuff here
    for row in tiles:
        for tile in row:
            tile.draw()
    drivetrain.draw()
    
    pygame.display.flip()
    if not code_run:
        self.que.put(getattr(exec(code), drivetrain))


pygame.quit()


runner = Runner()
vals = asyncio.gather(runner.draw(),
    runner.run_user_code())


