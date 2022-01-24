"""Basically a 2D position in space. Meant to have as either targets or as locations to travel to.
"""
from utils import config


class Waypoint:
    """Constructs the waypoint.

    :param x: x pos
    :type x: int
    :param y: y pos
    :type y: int
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = config.ship_size
        self.is_dead = False
