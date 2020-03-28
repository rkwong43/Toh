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
    # Display settings and constants
    # Default, will allow resizing in future.
    display_width = 1000
    display_height = 750
    game_title = 'Tears Over Heaven'
    game_fps = 60
    ship_size = 100
    finished = False
    # Loops until finished
    while not finished:
        menu_view = MenuView(display_width, display_height, game_title, ship_size, game_fps)
        menu_controller = MenuController(menu_view, game_fps)
        game_mode, difficulty, weapon_selected, player = menu_controller.run_menus()
        # If window is closed
        if weapon_selected is None:
            break
        view = View(display_width, display_height, game_title, ship_size, game_mode, game_fps)
        model = Model(display_width, display_height, ship_size, game_fps, weapon_selected, difficulty,
                      game_mode, player)
        model.clear()
        controller = Controller(model, view, game_fps)
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
