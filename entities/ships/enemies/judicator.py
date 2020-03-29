from src.entities.ships.enemies.terminus import Terminus
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Judicator enemy fighter."""


class Judicator(Terminus):
    """Constructor to make the Judicator ship

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
    :param fps: frames per second
    :type fps: int
    """

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, effects):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, effects)
        self.entity_id = EnemyID.JUDICATOR
        # fire rate in seconds
        self.fire_rate = int(fire_rate * 3)
        self.projectile_type = ProjectileID.RAILGUN_BLAST
        self.move_again = True

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
