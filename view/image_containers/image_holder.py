import pygame

"""Container to hold images for ships and projectiles
"""


class ImageHolder:
    """Constructor to define and load the images.

    :param images: The png spritesheet of the image
    :type images: str
    :param size: size to scale images to
    :type size: int
    """

    def __init__(self, images, size):
        # Sprite sheet consists of 4 sprites by default
        spritesheet = pygame.image.load(images).convert_alpha()
        width = spritesheet.get_width()
        # 4 sprites
        sprite_size = width // 4
        image_size = (sprite_size, sprite_size)
        sprites = []
        for i in range(4):
            offset = sprite_size * i
            sprites.append(
                pygame.transform.scale(spritesheet.subsurface(pygame.Rect((offset, 0), image_size)), (size, size)))
        self.base_image = sprites[0]
        self.animated_image = sprites[1]
        self.damaged_image = sprites[2]
        self.shield_damage_image = sprites[3]
