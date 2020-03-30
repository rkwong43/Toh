from src.entities.ships.enemies.enemy import Enemy
from src.utils.ids.enemy_id import EnemyID

"""Represents a Seer enemy fighter."""


class Seer(Enemy):
    """Constructor to make the Seer ship

    :param ship_size: size the ship should be
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
    """

    def __init__(self, hp, shield, x, y, speed, ship_size, fire_rate, *args):
        super().__init__(EnemyID.SEER, hp, shield, x, y, speed, ship_size, fire_rate)
        # fire rate in seconds
        self.fire_rate = fire_rate * 2
