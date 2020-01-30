from enum import Enum, auto

"""Directions or commands to give the player and model.
"""


class Direction(Enum):
    # Movement
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    # Firing
    FIRE = auto()
