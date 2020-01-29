import pygame

"""Container to hold images for an explosion.
"""


class ExplosionImages:
    """Constructor to define and load the images.

    :param images: list of image names
    :type images: List of str
    :param size: size to scale images to
    :type size: int
    :param fps: Frames per second to adjust each frame length to
    :type fps: int
    """

    def __init__(self, images, size, fps):
        frame1 = pygame.image.load(images[0]).convert_alpha()
        frame1 = pygame.transform.scale(frame1, (size, size))
        frame2 = pygame.image.load(images[1]).convert_alpha()
        frame2 = pygame.transform.scale(frame2, (size, size))
        frame3 = pygame.image.load(images[2]).convert_alpha()
        frame3 = pygame.transform.scale(frame3, (size, size))
        frame4 = pygame.image.load(images[3]).convert_alpha()
        frame4 = pygame.transform.scale(frame4, (size, size))
        frame5 = pygame.image.load(images[4]).convert_alpha()
        frame5 = pygame.transform.scale(frame5, (size, size))
        self.frames = [frame1, frame2, frame3, frame4, frame5]
        self.frame_offset = fps / 30

    """Returns the given frame of the explosion.
    
    :param effect: Effect to grab frame and other information from
    :type effect: Effect
    :returns: Frame to show
    :rtype: pygame image
    """
    def get_frame(self, effect):
        result = self.frames[int(effect.curr_frame // self.frame_offset)]
        effect.curr_frame += 1
        return result
