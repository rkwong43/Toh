from enum import Enum, auto

"""Represents the IDs miscellaneous game modes and identities.
"""


class GameID(Enum):
    # Different ID's to generalize different types of entities
    WEAPON = auto()
    SHIP = auto()
    # Difficulties
    EASY = auto()
    NORMAL = auto()
    HARD = auto()
    # Game modes
    SURVIVAL = auto()
    MANDIBLE_MADNESS = auto()
    TITAN_SLAYER = auto()
    HEAVEN = auto()
    TUTORIAL = auto()
    # Menu IDs
    GALLERY = auto()
