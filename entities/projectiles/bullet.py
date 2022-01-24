import math

from entities.projectiles.projectile import Projectile
from utils.ids.projectile_id import ProjectileID

"""A bullet that travels in a straight line."""


class Bullet(Projectile):
    """Constructor that initializes the bullet.

    :param direction: angle the bullet should be going
    :type direction: int
    """

    def __init__(self, speed, x, y, direction, damage, entity_id):
        super().__init__(speed, x, y, damage, entity_id)
        self.direction = direction

        self.y_change = -math.sin(math.radians(direction)) * speed
        self.x_change = math.cos(math.radians(direction)) * speed
        if entity_id in [ProjectileID.ENEMY_FLAK, ProjectileID.FRIENDLY_FLAK, ProjectileID.RAILGUN_BLAST]:
            self.has_splash = True
            self.air_burst = True

    """Moves the bullet depending on what direction it is going
    """

    def move(self):
        self.y += self.y_change
        self.x += self.x_change
