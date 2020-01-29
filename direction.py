from enum import Enum

"""Directions or commands to give the player and model.
"""


class Direction(Enum):
    # Movement
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    # Firing
