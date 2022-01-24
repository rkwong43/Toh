import math

from entities.ships.allies.ally import Ally
from utils import config
from utils.ids.ally_id import AllyID
from utils.ids.projectile_id import ProjectileID

"""A friendly Archer turret.
"""


class Archer(Ally):
    """Constructs the Archer.
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, *args, **kwargs):
        super().__init__(hp, shield, x, y, speed, fire_rate)
        self.projectile_type = ProjectileID.FRIENDLY_BULLET
        self.entity_id = AllyID.ARCHER
        self.fire_rate = fire_rate // 2
        self.projectile_damage = 5
        self.fire_variance = 3
        self.projectile_speed = 20 * (30 / config.game_fps)

    """Fires in a spread. Overrides Ally fire.
    """
    def fire(self, target, projectiles):
        # Fires twice
        super().fire(target, projectiles)
        super().fire(target, projectiles)
