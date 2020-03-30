from src.entities.ships.enemies.terminus import Terminus
from src.utils import config
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Judicator enemy fighter."""


class Judicator(Terminus):
    """Constructor to make the Judicator ship

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
    :param effects: Effects to add onto when firing
    :type effects: List of Effect
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, effects, *args):
        super().__init__(hp, shield, x, y, speed, int(1.5 * config.ship_size), fire_rate, effects)
        self.entity_id = EnemyID.JUDICATOR
        # fire rate in seconds
        self.fire_rate = int(fire_rate * 3)
        self.projectile_type = ProjectileID.RAILGUN_BLAST

    """Judicator fires multiple bullets and a railgun blast at the enemy.

    :param target: Target to fire at.
    :type target: Ship
    :param projectiles: Projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
        super().fire(target, projectiles)
        self.projectile_type = ProjectileID.DIAMOND_DUST
        temp = self.projectile_speed
        self.projectile_speed = 10
        self.fire_variance = 15
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        self.fire_variance = 0
        self.projectile_speed = temp
        self.projectile_type = ProjectileID.RAILGUN_BLAST
