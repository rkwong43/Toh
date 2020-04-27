import pygame

from src.utils import config

"""Container to hold images for an explosion.
"""


class ExplosionImages:
    """Constructor to define and load the images.

    :param images: list of image names
    :type images: List of str
    :param size: size to scale images to
    :type size: int
    """

    def __init__(self, images, size):
        self.frames = []
        for image in images:
            frame = pygame.image.load(image).convert_alpha()
            frame = pygame.transform.scale(frame, (size, size))
            self.frames.append(frame)
        self.frame_offset = int(config.game_fps / 30)

    """Returns the given frame of the explosion.
    
    :param effect: Effect to grab frame and other information from
    :type effect: Effect
    :returns: Frame to show
    :rtype: pygame image
    """
    def get_frame(self, effect):
        try:
            result = self.frames[int(effect.curr_frame / (self.frame_offset * effect.frame_multiplier))]
        except IndexError:
            result = self.frames[0]
        effect.curr_frame += 1
        return result
