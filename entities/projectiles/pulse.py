from src.entities.projectiles.projectile import Projectile
from src.utils import config
from src.utils.ids.projectile_id import ProjectileID

"""Represents a timed pulse of energy."""


class Pulse(Projectile):
    """Constructs the pulse projectile.

    :param speed: The speed at which the pulse forms in frames.
    :type speed: int
    :param x: top left x position
    :type x: int
    :param y: top left y position
    :type y: int
    :param damage: damage it deals when fully formed
    :type damage: int
    :param radius: radius of the pulse
    :type radius: int
    """

    def __init__(self, speed, x, y, damage, radius):
        super().__init__(speed, x, y, damage, ProjectileID.PULSE)
        self.speed = 0
        self.charge_time = speed
        self.curr_charge = 0
        self.size = radius * 2
        self.air_burst = True
        self.has_splash = True

    """Doesn't really move it, just accelerates the charge time.
    """
    def move(self):
        self.curr_charge += 1
        if self.curr_charge > self.charge_time:
            self.x = -config.display_width
            self.damage = 0
