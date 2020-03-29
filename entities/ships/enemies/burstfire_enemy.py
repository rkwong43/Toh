
from src.entities.ships.enemies.enemy import Enemy
from src.utils import config

"""Represents an enemy ship that fires in bursts."""


class BurstFireEnemy(Enemy):
    """Constructor to make the enemy.

    :param ship_size: size the ship is
    :type ship_size: int
    :param x: starting x coordinate of ship
    :type x: int
    :param y: starting y coordinate of ship
    :type y: int
    :param hp: hit points of ship
    :type hp: int
    :param end_x: ending x position
    :type end_x: int
    :param end_y: ending y position
    :type end_y: int
    :param speed: speed it moves towards the ending position
    :type speed: int
    :param fire_rate: fire rate of the enemy
    :type fire_rate: int
    :param shield: shield health
    :type shield: int
    :param move_again: determines if it continuously moves
    :type move_again: bool
    :param entity_id: ID of enemy
    :type entity_id: EntityID
    :param: bursts: number of projectiles fired per burst
    :type bursts: int
    """

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, move_again, entity_id, bursts):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, move_again, entity_id)
        # fire rate in frames
        # Mantis has different fire rate mechanics
        # Fire rate affects an internal burst counter to determine
        # when to fire a burst
        self.fire_rate = 1 * (config.game_fps // 30)

        # Fires a burst
        self.burst_max = bursts * (config.game_fps // 30)
        self.burst_curr = self.burst_max
        self.reload_speed = fire_rate
        self.reload_curr = fire_rate

    """Reloads the burst weapon.
    """

    def reload(self):
        self.burst_curr -= 1
        if self.burst_curr <= 0:
            self.ready_to_fire = False
            self.reload_curr -= 1

        if self.reload_curr <= 0:
            self.reload_curr = self.reload_speed
            self.burst_curr = self.burst_max
            self.ready_to_fire = True
