from enum import Enum, auto

"""Represents the IDs of game modes available to play. Made for the purpose of cleaner pulling of data for high scores.
"""


class GameModeID(Enum):
    # Game modes
    CLASSIC = auto()
    MANDIBLE_MADNESS = auto()
    HEAVEN = auto()
    TITAN_SLAYER = auto()
