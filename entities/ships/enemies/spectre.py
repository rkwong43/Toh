from src.entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from src.utils import config

from src.utils.ids.enemy_id import EnemyID

"""Represents a Spectre enemy fighter. Fires a burst of bullets."""


class Spectre(BurstFireEnemy):
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
        super().__init__(EnemyID.SPECTRE, hp, shield, x, y, speed, config.ship_size, fire_rate * 3, 12)
        self.fire_variance = 2
        self.stealth = True

    """Fires a burst of bullets.
    """
    def fire(self, target, projectiles):
        super().fire(target, projectiles)
        self.is_damaged = True
        self.stealth = False

    """Stealth as it moves.
    """
    def move(self):
        self.stealth = True
        super().move()
