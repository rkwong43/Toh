import pygame
import os

from src.utils.direction import Direction
from src.utils.entity_id import EntityID
from src.view.image_containers.menu_gallery import MenuGallery
from src.view.menu_tree import MenuTree

"""Controller that allows for traversing of the menus.
"""


class MenuController:

    """Constructor that takes in a view to run the menus.

    :param menus: the menu view
    :type menus: MenuView
    :param fps: Frames per second to run game on
    :type fps: int
    """

    def __init__(self, menus, fps):
        self.menus = menus
        self.fps = fps
        # Selection ticks for the delay before moving selection
        self.ticks = fps // 6
        self.tick_limit = fps // 6
        # Music by Scott Buckley – www.scottbuckley.com.au
        current_path = os.path.dirname(__file__)  # where this file is located
        outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the View folder
        resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
        music_path = os.path.join(resource_path, 'music')  # the music folder path
        self.start_menu_music_path = os.path.join(music_path, 'undertow.mp3')
        self.difficulty_selection_tree = None
        self.weapon_selection_tree = None
        self.tree = self.construct_tree()
        # To keep background continuity between the two views:

    """Constructs the menu tree for the menus.
    
    :returns: the root
    :rtype: MenuTree
    """

    def construct_tree(self):
        # WEAPONS
        weapon_selection = ["GUN", "SHOTGUN", "MACHINE GUN", "FLAK GUN", "FLAK CANNON", "MISSILE LAUNCHER",
                            "MISSILE BATTERY",
                            "DIAMOND DUST", "STRIKER", "RAILGUN"]
        weapon_ids = [EntityID.GUN, EntityID.SHOTGUN, EntityID.MACHINE_GUN, EntityID.FLAK_GUN, EntityID.FLAK_CANNON,
                      EntityID.MISSILE_LAUNCHER, EntityID.MULTI_MISSILE, EntityID.BAD_MISSILE_LAUNCHER,
                      EntityID.STRIKER, EntityID.RAILGUN]
        # ENEMIES
        enemy_selection = ["MANDIBLE", "MANTIS", "MOSQUITO", "SEER", "SUBJUGATOR", "CRUCIBLE", "ARBITRATOR", "TERMINUS",
                           "JUDICATOR", "DESPOILER", "MOTHERSHIP"]
        enemy_ids = [EntityID.MANDIBLE, EntityID.MANTIS, EntityID.MOSQUITO, EntityID.SEER, EntityID.SUBJUGATOR,
                     EntityID.CRUCIBLE, EntityID.ARBITRATOR, EntityID.TERMINUS, EntityID.JUDICATOR, EntityID.DESPOILER,
                     EntityID.MOTHERSHIP]
        # Tree to select weapons
        self.weapon_selection_tree = MenuTree(weapon_selection, weapon_ids, None)
        # Tree to select difficulty
        difficulty_selection = ["EASY", "NORMAL", "HARD"]
        difficulty_ids = [EntityID.EASY, EntityID.NORMAL, EntityID.HARD]
        self.difficulty_selection_tree = MenuTree(difficulty_selection, difficulty_ids, None)
        self.weapon_selection_tree.root = self.difficulty_selection_tree
        # Challenge Options
        challenge_layer = ["TITAN SLAYER"]
        challenge_tree = MenuTree(challenge_layer, [0], [EntityID.TITAN_SLAYER])
        # Survival options
        survival_layer = ["CLASSIC", "MANDIBLE MADNESS", "HEAVEN", "TERMINUS TERRORS (COMING SOON)",
                          "TIME ATTACK (COMING SOON)"]
        survival_tree = MenuTree(survival_layer, [0, 0, 0, -1, -1], [EntityID.SURVIVAL, EntityID.MANDIBLE_MADNESS,
                                                                     EntityID.HEAVEN])
        # MENUS
        # Hangar
        hangar_layer = ["SHIPS (COMING SOON", "WEAPONS", "ENEMIES"]
        weapon_descriptions = self.construct_gallery(weapon_ids)
        enemy_descriptions = self.construct_gallery(enemy_ids)
        gallery_list_weapons = [EntityID.GALLERY] * (len(weapon_selection))
        gallery_list_enemies = [EntityID.GALLERY] * (len(enemy_selection))
        gallery_weapons = MenuTree(weapon_selection, weapon_descriptions, gallery_list_weapons)
        gallery_enemies = MenuTree(enemy_selection, enemy_descriptions, gallery_list_enemies)
        for gallery in weapon_descriptions:
            gallery.root = gallery_weapons
        for gallery in enemy_descriptions:
            gallery.root = gallery_enemies
        hangar_tree = MenuTree(hangar_layer, [-1, gallery_weapons, gallery_enemies], [0, 0, 0])
        first_layer = ["STORY (COMING SOON)", "SURVIVAL", "CHALLENGE",
                       "TUTORIAL", "HANGAR", "SETTINGS (COMING SOON)"]
        main_menu_tree = MenuTree(first_layer, [-1, survival_tree, challenge_tree, 0, hangar_tree, -1],
                                  [0, 0, 0, EntityID.TUTORIAL, 0, -1])
        gallery_enemies.root = hangar_tree
        gallery_weapons.root = hangar_tree
        hangar_tree.root = main_menu_tree
        survival_tree.root = main_menu_tree
        challenge_tree.root = main_menu_tree
        return main_menu_tree

    """Figures out what to do depending on the key inputs.
    
    :param key: key released
    :type key: pygame key constant
    """

    def parse_key_input(self, key):
        if not self.menus.gallery:
            direction = None
            if key == pygame.K_w:
                direction = Direction.UP
            elif key == pygame.K_s:
                direction = Direction.DOWN
            self.tree.switch_selection(direction)

    """Runs the menus, allowing for the player to select game mode, difficulty, and weapon.

    :returns: tuple of game mode, difficulty, and weapon
    :rtype: (EntityID, EntityID, EntityID)
    """

    def run_menus(self):
        # Things to return:
        game_mode = None
        difficulty = None
        weapon_chosen = None
        # In game clock for FPS and time
        clock = pygame.time.Clock()
        # Defines if the game is done
        done = False
        select_difficulty = False
        select_weapon = False
        if self.start_screen(clock):
            done = True
        # Loops on the menu
        while not done:
            if self.ticks < self.tick_limit:
                self.ticks += 1
            else:
                self.menus.animate()
                self.ticks = 0
            # Grabs the keys currently pressed down
            keys = pygame.key.get_pressed()
            self.menus.render_menu(self.tree)
            self.parse_key_input(keys)
            # Gets game_events
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    done = True
                elif game_event.type == pygame.KEYUP:
                    self.parse_key_input(game_event.key)
                    # Selects the current option if space is pressed
                    if game_event.key == pygame.K_SPACE:
                        new_tree = self.tree.select()
                        if new_tree == 0:
                            if self.tree.name is not None:
                                game_mode = self.tree.name[self.tree.current_selection]
                                if game_mode == EntityID.TUTORIAL:
                                    return game_mode, EntityID.EASY, EntityID.GUN
                            select_difficulty = True
                            self.difficulty_selection_tree.root = self.tree
                            self.tree = self.difficulty_selection_tree
                        elif select_difficulty:
                            difficulty = new_tree
                            select_weapon = True
                            select_difficulty = False
                            self.tree = self.weapon_selection_tree
                        elif select_weapon:
                            weapon_chosen = new_tree
                            done = True
                        elif new_tree != -1:
                            if self.tree.name[self.tree.current_selection] == EntityID.GALLERY:
                                self.menus.gallery = True
                            self.tree = new_tree
                    # Goes back a layer
                    elif game_event.key == pygame.K_ESCAPE or game_event.key == pygame.K_BACKSPACE:
                        new_tree = self.tree.goto_root()
                        self.menus.gallery = False
                        self.menus.model.clear()
                        if select_weapon:
                            select_weapon = False
                            select_difficulty = True
                        elif select_difficulty:
                            select_difficulty = False
                        if new_tree is not None:
                            self.tree = new_tree
                        else:
                            if self.start_screen(clock):
                                done = True
            # Updates display
            pygame.display.update()
            clock.tick(self.fps)
        return game_mode, difficulty, weapon_chosen

    """Defines the starting menu screen for the game. Returns a boolean whether the user exited the window.

    :param clock: pygame clock to tick
    :type clock: pygame clock
    :returns: boolean whether the user manually exited
    :rtype: bool
    """

    def start_screen(self, clock):
        # Loads the start menu music
        pygame.mixer.music.load(self.start_menu_music_path)
        pygame.mixer.music.play(-1, 0)
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
            self.menus.render_menu(None)
            pygame.display.update()
            clock.tick(self.fps)

    """Creates a list of gallery objects to display information for.
    :param ids: list of IDs
    :type ids: EntityID
    :returns: list of gallery items
    :rtype: list of MenuGallery
    """

    def construct_gallery(self, ids):
        result = []
        for entity in ids:
            gallery = MenuGallery(entity)
            result.append(gallery)
        return result
