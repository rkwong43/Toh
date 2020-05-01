
from src.entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from src.utils import config

from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Phantom enemy fighter. Fires pulses of energy."""


class Phantom(BurstFireEnemy):
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
        super().__init__(EnemyID.PHANTOM, hp, shield, x, y, speed, config.ship_size * 2, fire_rate * 4, 8,
                         burst_rate=4)
        self.stealth = True
        self.projectile_type = ProjectileID.PULSE
        self.effects = effects

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
