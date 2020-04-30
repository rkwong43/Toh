from enum import Enum, auto

"""Represents the IDs of different effects in-game.
"""


class EffectID(Enum):
    # Effects
    EXPLOSION = auto()
    TITAN_EXPLOSION = auto()
    RED_EXPLOSION = auto()
    BLUE_EXPLOSION = auto()
    POPUP = auto()
    RED_CHARGE = auto()
    BLUE_CHARGE = auto()
    # Screen effects
    SHIELD_TINT = auto()
    HP_TINT = auto()
