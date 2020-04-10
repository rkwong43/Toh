from enum import Enum, auto

"""Represents the IDs of game modes available to play. Made for the purpose of cleaner pulling of data for high scores.
"""


class GameModeID(Enum):
    # Game modes
    CLASSIC = auto()
    MANDIBLE_MADNESS = auto()
    HEAVEN = auto()
    # All out war - include enemies and allies
    # Assign each enemy a target
    # Add warships
    #ONSLAUGHT = auto()
    # Randomly generate weapons every few waves
    #FATE = auto()

    TITAN_SLAYER = auto()
