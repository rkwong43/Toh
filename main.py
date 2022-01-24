import pygame
from model.menu_model import MenuModel
from utils import config, score_storage
from controller.menu_controller import MenuController
from controller.controller import Controller
from model.model import Model
from view.menu_view import MenuView
from view.view import View

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
