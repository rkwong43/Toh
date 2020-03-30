
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
    :param speed: speed it moves towards the ending position
    :type speed: int
    :param fire_rate: fire rate of the enemy
    :type fire_rate: int
    :param shield: shield health
    :type shield: int
    :param entity_id: ID of enemy
    :type entity_id: EntityID
    :param: bursts: number of projectiles fired per burst
    :type bursts: int
    """

    def __init__(self, entity_id, hp, shield, x, y, speed, ship_size, fire_rate, bursts):
        super().__init__(entity_id, hp, shield, x, y, speed, ship_size, fire_rate)
        # fire rate in frames
        # Mantis has different fire rate mechanics
        # Fire rate affects an internal burst counter to determine
        # when to fire a burst
        self.fire_rate = 1 * (config.game_fps // 30)

        # Fires a burst
        self._burst_max = bursts * (config.game_fps // 30)
        self._burst_curr = self._burst_max
        self._reload_speed = fire_rate
        self._reload_curr = fire_rate

    """Reloads the burst weapon.
    """

    def reload(self):
        self._burst_curr -= 1
        if self._burst_curr <= 0:
            self.ready_to_fire = False
            self._reload_curr -= 1

        if self._reload_curr <= 0:
            self._reload_curr = self._reload_speed
            self._burst_curr = self._burst_max
            self.ready_to_fire = True
