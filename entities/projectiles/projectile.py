"""A basic projectile, can be extended into different types such as bullets or missiles.
"""
from utils import config


class Projectile:
    """Initializes the projectile.

    :param speed: speed of the projectile
    :type speed: int
    :param x: starting x location
    :type x: int
    :param y: starting y location
    :type y: int
    :param damage: the damage it inflicts
    :type damage: int
    """

    def __init__(self, speed, x, y, damage, entity_id):
        self.speed = speed
        self.x = x
        self.y = y
        self.damage = damage
        self.entity_id = entity_id
        self.has_splash = False
        self.air_burst = False
        self.size = config.ship_size
        self.target_destroyed = False
        self.remove_if_offscreen = True

    """Moves the projectile, to be done in child classes
    """

    def move(self):
        pass
