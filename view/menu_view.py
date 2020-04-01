import os
import pygame

from src.model.menu_model import MenuModel
from src.utils import config
from src.utils.ids.game_id import GameID
from src.view.view import View

"""View to render the game, uses pygame to render images. Represents the menus in game.
"""


class MenuView(View):
    # Image paths
    current_path = os.path.dirname(__file__)  # where this file is located
    outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the View folder
    resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
    image_path = os.path.join(resource_path, 'images')  # the image folder path
    background_path = os.path.join(image_path, 'background.png')

    """Constructor to initialize the game display.

    :param display_width: width of the window
    :type display_width: int
    :param display_height: height of the window
    :type display_height: int
    :param game_title: caption to put as the window title
    :type game_title: str
    :param ship_size: Size of ships to draw
    :type ship_size: int
    :param fps: Frames per second
    :type fps: int
    """

    def __init__(self):
        # Sets up the game window surface
        super().__init__(GameID.MENU)
        # Background image is 1920 x 1080
        # For scrolling background
        self._init_background()
        # Title font size
        self._title_font_size = config.display_height / 10
        font_path = os.path.join(self.resource_path, 'fonts')
        font_path = os.path.join(font_path, 'insane_hours_2.ttf')
        self._text_font = pygame.font.Font(font_path, int(self._font_size))
        prompt_width, prompt_height = pygame.font.Font.size(self._text_font, "TEST")
        self._text_height = int(prompt_height * 1.5)
        # TODO: ADD SCROLLING
        self._current = 0
        self._init_title_screen(font_path)
        self._description_font = pygame.font.Font(font_path, int(self._font_size / 2))
        # When to switch animations:
        # Mock model to simulate gallery items
        self._model = MenuModel()

    """Initializes the background.
    """

    def _init_background(self):
        self._background = pygame.image.load(self.background_path).convert_alpha()
        self._background_x = 0
        self._background_change = 1 * (30 / config.game_fps)
        self._font_size = config.display_height // 24

    """Initializes the title screen attributes.
    
    :param font_path: The file pathing for the font
    :type font_path: str
    """

    def _init_title_screen(self, font_path):
        # Title attributes
        self._title = self._text_font.render(config.game_title, 1, (255, 255, 255)).convert_alpha()
        # Title dimensions
        title_width, title_height = pygame.font.Font.size(self._text_font, config.game_title)
        self._title_x = config.display_width / 2 - title_width / 2
        self._title_y = config.display_width / 2 - title_height
        # Prompt to start the game
        self._start_font = pygame.font.Font(font_path, int(self._title_font_size / 4))
        self._start_prompt = self._start_font.render("Press [Space] to Begin", 1, (255, 255, 255)).convert_alpha()
        prompt_width, prompt_height = pygame.font.Font.size(self._start_font, "Press [Space] to Begin")
        self._prompt_x = (config.display_width / 2) - (prompt_width / 2)
        self._prompt_y = self._title_y + title_height + (2 * prompt_height)
        # Alpha levels for anything that fades or glows
        self._prompt_alpha = 150
        self._prompt_alpha_change = -2

    """Renders menu options.

    :param tree: Tree to get options from.
    :type tree: MenuTree
    """

    def render_menu(self, tree):
        # TODO: ADD ANIMATIONS FOR SCROLLING BETWEEN OPTIONS
        if tree is None:
            self._render_title_screen()
        elif tree.name not in GameID:
            self._model.set_play(True)
            self._render_gallery(tree)
        else:
            self._model.set_play(False)
            self._model.clear()
            if tree is None:
                self._render_title_screen()
            else:
                self._render_descriptive_menu(tree)

    """Renders a menu which may include descriptions or high scores.
    
    :param tree: The menu object to render
    :type tree: MenuSelector or MenuTree
    """

    def _render_descriptive_menu(self, tree):
        self._render_background()
        text_to_render = tree.get_options()
        curr_selected = self._current = tree.get_current_selection()
        # Images to render
        images = []
        for i in range(0, len(text_to_render)):
            text = text_to_render[i]
            image = self._text_font.render(text, 1, (255, 255, 255)).convert_alpha()
            if i != curr_selected:
                image.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)
            images.append(image)
        upper_difference = curr_selected * self._text_height
        y = (self._height // 2) - upper_difference
        if tree.name in [GameID.GALLERY, GameID.HANGAR]:
            x = self._width / 2
        else:
            x = self._width // 4
        pointer = self._text_font.render(">>", 1, (255, 255, 255)).convert_alpha()
        # Renders all the text
        pointer.fill((255, 255, 255, self._prompt_alpha), None, pygame.BLEND_RGBA_MULT)
        self._compute_alpha()
        for i in range(len(images)):
            image = images[i]
            pos = (x, y)
            rect = image.get_rect(center=pos)
            if i == curr_selected:
                pointer_rect = pointer.get_rect(topright=rect.topleft)
                self._game_display.blit(pointer, pointer_rect.topleft)
            self._game_display.blit(image, rect.topleft)
            y += self._text_height

    """Renders the title screen.
    """

    def _render_title_screen(self):
        self._render_background()
        title_rect = self._title.get_rect(center=(int(self._width / 2), int(self._height / 2.5)))
        self._game_display.blit(self._title, title_rect.topleft)
        self._compute_alpha()
        image = self._start_prompt.copy()
        image.fill((255, 255, 255, self._prompt_alpha), None, pygame.BLEND_RGBA_MULT)
        self._game_display.blit(image, (self._prompt_x, self._prompt_y))

    """Computes alpha values for anything that fades in and out.
    """

    def _compute_alpha(self):
        self._prompt_alpha += self._prompt_alpha_change
        if self._prompt_alpha < 60:
            self._prompt_alpha_change = 2
        elif self._prompt_alpha > 200:
            self._prompt_alpha_change = -2

    """Renders the background for the menus.
    """

    def _render_background(self):
        self._game_display.fill((0, 0, 0))
        self._game_display.blit(self._background, (self._background_x, self._background_y))
        if self._background_x > -self._width or self._background_y > 2 * -self._height:
            self._background_x -= self._background_change
            self._background_y -= self._background_change

    """Renders the given gallery object.

    :param gallery: gallery with the information to render.
    :type gallery: MenuGallery
    """

    def _render_gallery(self, gallery):
        self._model.tick()
        # Name of the current entity being viewed
        self._render_background()
        # Render a ship or weapon?
        if gallery.entity_type == GameID.WEAPON:
            self._model.switch_weapon(gallery.entity_id)
        else:
            self._model.spawn_ship(gallery.entity_id)
        self.render(self._model.get_player(), self._model.get_projectiles(),
                    self._model.get_enemies(), self._model.get_effects())
        # Title and description
        name_displayed = self._text_font.render(str(gallery.name), 1, (255, 255, 255)).convert_alpha()
        name_rect = name_displayed.get_rect(center=(int(self._width / 2), int(self._height / 10)))
        self._game_display.blit(name_displayed, name_rect.topleft)
        description = self._description_font.render(gallery.description, 0, (255, 255, 255)).convert_alpha()
        description_rect = description.get_rect(center=(int(self._width / 2), int(self._height / 6)))
        self._game_display.blit(description, description_rect.topleft)
        # Other stats to show
        offset = 0
        for stat in gallery.stats:
            stat_displayed = self._description_font.render(stat, 0, (255, 255, 255)).convert_alpha()
            stat_rect = stat_displayed.get_rect(center=(int(self._width * .7), int(self._height / 4) + offset))
            offset += self._ship_size // 4
            self._game_display.blit(stat_displayed, stat_rect.topleft)

    """Renders the game, including background, ships, and projectiles.

       :param items: ships and projectiles to render
       :type items: list of Ship or Projectile
       """

    def render(self, player, projectiles, enemies, effects):
        self._model.remove_effects()
        # If the player isn't dead, it is rendered
        self._render_ship(player, 0)
        # Renders enemies to face the player
        for enemy in enemies:
            self._render_ship(enemy, enemy.angle)
        # Renders projectiles
        for projectile in projectiles:
            self._render_projectile(projectile)
        # Renders effects
        for effect in effects:
            self._render_effect(effect)
