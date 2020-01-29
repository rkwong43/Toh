import os
import pygame

from src.entity_id import EntityID
from src.model.menu_model import MenuModel
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

    def __init__(self, display_width, display_height, game_title, ship_size, fps):
        # Sets up the game window surface
        super().__init__(display_width, display_height, game_title, ship_size, None, fps)
        self.game_display = pygame.display.set_mode((display_width, display_height))
        # Title of the window
        pygame.display.set_caption(game_title)
        # Background image is 1920 x 1080
        # For scrolling background
        self.background = pygame.image.load(self.background_path).convert_alpha()
        self.background_x = 0
        self.background_y = 0
        self.width = display_width
        self.height = display_height
        self.font_size = display_height / 20
        # Title font size
        self.title_font_size = display_height / 10
        font_path = os.path.join(self.resource_path, 'fonts')
        font_path = os.path.join(font_path, 'insane_hours_2.ttf')
        self.text_font = pygame.font.Font(font_path, int(self.font_size))
        prompt_width, prompt_height = pygame.font.Font.size(self.text_font, "TEST")
        self.text_height = int(prompt_height * 1.5)
        # TODO: ADD SCROLLING
        self.current = 0
        # Title attributes
        self.title = self.text_font.render(game_title, 1, (255, 255, 255)).convert_alpha()
        # Title dimensions
        title_width, title_height = pygame.font.Font.size(self.text_font, game_title)
        self.title_x = display_width / 2 - title_width / 2
        self.title_y = display_height / 2 - title_height
        # Prompt to start the game
        self.start_font = pygame.font.Font(font_path, int(self.title_font_size / 4))
        self.start_prompt = self.start_font.render("Press [Space] to Begin", 1, (255, 255, 255)).convert_alpha()
        prompt_width, prompt_height = pygame.font.Font.size(self.start_font, "Press [Space] to Begin")
        self.prompt_x = (display_width / 2) - (prompt_width / 2)
        self.prompt_y = self.title_y + title_height + (2 * prompt_height)
        self.prompt_alpha = 200
        self.prompt_alpha_change = -2
        # If the current view is a description or gallery
        self.gallery = False
        self.description_font = pygame.font.Font(font_path, int(self.font_size / 2))
        # When to switch animations:
        self.animation_switch = False
        # Mock model to simulate gallery items
        self.model = MenuModel(display_width, display_height, ship_size, fps)

    """Renders menu options.
    
    :param tree: Tree to get options from.
    :type tree: MenuTree
    """

    def render_menu(self, tree):
        # TODO: ADD ANIMATIONS FOR SCROLLING BETWEEN OPTIONS
        if self.gallery:
            self.model.play = True
            self.render_gallery(tree)
        else:
            self.model.play = False
            self.model.clear()
            if tree is None:
                self.render_title_screen()
            else:
                self.render_background()
                text_to_render = tree.options
                curr_selected = tree.current_selection
                # Images to render
                images = []
                for i in range(0, len(text_to_render)):
                    image = self.text_font.render(text_to_render[i], 1, (255, 255, 255)).convert_alpha()
                    if i != curr_selected:
                        image.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)
                    images.append(image)
                upper_difference = curr_selected * self.text_height
                y = (self.height // 2) - upper_difference
                x = self.width // 2
                # Renders all the text
                for image in images:
                    pos = (x, y)
                    rect = image.get_rect(center=pos)
                    self.game_display.blit(image, rect.topleft)
                    y += self.text_height

    """Renders the title screen.
    """

    def render_title_screen(self):
        self.render_background()
        title_rect = self.title.get_rect(center=(int(self.width / 2), int(self.height / 2.5)))
        self.game_display.blit(self.title, title_rect.topleft)
        self.prompt_alpha += self.prompt_alpha_change
        image = self.start_prompt.copy()
        image.fill((255, 255, 255, self.prompt_alpha), None, pygame.BLEND_RGBA_MULT)
        self.game_display.blit(image, (self.prompt_x, self.prompt_y))
        if self.prompt_alpha <= 50 or self.prompt_alpha >= 200:
            self.prompt_alpha_change *= -1

    """Renders the background for the menus.
    """

    def render_background(self):
        self.game_display.fill((0, 0, 0))
        self.game_display.blit(self.background, (self.background_x, self.background_y))
        if self.background_x > -self.width or self.background_y > 2 * -self.height:
            self.background_x -= 1
            self.background_y -= 1

    """Renders the given gallery object.
    
    :param gallery: gallery with the information to render.
    :type gallery: MenuGallery
    """

    def render_gallery(self, gallery):
        self.model.tick()
        # Name of the current entity being viewed
        self.render_background()
        # Render a ship or weapon?
        if gallery.entity_type == EntityID.WEAPON:
            self.model.switch_weapon(gallery.entity_id)
        else:
            self.model.spawn_ship(gallery.entity_id)
        self.render(self.model.player_ship, self.model.get_projectiles(),
                    self.model.get_enemies(), self.model.get_effects())
        # Title and description
        name_displayed = self.text_font.render(str(gallery.name), 1, (255, 255, 255)).convert_alpha()
        name_rect = name_displayed.get_rect(center=(int(self.width / 2), int(self.height / 10)))
        self.game_display.blit(name_displayed, name_rect.topleft)
        description = self.description_font.render(gallery.description, 0, (255, 255, 255)).convert_alpha()
        description_rect = description.get_rect(center=(int(self.width / 2), int(self.height / 6)))
        self.game_display.blit(description, description_rect.topleft)
        # Other stats to show
        offset = 0
        for stat in gallery.stats:
            stat_displayed = self.description_font.render(stat, 0, (255, 255, 255)).convert_alpha()
            stat_rect = stat_displayed.get_rect(center=(int(self.width * .7), int(self.height / 4) + offset))
            offset += self.ship_size // 4
            self.game_display.blit(stat_displayed, stat_rect.topleft)

    """Renders the game, including background, ships, and projectiles.

       :param items: ships and projectiles to render
       :type items: list of Ship or Projectile
       """

    def render(self, player, projectiles, enemies, effects):
        # If the player isn't dead, it is rendered
        self.render_ship(player, 0)
        # Renders enemies to face the player
        for enemy in enemies:
            self.render_ship(enemy, enemy.angle)
        # Renders projectiles
        for projectile in projectiles:
            self.render_projectile(projectile)
        # Renders effects
        for effect in effects:
            if self.render_effect(effect):
                effects.remove(effect)
