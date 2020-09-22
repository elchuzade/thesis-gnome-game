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
import pygame


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
def scan_map(scanned_map, gnome, gnome_vision, state):
    # Loop through gnome vision and find those cells in the state and check if they are discovered
    # Each cell is represented as dict of { x, y, v } coordinates and value
    for row in range(len(gnome_vision)):
        for col in range(len(gnome_vision[row])):
            cell = {
                "x": col - gnome.vision_size + gnome.x,
                "y": row - gnome.vision_size + gnome.y,
                "v": state[row - gnome.vision_size + gnome.y][col - gnome.vision_size + gnome.x]
            }
            exists = False
            for item in scanned_map:
                if item["x"] == cell["x"] and item["y"] == cell["y"]:
                    exists = True

            if not exists:
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


# TEXT

def find_exit_distance(gnome):
    return abs(constants.EXIT_Y - gnome.y) + abs(constants.EXIT_X - gnome.x)


def check_coin_collect(gnome, gold):
    for coin in gold:
        if coin.x == gnome.x and coin.y == gnome.y:
            return True
    return False


def update_gold_text_placeholder(font):
    text = font.render("GOLD: ", True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 - constants.TEXT_WIDTH * 2,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


def update_exit_text_placeholder(font):
    text = font.render("EXIT: ", True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 + constants.TEXT_WIDTH,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


def update_gold_text(font, collected_gold):
    text = font.render(str(collected_gold), True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 - constants.TEXT_WIDTH,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


def update_exit_text(font, exit_distance):
    text = font.render(str(exit_distance), True, constants.TEXT_COLOR, constants.SCOREBOARD_BACKGROUND)
    text_rect = text.get_rect()
    text_rect.center = (((constants.MARGIN * 2) + constants.GAME_PLAY_WIDTH) // 2 + constants.TEXT_WIDTH * 2,
                        ((constants.SCOREBOARD_HEIGHT // 2) + constants.MARGIN * 2 + constants.GAME_PLAY_HEIGHT))

    return text, text_rect


# DRAWING

def draw_scoreboard(screen):
    pygame.draw.rect(screen, constants.SCOREBOARD_BACKGROUND, (0, constants.GAME_PLAY_HEIGHT + constants.MARGIN * 2,
                                                               constants.GAME_PLAY_WIDTH + constants.MARGIN * 2,
                                                               constants.SCOREBOARD_HEIGHT))


def draw_margins(screen):
    # Left line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN,
                                                           constants.MARGIN, constants.GAME_PLAY_HEIGHT))
    # Right line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND,
                     (constants.MARGIN + constants.GAME_PLAY_WIDTH, constants.MARGIN,
                      constants.MARGIN, constants.GAME_PLAY_HEIGHT))
    # Top line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, 0,
                                                           constants.MARGIN * 2 + constants.GAME_PLAY_WIDTH,
                                                           constants.MARGIN))
    # Bottom line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN + constants.GAME_PLAY_HEIGHT,
                                                           constants.MARGIN * 2 + constants.GAME_PLAY_WIDTH,
                                                           constants.MARGIN))


def draw_grid(screen):
    # Draws a grid to separate each game cell
    for i in range(constants.CELL_AMOUNT_X - 1):
        pygame.draw.rect(screen, constants.GRID_LINE_COLOR, (constants.MARGIN + i * constants.CELL_SIZE +
                                                             constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2,
                                                             constants.MARGIN,
                                                             constants.GRID_LINE_WIDTH,
                                                             constants.CELL_SIZE * constants.CELL_AMOUNT_Y))

    for i in range(constants.CELL_AMOUNT_Y - 1):
        pygame.draw.rect(screen, constants.GRID_LINE_COLOR, (constants.MARGIN,
                                                             constants.MARGIN + i * constants.CELL_SIZE +
                                                             constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2,
                                                             constants.CELL_SIZE * constants.CELL_AMOUNT_X,
                                                             constants.GRID_LINE_WIDTH))


def draw_gnome(screen, gnome):
    pygame.draw.circle(screen, constants.GNOME_COLOR,
                       [int(gnome.x * constants.CELL_SIZE + constants.CELL_SIZE / 2) + constants.MARGIN,
                        int(gnome.y * constants.CELL_SIZE + constants.CELL_SIZE / 2) + constants.MARGIN],
                       int(constants.GNOME_RADIUS))


def draw_gold(screen, gnome, vision_size, row, col):
    pygame.draw.circle(screen, constants.GOLD_COLOR,
                       [int((gnome.x + col - vision_size) * constants.CELL_SIZE + constants.CELL_SIZE / 2) +
                        constants.MARGIN,
                        int((gnome.y + row - vision_size) * constants.CELL_SIZE + constants.CELL_SIZE / 2) +
                        constants.MARGIN],
                       int(constants.GOLD_RADIUS))


def draw_vision_cell(screen, gnome, vision_size, row, col):
    pygame.draw.rect(screen, constants.GNOME_VISION_COLOR,
                     ((col + gnome.x - vision_size) * constants.CELL_SIZE + constants.MARGIN,
                      (row + gnome.y - vision_size) * constants.CELL_SIZE + constants.MARGIN,
                      constants.CELL_SIZE, constants.CELL_SIZE))


def draw_vision(screen, gnome, vision):
    for row in range(len(vision)):
        for col in range(len(vision[row])):
            draw_vision_cell(screen, gnome, len(vision[0]) // 2, row, col)
            if vision[row][col] == 2:
                draw_gold(screen, gnome, len(vision[0]) // 2, row, col)


def draw_exit(screen):
    pygame.draw.rect(screen, constants.EXIT_COLOR, (constants.EXIT_X * constants.CELL_SIZE + constants.MARGIN,
                                                    constants.EXIT_Y * constants.CELL_SIZE + constants.MARGIN,
                                                    constants.CELL_SIZE, constants.CELL_SIZE))


def draw_scanned_map(screen, scanned_map):
    for i in scanned_map:
        pygame.draw.rect(screen, constants.SCANNED_MAP_COLOR, (i["x"] * constants.CELL_SIZE + constants.MARGIN,
                                                               i["y"] * constants.CELL_SIZE + constants.MARGIN,
                                                               constants.CELL_SIZE, constants.CELL_SIZE))


def draw_game(screen, scaned_map, gnome, vision):
    draw_scanned_map(screen, scaned_map)
    draw_vision(screen, gnome, vision)
    draw_margins(screen)
    draw_scoreboard(screen)
    draw_grid(screen)
    draw_exit(screen)
    draw_gnome(screen, gnome)