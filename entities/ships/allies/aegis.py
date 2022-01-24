from entities.ships.allies.ally import Ally
from utils.ids.player_id import PlayerID
from utils.ids.projectile_id import ProjectileID

"""A friendly Aegis ship.
"""


class Aegis(Ally):
    """Constructs the Aegis.
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, *args, **kwargs):
        super().__init__(hp, shield, x, y, speed, fire_rate)
        self.projectile_type = ProjectileID.FRIENDLY_MISSILE
        self.projectile_damage = 20
        self.entity_id = PlayerID.AEGIS
