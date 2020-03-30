from src.entities.ships.enemies.enemy import Enemy
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Subjugator enemy fighter."""


class Subjugator(Enemy):
    """Constructor to make the enemy.

    :param ship_size: size the ship is
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

    def __init__(self, hp, shield, x, y, speed, ship_size, fire_rate, *args):
        super().__init__(EnemyID.SUBJUGATOR, hp, shield, x, y, speed, ship_size, fire_rate)
        self.projectile_type = ProjectileID.ENEMY_MISSILE

