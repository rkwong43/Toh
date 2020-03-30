import pygame

from src.utils import config

"""Container to hold images for an explosion.
"""


class ScreenTintImages:
    """Constructor to define and load the images.

    :param image: image path
    :type image: List of str
    """

    def __init__(self, image):
        frame1 = pygame.image.load(image).convert_alpha()
        frame1 = pygame.transform.scale(frame1, (config.display_width, config.display_height))
        self.frame = frame1

    """Returns the given frame. Always returns a single frame.

    :param effect: Effect update to.
    :type effect: Effect
    :returns: Frame to show
    :rtype: pygame image"""

    def get_frame(self, effect):
        effect.curr_frame += 1
        return self.frame
