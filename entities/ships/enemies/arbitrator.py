from src.entities.ships.enemies.enemy import Enemy
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Arbitrator enemy fighter."""


class Arbitrator(Enemy):
    """Constructor to make the Arbitrator ship

    :param ship_size: size the ship should be
    :type ship_size: int
    :param x: starting x coordinate of ship
    :type x: int
    :param y: starting y coordinate of ship
    :type y: int
    :param hp: hit points of ship
    :type hp: int
    :param end_x: ending x position
    :type end_x: int
    :param end_y: ending y position
    :type end_y: int
    :param speed: speed it moves towards the ending position
    :type speed: int
    :param fire_rate: fire rate of the enemy
    :type fire_rate: int
    :param shield: shield health
    :type shield: int
    """

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, True, EnemyID.ARBITRATOR)
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
