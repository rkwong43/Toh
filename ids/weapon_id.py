from enum import Enum, auto

"""Represents the IDs of different weapon types.
"""


class WeaponID(Enum):
    # Weapon types
    GUN = auto()
    MACHINE_GUN = auto()
    FLAK_GUN = auto()
    FLAK_CANNON = auto()
    SHOTGUN = auto()
    MISSILE_LAUNCHER = auto()
    MULTI_MISSILE = auto()
    BAD_MISSILE_LAUNCHER = auto()
    RAILGUN = auto()
    STRIKER = auto()
