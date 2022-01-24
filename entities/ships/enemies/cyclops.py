
from entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from utils import config

from utils.ids.enemy_id import EnemyID
from utils.ids.projectile_id import ProjectileID

"""Represents a Cyclops enemy fighter. Fires pulses of energy."""


class Cyclops(BurstFireEnemy):
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

    def __init__(self, hp, shield, x, y, speed, fire_rate, effects, **args):
        super().__init__(EnemyID.CYCLOPS, hp, shield, x, y, speed, config.ship_size * 3, fire_rate * 3, 8,
                         burst_rate=2)
        self.projectile_type = ProjectileID.PULSE
        self.effects = effects
        self.fire_variance = 2 * config.ship_size

    """Fires a bunch of pulse rounds.
    """

    def fire(self, target, projectiles):
        for _ in range(4):
            super().fire(target, projectiles)
