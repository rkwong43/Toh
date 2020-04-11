from src.entities.ships.allies.ally import Ally
from src.utils.ids.player_id import PlayerID
from src.utils.ids.projectile_id import ProjectileID

"""A friendly Aegis ship.
"""


class Aegis(Ally):
    """Constructs the citadel.
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, *args, **kwargs):
        super().__init__(hp, shield, x, y, speed, fire_rate)
        self.projectile_type = ProjectileID.FRIENDLY_BULLET
        self.entity_id = PlayerID.AEGIS
