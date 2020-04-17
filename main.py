import pygame
import sys
import os

# Makes sure the game knows where the files are located:

current_path = os.path.dirname(__file__)  # where this file is located
outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the src folder
sys.path.insert(1, outer_path)

from src.model.menu_model import MenuModel
from src.utils import config, score_storage
from src.controller.menu_controller import MenuController
from src.controller.controller import Controller
from src.model.model import Model
from src.view.menu_view import MenuView
from src.view.view import View

"""Starts the game and loops until exit.
"""


def start_game():
    finished = False
    # Loops until finished
    while not finished:
        menu_model = MenuModel()
        menu_view = MenuView(menu_model)
        menu_controller = MenuController(menu_view, menu_model)
        game_mode, difficulty, play_game = menu_controller.run_menus()
        # If window is closed
        if not play_game:
            score_storage.save_data()
            break
        view = View(game_mode)
        model = Model(difficulty, game_mode)
        model.switch_weapon(config.weapon)
        controller = Controller(model, view)
        finished = not controller.run_game()
        if not finished:
            finished = menu_controller.display_score(model.get_score())
        else:
            score_storage.save_data()


"""Starts the game and initializes the music player.
"""


def main():
    pygame.mixer.pre_init(channels=32)
    pygame.init()
    start_game()
    pygame.quit()
    pygame.mixer.quit()


if __name__ == "__main__":
    main()
