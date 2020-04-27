from enum import Enum, auto

"""Represents the IDs of different player ships.
"""


class PlayerID(Enum):
    # Player:
    # Base:
    CITADEL = auto()
    # More HP and Shield, slower movement
    AEGIS = auto()
    # Less HP, faster
    GHOST = auto()
    # Slower ship, more damage
    ARCHANGEL = auto()
    # Faster ship, less shield, faster fire rate
    STORM = auto()
    # New generation:
    JUDGMENT = auto()

    # From killing deities:
    # WRATH
    # TODO: Remake
    ETERNITY = auto()
    ORIGIN = auto()
