# -1 margin
# 0 empty cell
# 1 gnome
# 2 gold
# 3 gem
# 4 exit
# 5 wall
# 5 explored empty cell
# 52 explored gold cell
# 53 explored gem cell
# 54 explored exit cell
# 55 explored wall cell

import random
import constants
import core
# import pygame


def make_gnome_vision(state, gnome):
    x_vis = gnome.x + gnome.vision_size
    y_vis = gnome.y + gnome.vision_size

    vision = []

    # 2 * vision_size + 1 -> Because vision_size is a distance form your front to the furthers cell
    for row in range(2 * gnome.vision_size + 1):
        vision_row = []

        for col in range(2 * gnome.vision_size + 1):
            cell = state[y_vis + row - gnome.vision_size][x_vis + col - gnome.vision_size]
            vision_row.append(cell)

        vision.append(vision_row)

    return vision


# Coordinates of the scanned map are counted including margins
def scan_map(scanned_map, gnome, gnome_vision):
    # Loop through gnome vision and find those cells in the state and check if they are discovered
    # Each cell is represented as dict of { x, y, v } coordinates and value
    for row in range(len(gnome_vision)):
        for col in range(len(gnome_vision[row])):
            cell = {
                "x": col - gnome.vision_size + gnome.x,
                "y": row - gnome.vision_size + gnome.y,
                "v": gnome_vision[row][col]
            }
            if cell not in scanned_map:
                scanned_map.append(cell)

    return scanned_map


def make_state(gnome, gold):
    empty_state = make_empty_state()
    gnome_state = add_gnome(empty_state, gnome)
    exit_state = add_exit(gnome_state)
    gem_state = add_gem(exit_state)
    gold_state = add_gold(gem_state, gold)
    margin_state = add_margin(gold_state)
    return margin_state


def make_empty_state():
    empty_state = []
    for row in range(constants.CELL_AMOUNT_Y):
        empty_row = []
        for col in range(constants.CELL_AMOUNT_X):
            empty_row.append(constants.EMPTY_CODE)

        empty_state.append(empty_row)

    return empty_state


def add_margin(state):
    margin_state = []
    margin_row = []

    # Build up a placeholder for the horizontal margin walls
    for i in range(len(state[0]) + constants.GNOME_VISION_SIZE * 2):
        # -1 represents walls ie non accessible cells
        margin_row.append(constants.MARGIN_CODE)

    # Add top margin
    for i in range(constants.GNOME_VISION_SIZE):
        margin_state.append(margin_row)

    for row in state:
        mid_line = []
        # Adding first vision_size amount of -2s to the beginning of the row
        for i in range(constants.GNOME_VISION_SIZE):
            mid_line.append(constants.MARGIN_CODE)

        # Adding the actual row to the mid_line
        mid_line.extend(row)

        # Adding last vision_size amount of -2s to the end of the row
        for i in range(constants.GNOME_VISION_SIZE):
            mid_line.append(constants.MARGIN_CODE)

        # Adding built up row to the actual state
        margin_state.append(mid_line)

    # Add bottom margin
    for i in range(constants.GNOME_VISION_SIZE):
        margin_state.append(margin_row)

    return margin_state


def add_gnome(state, gnome):
    state[gnome.y][gnome.x] = constants.GNOME_CODE
    return state


def add_exit(state):
    state[constants.EXIT_Y][constants.EXIT_X] = constants.EXIT_CODE
    return state


def add_gem(state):
    state[constants.GEM_Y][constants.GEM_X] = constants.GEM_CODE
    return state


def add_gold(state, gold):
    return state
