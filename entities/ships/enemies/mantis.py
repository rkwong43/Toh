from src.entities.ships.enemies.burstfire_enemy import BurstFireEnemy

from src.utils.ids.enemy_id import EnemyID

"""Represents a Mantis enemy fighter. Fires a burst of bullets."""


class Mantis(BurstFireEnemy):
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
    """

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, move_again):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, move_again, EnemyID.MANTIS, 5)

    """Moves the Mantis to its predetermined location. Will also reload its gun. Overrides move() in Enemy.
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
