import constants
import helpers
import pygame
import random
# import numpy as np

class Gold:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
    def __init__(self, mode=constants.GAME_MODE):
        self.__mode = mode
        self.__step_counter = 0
        self.__collected_gem = 0
        self.__collected_gold = 0
        self.__action_frequency = constants.FPS / constants.GAME_SPEED
        self.__gold = helpers.initialize_all_gold()
        self.__gnome = Gnome(constants.GNOME_X, constants.GNOME_Y)
        self.__state = helpers.make_state(self.__gnome, self.__gold)
        self.__gnome_vision = helpers.make_gnome_vision(self.__state, self.__gnome)
        self.__scanned_map = helpers.scan_map([], self.__gnome, self.__gnome_vision, self.__state)
        self.__covered_map = helpers.make_covered_map(self.__state, self.__scanned_map)

    def reset(self):
        self.__step_counter = 0
        self.__collected_gem = 0
        self.__collected_gold = 0
        self.__gold = helpers.initialize_all_gold()
        self.__gnome = Gnome(constants.GNOME_X, constants.GNOME_Y)
        self.__state = helpers.make_state(self.__gnome, self.__gold)
        self.__gnome_vision = helpers.make_gnome_vision(self.__state, self.__gnome)
        self.__scanned_map = helpers.scan_map([], self.__gnome, self.__gnome_vision, self.__state)
        self.__covered_map = helpers.make_covered_map(self.__state, self.__scanned_map)

    def get_exit(self):
        return helpers.find_exit_distance(self.__gnome)

    def get_gold(self):
        return self.__collected_gold

    def get_gem(self):
        return self.__collected_gem

    def get_steps(self):
        return self.__step_counter

    def get_state(self, __print=False):
        if __print:
            for row in self.__state:
                print(row)
        else:
            return self.__state

    def get_scanned_map(self):
        return self.__scanned_map

    def get_covered_map(self):
        return self.__covered_map

    def get_gnome_vision(self, __print=False):
        if __print:
            for row in self.__gnome_vision:
                print(row)
        else:
            return self.__gnome_vision

    def __remove_gold(self):
        for index, coin in enumerate(self.__gold):
            if coin.x == self.__gnome.x and coin.y == self.__gnome.y:
                del self.__gold[index]
                self.__collected_gold += 1
                for i in self.__scanned_map:
                    if i["x"] == self.__gnome.x and i["y"] == self.__gnome.y and i["v"] == constants.GOLD_CODE:
                        i["v"] = 0

    def __remove_gem(self):
        self.__collected_gem += 1
        for i in self.__scanned_map:
            if i["x"] == self.__gnome.x and i["y"] == self.__gnome.y and i["v"] == constants.GEM_CODE:
                i["v"] = 0

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

        # Check if gnome has stepped on a gold
        if helpers.check_coin_collect(self.__gnome, self.__gold):
            self.__remove_gold()

        if helpers.check_gem_collect(self.__gnome):
            self.__remove_gem()

        if helpers.check_exit_reached(self.__gnome):
            self.reset()

        # Update state after moving gnome
        self.__state = helpers.make_state(self.__gnome, self.__gold)
        self.__gnome_vision = helpers.make_gnome_vision(self.__state, self.__gnome)
        self.__scanned_map = helpers.scan_map(self.__scanned_map, self.__gnome, self.__gnome_vision, self.__state)
        self.__covered_map = helpers.make_covered_map(self.__state, self.__scanned_map)
        return self.__gnome_vision

    def __initialize_game(self):
        pygame.init()
        pygame.display.set_caption("Gnome game by {}".format(self.__mode))
        size = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT
        screen = pygame.display.set_mode(size)
        font = pygame.font.Font(constants.FONT_NAME, constants.FONT_SIZE)

        # Clock is set to keep track of frames
        clock = pygame.time.Clock()
        pygame.display.flip()
        frame = 1
        action_taken = False
        while True:
            clock.tick(constants.FPS)
            pygame.event.pump()
            for event in pygame.event.get():
                if self.__mode == "player" and not action_taken:
                    # Look for any button press action
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            action_taken = True
                            action = 0  # 0 means go left
                            self.step(action)
                            self.__step_counter += 1

                        elif event.key == pygame.K_UP:
                            action_taken = True
                            action = 1  # 1 means go up
                            self.step(action)
                            self.__step_counter += 1

                        elif event.key == pygame.K_RIGHT:
                            action_taken = True
                            action = 2  # 2 means go right
                            self.step(action)
                            self.__step_counter += 1

                        elif event.key == pygame.K_DOWN:
                            action_taken = True
                            action = 3  # 3 means go down
                            self.step(action)
                            self.__step_counter += 1

                # Quit the game if the X symbol is clicked
                if event.type == pygame.QUIT:
                    print("pressing escape")
                    pygame.quit()
                    raise SystemExit

            # if self.__mode == "ai":
            #     if frame % self.__action_frequency == 0:
            #         self.gnome_vision = helpers.make_gnome_vision(self.state, self.gnome.vision_size,
            #                                                       self.gnome.x, self.gnome.y)
            #
            #         gnome_vision_flat = helpers.flatten_gnome_vision(self.gnome_vision)
            #
            #         gnome_vision_flat.extend([self.get_gold(), self.get_exit(), self.get_gnome().x, self.get_gnome().y])
            #
            #         if self.play:
            #             print(gnome_vision_flat)
            #
            #         reshaped_state = np.reshape(gnome_vision_flat, [1, self.state_size])
            #         action = self.model.predict(reshaped_state)
            #         self.gnome_vision = self.step(action)
            #
            #         done = helpers.check_if_exit(self.gnome)
            #         if done:
            #             self.soft_reset()

            action_taken = False

            # Build up a black screen as a game background
            screen.fill(constants.GAME_BACKGROUND)

            helpers.draw_game(screen, self.__scanned_map, self.__covered_map, self.__gnome)

            # GOLD PLACEHOLDER
            gold_text_placeholder, gold_rect_text_placeholder = helpers.update_gold_text_placeholder(font)
            screen.blit(gold_text_placeholder, gold_rect_text_placeholder)

            # EXIT PLACEHOLDER
            exit_text_placeholder, exit_rect_text_placeholder = helpers.update_exit_text_placeholder(font)
            screen.blit(exit_text_placeholder, exit_rect_text_placeholder)

            # GEM PLACEHOLDER
            gem_text_placeholder, gem_rect_text_placeholder = helpers.update_gem_text_placeholder(font)
            screen.blit(gem_text_placeholder, gem_rect_text_placeholder)

            # STEPS PLACEHOLDER
            steps_text_placeholder, steps_rect_text_placeholder = helpers.update_steps_text_placeholder(font)
            screen.blit(steps_text_placeholder, steps_rect_text_placeholder)

            # EXIT
            exit_text, exit_text_rect = helpers.update_exit_text(font, self.get_exit())
            screen.blit(exit_text, exit_text_rect)

            # GOLD
            gold_text, gold_text_rect = helpers.update_gold_text(font, self.get_gold())
            screen.blit(gold_text, gold_text_rect)

            # GEM
            gem_text, gem_text_rect = helpers.update_gem_text(font, self.get_gem())
            screen.blit(gem_text, gem_text_rect)

            # STEPS
            steps_text, steps_text_rect = helpers.update_steps_text(font, self.get_steps())
            screen.blit(steps_text, steps_text_rect)

            # update display
            pygame.display.flip()
            frame += 1

    def play(self):
        if self.__mode == "ai":
            print("ai playing")
        self.__initialize_game()