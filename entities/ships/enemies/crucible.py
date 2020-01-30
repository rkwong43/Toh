
from src.entities.ships.enemies.enemy import Enemy
from src.utils.entity_id import EntityID

"""Represents a Crucible enemy fighter."""


class Crucible(Enemy):
    """Constructor to make the Crucible ship

    :param ship_size: size the Crucible should be
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
    :param fps: Frames per second
    :type fps: int
    """

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, fps):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, True, fps, EntityID.CRUCIBLE)
        # fire rate in seconds
        self.fire_rate = int(fire_rate // 2.5)
        self.projectile_type = EntityID.ENEMY_BULLET
        self.fire_variance = 20

    def fire(self, target, projectiles):
        # Crucible ships fire twice
        temp = self.fire_variance
        super().fire(target, projectiles)
        self.fire_variance = 0
        super().fire(target, projectiles)
        self.fire_variance = temp
