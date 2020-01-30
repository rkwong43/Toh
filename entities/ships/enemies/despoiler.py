from src.entities.ships.enemies.enemy import Enemy
from src.utils.entity_id import EntityID

"""Represents a Despoiler enemy fighter."""


class Despoiler(Enemy):
    """Constructor to make the Despoiler ship

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

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, fps):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, True, fps, EntityID.DESPOILER)
        # fire rate in seconds
        self.fire_rate = 1 * (fps // 30)
        self.projectile_type = EntityID.ENEMY_MISSILE
        self.fire_variance = 10

        # Fires a burst
        self.burst_max = 8 * (fps // 30)
        self.burst_curr = self.burst_max
        self.reload_speed = fire_rate * 2
        self.reload_curr = fire_rate * 2

    """Added the ability to reload the burst every time it moves."""

    def move(self):
        super().move()
        self.reload()

    """Reloads the burst weapon.
    """

    def reload(self):
        self.burst_curr -= 1
        if self.burst_curr <= 0:
            self.ready_to_fire = False
            self.reload_curr -= 1

        if self.reload_curr <= 0:
            self.reload_curr = self.reload_speed
            self.burst_curr = self.burst_max
            self.ready_to_fire = True
