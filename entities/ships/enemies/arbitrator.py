from entities.ships.enemies.enemy import Enemy
from utils import config
from utils.ids.enemy_id import EnemyID
from utils.ids.projectile_id import ProjectileID

"""Represents a Arbitrator enemy fighter."""


class Arbitrator(Enemy):
    """Constructor to make the Arbitrator ship

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
        super().__init__(EnemyID.ARBITRATOR, hp, shield, x, y, speed, int(1.5 * config.ship_size), fire_rate)
        self.fire_variance = 20

    """Arbitrator fires multiple bullets and multiple missiles at the target.
    
    :param target: Target to fire at.
    :type target: Ship
    :param projectiles: Projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
        temp = self.fire_variance
        # Fires 3 bullets
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        self.fire_variance = 0
        super().fire(target, projectiles)
        # Fires 2 missiles
        self.projectile_type = ProjectileID.ENEMY_MISSILE
        self.projectile_damage = 20
        super().fire(target, projectiles)
        self.fire_variance = temp
        super().fire(target, projectiles)
        self.projectile_type = ProjectileID.ENEMY_BULLET
        self.projectile_damage = 10
