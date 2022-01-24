import pygame

from utils import config

"""Container to hold and render text.
"""


class PopUpImage:
    """Constructor to define and load the images.

    :param font: Font object to use to render text
    :type font: pygame Font
    """

    def __init__(self, font):
        self.current_text = ''
        self.font = font
        # How much the text fades
        self.alpha_decrease = 0
        # Maximum transparency
        self.max_alpha = 200
        self.current_alpha = self.max_alpha
        self.width = config.display_width
        self.height = config.display_height

    """Returns the given frame of the image.

    :param effect: Effect to grab frame and other information from
    :type effect: PopUp
    :returns: Frame to show
    :rtype: pygame image
    """

    def get_frame(self, effect):
        if effect.text != self.current_text:
            # New text, resets all fields
            self.current_alpha = self.max_alpha
            self.current_text = effect.text
            # Places text image on center of screen
            self.alpha_decrease = self.max_alpha // effect.max_frame
        image = self.font.render(effect.text, 1, (255, 255, 255)).convert_alpha()
        rect = image.get_rect(center=(effect.center_x, effect.center_y))
        effect.x, effect.y = rect.topleft
        effect.curr_frame += 1
        self.current_alpha -= self.alpha_decrease
        if self.current_alpha <= 0:
            self.current_alpha = self.max_alpha
        image.fill((255, 255, 255, self.current_alpha), None, pygame.BLEND_RGBA_MULT)
        return image
