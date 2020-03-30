from src.entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from src.utils import config

from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Despoiler enemy fighter."""


class Despoiler(BurstFireEnemy):
    """Constructor to make the Despoiler ship

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
        super().__init__(EnemyID.DESPOILER, hp, shield, x, y, speed, int(2 * config.ship_size), fire_rate, 8)
        self.projectile_type = ProjectileID.ENEMY_MISSILE
        self.fire_variance = 10
        self._reload_speed = fire_rate * 2
        self._reload_curr = fire_rate * 2

    """Added the ability to reload the burst every time it moves. Overrides move() in Enemy"""

    def move(self):
        self.reload()
        super().move()

