from enum import Enum, auto

"""Represents the IDs of different weapon types.
"""


class WeaponID(Enum):
    # Weapon types
    GUN = auto()
    SHOTGUN = auto()
    MACHINE_GUN = auto()
    FLAK_GUN = auto()
    MISSILE_LAUNCHER = auto()
    FLAK_CANNON = auto()
    DIAMOND_DUST = auto()
    MULTI_MISSILE = auto()
    STRIKER = auto()
    # Rapid fire missiles
    SWARM = auto()
    # Fires a huge spread of flak that slow down the further they move
    CONSTELLATION = auto()
    # Burst fire multiple volleys of homing bullets
    AURORA = auto()
    RAILGUN = auto()
