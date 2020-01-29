import random

from src.entities.projectiles.projectile import Projectile

"""A really bad missile."""


class BadMissile(Projectile):
    """Constructor that initializes the missile.

    :param direction: angle the missile should be going
    :type direction: int
    :param target: target to follow
    :type target: Ship
    """

    def __init__(self, speed, x, y, direction, damage, size, entity_id, target):
        super().__init__(speed, x, y, damage, size, entity_id)
        self.direction = direction
        self.has_splash = True
        self.target = target
        self.size = size
        self.target_destroyed = False
        self.orientation = 1
        if self.direction > 0:
            self.orientation = -1

    """Gives the missile a new target.

        :param target: new target to track
        :type target: Ship
        """

    def acquire_target(self, target):
        if target != 0:
            self.target = target
            self.target_destroyed = False

    """Moves the missile depending on what direction it is going. Very random and unpredictable.
    """

    def move(self):
        random_speed = random.randint(1, 3 * self.speed)
        random_direction = random.randint(-180, 180)
        self.direction = random_direction
        random_x = random.randint(5 * -self.speed, 5 * self.speed)
        self.x += random_x
        self.y += random_speed * self.orientation
        if self.target != 0:
            if self.x < self.target.x:
                self.x += random_speed
            elif self.x > self.target.x:
                self.x -= random_speed
            if self.target.dead:
                self.target_destroyed = True
        else:
            self.target_destroyed = True
