
from src.entities.ships.enemies.enemy import Enemy
from src.utils import config
from src.utils.ids.enemy_id import EnemyID

"""Represents a Crucible enemy fighter."""


class Crucible(Enemy):
    """Constructor to make the Crucible ship

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

    def __init__(self, hp, shield, x, y, speed, fire_rate, *args):
        super().__init__(EnemyID.CRUCIBLE, hp, shield, x, y, speed, config.ship_size, fire_rate)
        # fire rate in seconds
        self.fire_rate = int(fire_rate // 2.5)
        self.fire_variance = 20

    # Overrides fire() in enemy
    def fire(self, target, projectiles):
        # Crucible ships fire twice
        temp = self.fire_variance
        super().fire(target, projectiles)
        self.fire_variance = 0
        super().fire(target, projectiles)
        self.fire_variance = temp
