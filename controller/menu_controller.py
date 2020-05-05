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
from src.view.image_containers.menu_results import MenuResults
from src.view.loadout_selector import LoadoutSelector
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
    difficulty_selector = MenuSelector(difficulties, GameID.SELECTOR, LoadoutSelector())
    survival = MenuSelector([GameModeID.CLASSIC,
                             GameModeID.HEAVEN,
                             GameModeID.FATE,
                             GameModeID.ONSLAUGHT],
                            GameID.SELECTOR, difficulty_selector)
    challenge = MenuSelector([GameModeID.TITAN_SLAYER,
                              GameModeID.MANDIBLE_MADNESS,
                              GameModeID.SPECTRAL],
                             GameID.SELECTOR, difficulty_selector)
    weapon_gallery = MenuTree(GameID.GALLERY, construct_gallery([weapon for weapon in WeaponID]))
    ship_gallery = MenuTree(GameID.GALLERY, construct_gallery([ship for ship in PlayerID]))
    enemies_to_not_show = [EnemyID.TITAN, EnemyID.KING_MANDIBLE, EnemyID.QUEEN_MANDIBLE]
    enemy_gallery = MenuTree(GameID.GALLERY,
                             construct_gallery([enemy for enemy in EnemyID if enemy not in enemies_to_not_show]))
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
    """Constructor that takes in a view to run the menus.

    :param menus: the menu view
    :type menus: MenuView
    :param model: Model
    :type model: MenuModel
    """

    def __init__(self, menus, model):
        self._menus = menus
        self._model = model
        self._fps = config.game_fps
        self._difficulty = None
        self._game_mode = None
        # Music by Scott Buckley – www.scottbuckley.com.au
        # Loads the start menu music
        pygame.mixer.music.load(os.path.join(self.music_path, 'undertow.mp3'))
        pygame.mixer.music.play(-1, 0)
        pygame.mixer.music.set_volume(.5)
        # How many times the menu can transition per second in frames:
        self._option_transition = config.game_fps // 8.5
        self._curr_ticks = self._option_transition
        # Menu click
        path = os.path.join(self.resource_path, 'sounds')
        path = os.path.join(path, 'UI_change.ogg')
        self._menu_change_sound = pygame.mixer.Sound(file=path)
        self._menu_change_sound.set_volume(.1)
        self._clock = pygame.time.Clock()

        self.ANIMATE = pygame.USEREVENT + 1
        self.SPAWN_SHIPS = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ANIMATE, 300)
        pygame.time.set_timer(self.SPAWN_SHIPS, 1000)

    """Figures out what to do depending on the key inputs.

    :param keys: keys pressed
    :type keys: [pygame.key]
    """

    def _parse_key_input(self, keys):
        if self._tree.name in GameID:
            direction = None
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                direction = Direction.UP
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                direction = Direction.DOWN
            # Setting a limit for the number of options scrolled at once
            if self._curr_ticks == self._option_transition:
                if direction is not None:
                    self._menu_change_sound.play()
                self._tree.switch_selection(direction)
                self._curr_ticks = 0
            elif self._curr_ticks < self._option_transition:
                self._curr_ticks += 1

    """Runs the menus, allowing for the player to select game mode, difficulty, and weapon.

    :returns: tuple of game mode, difficulty, weapon, and ship chosen
    :rtype: (GameModeID, DifficultyID, WeaponID, PlayerID)
    """

    def run_menus(self):
        quit_options = (None, None, False)
        # _start_screen returns true if quit
        while True:
            if self._start_screen():
                return quit_options
            """Flags:
            1: start game
            0: go back to title screen
            -1: quit game
            """
            flag = self._run_menus_helper()
            if flag == 1:
                return self._game_mode, self._difficulty, True
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

    def _run_menus_helper(self):
        done = False
        while not done:
            # Grabs the keys currently pressed down
            keys = pygame.key.get_pressed()
            self._parse_key_input(keys)
            self._menus.render_menu(self._tree)
            # Gets game_events
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    return -1
                elif game_event.type == pygame.KEYUP:
                    # Selects the current option if space is pressed
                    if game_event.key == pygame.K_SPACE and self._tree.name in GameID:
                        # Selects the current option
                        done = self._select_option()
                    # Goes back a layer
                    elif game_event.key == pygame.K_ESCAPE or game_event.key == pygame.K_BACKSPACE:
                        if not self._go_back_menu():
                            return 0
                    elif game_event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_d, pygame.K_a]:
                        self._parse_horizontal_input(game_event.key)
                # Animates sprites
                if game_event.type == self.ANIMATE:
                    self._menus.animate()
                if game_event.type == self.SPAWN_SHIPS:
                    self._model.spawn_ships()
            # Updates display
            pygame.display.update()
            self._clock.tick(self._fps)
        return 1

    """Selects the current option on the current tree. Returns true if entering gameplay.
    
    :returns: True if beginning game, False otherwise
    :rtype: bool
    """

    def _select_option(self):
        ID, destination = self._tree.select()
        self._menu_change_sound.play()
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
            return True
        else:
            if self._tree.name == GameID.GALLERY:
                self._model.showcase(destination.entity_type, destination.entity_id)
            # Tutorial selection
            if destination == GameID.TUTORIAL:
                # Preset values for gear
                config.weapon = WeaponID.GUN
                config.player_ship = PlayerID.CITADEL
                self._game_mode = GameID.TUTORIAL
                self._difficulty = DifficultyID.EASY
                return True
            elif destination is not None:
                self._tree = destination
            return False

    """Goes back to the current tree's roots.
    
    :returns: True if the root is a valid menu, false otherwise (main menu)
    :rtype: bool
    """

    def _go_back_menu(self):
        self._model.reset_showcase()
        self._menu_change_sound.play()
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

    def _start_screen(self):
        # Loops until the user quits or presses space to begin
        while True:
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    return True
                elif game_event.type == pygame.KEYUP:
                    if game_event.key == pygame.K_SPACE:
                        return False
                if game_event.type == self.ANIMATE:
                    self._menus.animate()
                if game_event.type == self.SPAWN_SHIPS:
                    self._model.spawn_ships()
            self._menus.render_menu(None)
            pygame.display.update()
            self._clock.tick(self._fps)

    """Parses horizontal movement, which is not continuous upon holding down a key.
    
    :param key: The key released
    :type key: pygame key constant
    """

    def _parse_horizontal_input(self, key):
        direction = None
        if key == pygame.K_d or key == pygame.K_RIGHT:
            direction = Direction.RIGHT
        elif key == pygame.K_a or key == pygame.K_LEFT:
            direction = Direction.LEFT
        self._tree.switch_selection(direction)

    """Displays the final score screen.
    
    :returns: False if user doesn't exit the game
    :rtype: bool
    """

    def display_score(self, stats):
        self._model.reset_showcase()
        stats_container = MenuResults(stats)
        while True:
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    return True
                elif game_event.type == pygame.KEYUP:
                    if game_event.key in [pygame.K_SPACE, pygame.K_ESCAPE]:
                        return False
                if game_event.type == self.ANIMATE:
                    self._menus.animate()
                if game_event.type == self.SPAWN_SHIPS:
                    self._model.spawn_ships()
            self._menus.render_menu(stats_container)
            pygame.display.update()
            self._clock.tick(self._fps)
