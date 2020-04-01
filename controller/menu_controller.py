import pygame
import os

from src.utils import config
from src.utils.direction import Direction
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.game_id import GameID
from src.utils.ids.gamemode_id import GameModeID
from src.utils.ids.player_id import PlayerID
from src.utils.ids.weapon_id import WeaponID
from src.view.image_containers.menu_gallery import MenuGallery
from src.view.menu_selector import MenuSelector
from src.view.menu_tree import MenuTree

difficulties = [difficulty for difficulty in DifficultyID]

"""Creates a dictionary of gallery objects to display information for.

:param ids: list of IDs
:type ids: EntityID
:returns: list of gallery items
:rtype: list of MenuGallery
"""


def construct_gallery(ids):
    result = {}
    for entity in ids:
        gallery = MenuGallery(entity)
        result[entity] = gallery
    return result


"""Constructs the menu tree for the menus.

:returns: the root
:rtype: MenuTree
"""


def construct_tree():
    # TODO: Loadout menu
    difficulty_selector = MenuSelector(difficulties, GameID.SELECTOR, None)
    survival = MenuSelector([GameModeID.CLASSIC,
                             GameModeID.MANDIBLE_MADNESS,
                             GameModeID.HEAVEN],
                            GameID.SELECTOR, difficulty_selector)
    challenge = MenuSelector([GameModeID.TITAN_SLAYER],
                             GameID.SELECTOR, difficulty_selector)
    weapon_gallery = MenuTree(GameID.GALLERY, construct_gallery([weapon for weapon in WeaponID]))
    ship_gallery = MenuTree(GameID.GALLERY, construct_gallery([ship for ship in PlayerID]))
    enemy_gallery = MenuTree(GameID.GALLERY, construct_gallery([enemy for enemy in EnemyID if enemy != EnemyID.TITAN]))
    hangar_page = MenuTree(GameID.HANGAR,
                           {GameID.SHIP: ship_gallery,
                            GameID.WEAPON: weapon_gallery,
                            GameID.ENEMY: enemy_gallery})
    main_menu = MenuTree(GameID.MENU,
                         {GameID.STORY: None,
                          GameID.SURVIVAL: survival,
                          GameID.CHALLENGE: challenge,
                          GameID.TUTORIAL: GameID.TUTORIAL,
                          GameID.HANGAR: hangar_page,
                          GameID.SETTINGS: None})
    return main_menu


"""Controller that allows for traversing of the menus.
"""


class MenuController:
    current_path = os.path.dirname(__file__)  # where this file is located
    outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the View folder
    resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
    music_path = os.path.join(resource_path, 'music')  # the music folder path
    _tree = construct_tree()
    _main_menu = _tree

    _weapon_chosen = None
    _player = PlayerID.CITADEL
    """Constructor that takes in a view to run the menus.

    :param menus: the menu view
    :type menus: MenuView
    :type fps: int
    """

    def __init__(self, menus):
        self._menus = menus
        self._fps = config.game_fps
        self._difficulty = None
        self._game_mode = None
        # Music by Scott Buckley – www.scottbuckley.com.au
        # Loads the start menu music
        pygame.mixer.music.load(os.path.join(self.music_path, 'undertow.mp3'))
        pygame.mixer.music.play(-1, 0)
        # To keep background continuity between the two views:

    """Figures out what to do depending on the key inputs.

    :param key: key released
    :type key: pygame key constant
    """

    def _parse_key_input(self, key):
        if self._tree.name in GameID:
            direction = None
            if key == pygame.K_w:
                direction = Direction.UP
            elif key == pygame.K_s:
                direction = Direction.DOWN
            self._tree.switch_selection(direction)

    """Runs the menus, allowing for the player to select game mode, difficulty, and weapon.

    :returns: tuple of game mode, difficulty, weapon, and ship chosen
    :rtype: (GameModeID, DifficultyID, WeaponID, PlayerID)
    """

    def run_menus(self):
        # In game clock for FPS and time
        clock = pygame.time.Clock()
        quit_options = (None, None, None, None)
        # _start_screen returns true if quit
        while True:
            if self._start_screen(clock):
                return quit_options
            """Flags:
            1: start game
            0: go back to title screen
            -1: quit game
            """
            flag = self._run_menus_helper(clock)
            if flag == 1:
                return self._game_mode, self._difficulty, self._weapon_chosen, self._player
            elif flag == 0:
                continue
            else:
                return quit_options

    """Runs the internal menu tree.
    
    :param clock: pygame clock
    :type clock: pygame Clock
    :returns: True if the start menu should be rerun, false otherwise
    :rtype: bool
    """

    def _run_menus_helper(self, clock):
        ANIMATE = pygame.USEREVENT + 1
        pygame.time.set_timer(ANIMATE, 300)
        done = False
        while not done:
            # Grabs the keys currently pressed down
            keys = pygame.key.get_pressed()
            self._menus.render_menu(self._tree)
            self._parse_key_input(keys)
            # Gets game_events
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    return -1
                elif game_event.type == pygame.KEYUP:
                    self._parse_key_input(game_event.key)
                    # Selects the current option if space is pressed
                    if game_event.key == pygame.K_SPACE and self._tree.name in GameID:
                        # Selects the current option
                        done = self._select_option()
                    # Goes back a layer
                    elif game_event.key == pygame.K_ESCAPE or game_event.key == pygame.K_BACKSPACE:
                        if not self._go_back_menu():
                            return 0
                # Animates sprites
                if game_event.type == ANIMATE:
                    self._menus.animate()
            # Updates display
            pygame.display.update()
            clock.tick(self._fps)
        return 1

    """Selects the current option on the current tree. Returns true if entering gameplay.
    
    :returns: True if beginning game, False otherwise
    :rtype: bool
    """

    def _select_option(self):
        ID, destination = self._tree.select()
        if self._tree.name == GameID.SELECTOR:
            # Selecting options
            if ID in DifficultyID:
                self._difficulty = ID
            else:
                self._game_mode = ID
            self._tree = destination
            return False
        elif self._tree.name == GameID.LOADOUT:
            # Loadouts are preceded by a Selector
            self._weapon_chosen, self._player = self._tree.select
            return True
        else:
            # Tutorial selection
            if destination == GameID.TUTORIAL:
                # Preset values for gear
                self._weapon_chosen = WeaponID.GUN
                self._player = PlayerID.CITADEL
                self._game_mode = GameID.TUTORIAL
                self._difficulty = DifficultyID.EASY
                return True
            elif destination is not None:
                self._tree = destination
            # Covers cases where destination is a MenuTree or MenuGallery
            return False

    """Goes back to the current tree's roots.
    
    :returns: True if the root is a valid menu, false otherwise (main menu)
    :rtype: bool
    """

    def _go_back_menu(self):
        new_tree = self._tree.goto_root()
        if new_tree is None:
            self._tree = self._main_menu
            return False
        else:
            self._tree = new_tree
            return True

    """Defines the starting menu screen for the game. Returns a boolean whether the user exited the window.

    :param clock: pygame clock to tick
    :type clock: pygame clock
    :returns: boolean whether the user manually exited
    :rtype: bool
    """

    def _start_screen(self, clock):
        finished = False
        # Loops until the user quits or presses space to begin
        while not finished:
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    return True
                elif game_event.type == pygame.KEYUP:
                    if game_event.key == pygame.K_SPACE:
                        return False
            self._menus.render_menu(None)
            pygame.display.update()
            clock.tick(self._fps)
