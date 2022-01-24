from entities.ships.enemies.enemy import Enemy
from entities.ships.waypoint import Waypoint
from utils import config

""""Represents an enemy deity.
"""


class Deity(Enemy):
    def __init__(self, entity_id, hp, fire_rate):
        final_x = (config.display_width / 2) - config.ship_size * 4
        super().__init__(entity_id, hp, 0, final_x, -config.display_height, fire_rate=fire_rate * 4,
                         ship_size=config.ship_size * 8)
        self.remove_if_offscreen = False
        self.set_waypoint(wp=Waypoint((config.display_width / 2) - config.ship_size * 4, 0))
        # TODO: Keep track of previous state and not use it
