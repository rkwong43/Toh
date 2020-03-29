from enum import Enum, auto

"""Represents the IDs of different player ships.
"""


class PlayerID(Enum):
    # Player:
    # More HP and Shield, slower movement
    AEGIS = auto()
    # Less HP, faster
    GHOST = auto()
    # Slower ship, more damage
    ARCHANGEL = auto()
    # Faster ship, less shield, faster fire rate
    STORM = auto()
    # less HP and shield, more fire rate and damage
    ORIGIN = auto()
    # Base:
    CITADEL = auto()