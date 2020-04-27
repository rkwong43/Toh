from enum import Enum, auto

"""Represents the IDs of different projectiles.
"""


class ProjectileID(Enum):
    # Projectiles
    FRIENDLY_BULLET = auto()
    ENEMY_BULLET = auto()
    FRIENDLY_FLAK = auto()
    ENEMY_FLAK = auto()
    FRIENDLY_MISSILE = auto()
    ENEMY_MISSILE = auto()
    DIAMOND_DUST = auto()
    RAILGUN_BLAST = auto()
    PULSE = auto()
    HOMING_BULLET = auto()

