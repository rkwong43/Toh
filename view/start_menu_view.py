
import os
import pygame

"""View to render the game, uses pygame to render images. Represents the start menu.
"""


class StartMenuView:
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
    """

    def __init__(self, display_width, display_height, game_title):
        # Sets up the game window surface
        self.game_display = pygame.display.set_mode((display_width, display_height))
        # Title of the window
        pygame.display.set_caption(game_title)
        # Background image is 1920 x 1080
        self.background = pygame.image.load(self.background_path)
        self.width = display_width
        self.height = display_height
        self.font_size = display_height / 10
        font_path = os.path.join(self.resource_path, 'fonts')
        font_path = os.path.join(font_path, 'insane_hours_2.ttf')
        self.text_font = pygame.font.Font(font_path, int(self.font_size))
        title_font = pygame.font.Font(font_path, int(display_height / 20))
        # Title
        self.title = title_font.render(game_title, 1, (255, 255, 255))
        # Title dimensions
        title_width, title_height = pygame.font.Font.size(self.text_font, game_title)
        self.title_x = display_width / 2 - title_width / 2
        self.title_y = display_height / 2 - title_height

        self.background_x = 0
        self.background_y = 0
        # Prompt to start the game
        self.start_font = pygame.font.Font(font_path, int(self.font_size / 4))
        self.start_prompt = self.start_font.render("Press [Space] to Begin", 1, (255, 255, 255)).convert_alpha()
        prompt_width, prompt_height = pygame.font.Font.size(self.start_font, "Press [Space] to Begin")
        self.prompt_x = (display_width / 2) - (prompt_width / 2)
        self.prompt_y = self.title_y + title_height + (2 * prompt_height)
        self.prompt_alpha = 200
        self.prompt_alpha_change = -2

    """Renders the start menu, which consists of a title and the prompt to start the game.
    """

    def render(self):
        self.game_display.blit(self.background, (self.background_x, self.background_y))
        title_rect = self.title.get_rect(center=(int(self.width / 2), int(self.height / 2.5)))
        self.game_display.blit(self.title, title_rect.topleft)
        if self.background_x > -self.width or self.background_y > 2 * -self.height:
            self.background_x -= 1
            self.background_y -= 1
        self.prompt_alpha += self.prompt_alpha_change
        image = self.start_prompt.copy()
        image.fill((255, 255, 255, self.prompt_alpha), None, pygame.BLEND_RGBA_MULT)
        self.game_display.blit(image, (self.prompt_x, self.prompt_y))
        if self.prompt_alpha <= 50 or self.prompt_alpha >= 200:
            self.prompt_alpha_change *= -1
