from enum import Enum, auto

"""Represents the IDs miscellaneous game modes and identities.
"""


class GameID(Enum):
    # Different ID's to generalize different types of entities
    WEAPON = auto()
    SHIP = auto()
    ENEMY = auto()

    TUTORIAL = auto()
    SURVIVAL = auto()
    HANGAR = auto()
    CHALLENGE = auto()

    # Unimplemented:
    STORY = auto()
    SETTINGS = auto()

    # Menu IDs
    GALLERY = auto()
    MENU = auto()
    SELECTOR = auto()
    LOADOUT = auto()
    RESULTS = auto()
