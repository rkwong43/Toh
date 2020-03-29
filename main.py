import pygame
import sys
import os

# Makes sure the game knows where the files are located:
current_path = os.path.dirname(__file__)  # where this file is located
outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the src folder
sys.path.insert(1, outer_path)

from src.controller.MenuController import MenuController
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
        menu_view = MenuView()
        menu_controller = MenuController(menu_view)
        game_mode, difficulty, weapon_selected, player = menu_controller.run_menus()
        # If window is closed
        if weapon_selected is None:
            break
        view = View(game_mode)
        model = Model(weapon_selected, difficulty, game_mode, player)
        model.clear()
        controller = Controller(model, view)
        finished = not controller.run_game()


"""Starts the game and initializes the music player.
"""


def main():
    pygame.mixer.pre_init(channels=32)
    pygame.init()
    start_game()
    pygame.quit()
    pygame.mixer.quit()


if __name__ == "__main__":
    start_game()
