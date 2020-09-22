import constants
import helpers
# import pygame
import random
# import numpy as np


class Gnome:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vision_size = constants.GNOME_VISION_SIZE

    def move(self, direction):
        # Move the gnome in the given direction
        if direction == 0:
            self.x -= 1
        elif direction == 1:
            self.y -= 1
        elif direction == 2:
            self.x += 1
        elif direction == 3:
            self.y += 1


class Game:
    def __init__(self, mode=constants.GAME_MODE, speed=constants.GAME_SPEED, gold_amount=constants.GOLD_AMOUNT):
        self.__mode = mode
        self.__speed = speed
        self.__gold_amount = gold_amount
        self.__gnome = Gnome(constants.GNOME_X, constants.GNOME_Y)
        self.__gold = []
        self.__state = helpers.make_state(self.__gnome, self.__gold)
        self.__scanned_map = []
        self.__gnome_vision = helpers.make_gnome_vision(self.__state, self.__gnome)

    def get_state(self, __print=False):
        if __print:
            for row in self.__state:
                print(row)
        else:
            return self.__state

    def scan_map(self):
        self.__scanned_map = helpers.scan_map(self.__scanned_map, self.__gnome, self.__gnome_vision, self.__state)

    def get_scanned_map(self):
        return self.__scanned_map

    def get_gnome_vision(self, __print=False):
        if __print:
            for row in self.__gnome_vision:
                print(row)
        else:
            return self.__gnome_vision

    def step(self, direction):
        # 0 - left, 1 - up, 2 - right, 3 - down
        if direction == 0:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.__gnome_vision[self.__gnome.vision_size][self.__gnome.vision_size - 1] != -1:
                self.__gnome.move(0)

        elif direction == 1:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.__gnome_vision[self.__gnome.vision_size - 1][self.__gnome.vision_size] != -1:
                self.__gnome.move(1)

        elif direction == 2:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.__gnome_vision[self.__gnome.vision_size][self.__gnome.vision_size + 1] != -1:
                self.__gnome.move(2)

        elif direction == 3:
            # Check if there is a wall on the left by finding the center of the gnome's vision
            if self.__gnome_vision[self.__gnome.vision_size + 1][self.__gnome.vision_size] != -1:
                self.__gnome.move(3)

        # Update state after moving gnome
        self.__state = helpers.make_state(self.__gnome, self.__gold)
        self.__gnome_vision = helpers.make_gnome_vision(self.__state, self.__gnome)
        self.__scanned_map = helpers.scan_map(self.__scanned_map, self.__gnome, self.__gnome_vision, self.__state)
        return self.__gnome_vision
