import pygame

from src.controller.MenuController import MenuController
from src.controller.controller import Controller
from src.model.model import Model
from src.view.menu_view import MenuView
from src.view.view import View


def main():
    # Display settings and constants
    display_width = 1000
    display_height = 750
    game_title = 'Tears Over Heaven'
    game_fps = 32
    ship_size = 100
    finished = False
    while not finished:
        menu_view = MenuView(display_width, display_height, game_title, ship_size, game_fps)
        menu_controller = MenuController(menu_view, game_fps)
        game_mode, difficulty, weapon_selected = menu_controller.run_menus()
        if weapon_selected is None:
            break
        view = View(display_width, display_height, game_title, ship_size, game_mode)
        model = Model(display_width, display_height, ship_size, game_fps, weapon_selected, difficulty, game_mode)
        model.clear()
        controller = Controller(model, view, game_fps)
        finished = not controller.run_game()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
    quit()
