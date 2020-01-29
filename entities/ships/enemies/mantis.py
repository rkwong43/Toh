from src.entities.ships.enemies.enemy import Enemy
from src.entity_id import EntityID

"""Represents a Mantis enemy fighter. Fires a burst of bullets."""


class Mantis(Enemy):
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
    :param move_again: determines if it continuously moves
    :type move_again: bool
    :param fps: Frames per second
    :type fps: int
    """

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, move_again, fps):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, move_again, fps, EntityID.MANTIS)
        # fire rate in frames
        # Mantis has different fire rate mechanics
        # Fire rate affects an internal burst counter to determine
        # when to fire a burst
        self.fire_rate = 1 * (fps // 30)
        self.projectile_type = EntityID.ENEMY_BULLET

        # Fires a burst
        self.burst_max = 5
        self.burst_curr = 5
        self.reload_speed = fire_rate
        self.reload_curr = fire_rate

    """Moves the Mantis to its predetermined location. Will also reload its gun.
    """

    def move(self):
        self.reload()
        # Only moves up and down until it has to move again
        if not self.move_again:
            if self.y < self.end_y - self.speed:
                self.y += self.speed
            elif self.y > self.end_y + self.speed:
                self.y -= self.speed
        else:
            super().move()

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
