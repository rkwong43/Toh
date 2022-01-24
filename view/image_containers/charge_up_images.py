
from view.image_containers.explosion_images import ExplosionImages

"""Container to hold images for a charging effect.
"""


class ChargeUpImages(ExplosionImages):
    """Constructor to define and load the images.

    :param images: list of image names
    :type images: List of str
    :param size: size to scale images to
    :type size: int
    """

    def __init__(self, images, size):
        super().__init__(images, size)
        self.frames.reverse()
        self.frame_offset = self.frame_offset * 4
