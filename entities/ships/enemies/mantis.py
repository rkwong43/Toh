from src.entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from src.utils import config

from src.utils.ids.enemy_id import EnemyID

"""Represents a Mantis enemy fighter. Fires a burst of bullets."""


class Mantis(BurstFireEnemy):
    """Constructor to make the enemy.

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

    def __init__(self, hp, shield, x, y, speed, fire_rate, **args):
        super().__init__(EnemyID.MANTIS, hp, shield, x, y, speed, config.ship_size, fire_rate, 5)

    """Moves the Mantis to its predetermined location. Will also reload its gun. Overrides move() in Enemy.
    """

    def move(self):
        self.reload()
        super().move()
