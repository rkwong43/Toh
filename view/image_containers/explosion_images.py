import pygame

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
        frame1 = pygame.image.load(images[0])
        frame1 = pygame.transform.scale(frame1, (size, size))
        frame2 = pygame.image.load(images[1])
        frame2 = pygame.transform.scale(frame2, (size, size))
        frame3 = pygame.image.load(images[2])
        frame3 = pygame.transform.scale(frame3, (size, size))
        frame4 = pygame.image.load(images[3])
        frame4 = pygame.transform.scale(frame4, (size, size))
        frame5 = pygame.image.load(images[4])
        frame5 = pygame.transform.scale(frame5, (size, size))
        self.frames = [frame1, frame2, frame3, frame4, frame5]

    """Returns the given frame of the explosion.
    
    :param effect: Effect to grab frame and other information from
    :type effect: Effect
    :returns: Frame to show
    :rtype: pygame image
    """
    def get_frame(self, effect):
        result = self.frames[effect.curr_frame]
        effect.curr_frame += 1
        return result
