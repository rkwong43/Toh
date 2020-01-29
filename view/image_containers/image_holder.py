import pygame

"""Container to hold images for ships and projectiles
"""


class ImageHolder:
    """Constructor to define and load the images.

    :param images: list of image names
    :type images: List of str
    :param size: size to scale images to
    :type size: int
    """

    def __init__(self, images, size):
        self.base_image = pygame.image.load(images[0])
        self.base_image = pygame.transform.scale(self.base_image, (size, size))
        self.animated_image = pygame.image.load(images[1])
        self.animated_image = pygame.transform.scale(self.animated_image, (size, size))
        self.damaged_image = pygame.image.load(images[2])
        self.damaged_image = pygame.transform.scale(self.damaged_image, (size, size))
        self.shield_damage_image = pygame.image.load(images[3])
        self.shield_damage_image = pygame.transform.scale(self.shield_damage_image, (size, size))
