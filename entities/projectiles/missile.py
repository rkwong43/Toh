import math

from src.entities.projectiles.projectile import Projectile
from src.utils import config
from src.utils.ids.projectile_id import ProjectileID

"""A missile that moves down/up at a constant rate but tracks the closest target in the x-position."""


class Missile(Projectile):
    """Constructor that initializes the missile.

    :param direction: angle the bullet should be going
    :type direction: int
    :param target: target to follow
    :type target: Ship
    """

    def __init__(self, speed, x, y, direction, damage, entity_id, target):
        super().__init__(speed, x, y, damage, entity_id)
        self.direction = direction
        # -1 if going up, 1 if going down
        self.orientation = 1 if self.direction >= 0 else -1
        self.target = target
        # How many ticks does the missile have to prep before tracking
        self.ticks = int(4 * (config.game_fps / 30))
        # Initial direction when fired
        self.y_change = -math.sin(math.radians(direction)) * speed
        self.x_change = math.cos(math.radians(direction)) * speed
        self.target_destroyed = False
        if self.entity_id == ProjectileID.FRIENDLY_BULLET:
            self.has_splash = False
        else:
            self.has_splash = True

    """Moves the missile depending on where the enemy is.
    """

    def move(self):
        # Has a prepping distance before tracking
        if self.ticks > 0:
            self.x += self.x_change
            self.y += self.y_change
            self.ticks -= 1
        else:
            self.seek_target()

    """Alters the direction it is facing to align with a path onto the target.
    """
    def seek_target(self):
        # No target
        if self.target == 0:
            # Continues moving in the direction it is initially going
            self.x += self.x_change
            self.y += self.y_change
            self.target_destroyed = True
        elif self.target.is_dead:
            # Target is dead
            # Continues moving along its current angle
            self.move_along_angle()
            self.target_destroyed = True
        else:
            # Target is alive
            self.target_destroyed = False
            target_center = (self.target.x, self.target.y)
            # 100 is the base ship size
            if self.target.size > config.ship_size:
                target_center = (self.target.x + ((self.target.size - config.ship_size) // 2),
                                 self.target.y + ((self.target.size - config.ship_size) // 2))
            angle = int(-math.degrees(math.atan2(self.y - target_center[1], self.x - target_center[0])))
            self.adjust_angle(angle)
            self.move_along_angle()

    """Gives the missile a new target.
    
    :param target: new target to track
    :type target: Ship
    """
    def acquire_target(self, target):
        if target != 0:
            self.target = target
            self.target_destroyed = False

    """Moves the missile based on its orientation.
    """

    def move_along_angle(self):
        angle_in_radians = math.radians(self.direction)
        x_dist = math.cos(angle_in_radians) * self.speed
        y_dist = -math.sin(angle_in_radians) * self.speed
        self.x += x_dist
        self.y += y_dist

    """Adjusts the angle slowly to the given angle.
    
    :param target_angle: Given angle to adjust to
    :type target_angle: int
    """

    def adjust_angle(self, target_angle):
        # Which y direction the missile was initially fired
        # Only tracks targets that are in front of the missile.
        # Up (-y)
        going_up = self.orientation == 1 and self.y > self.target.y
        # Down (+y)
        going_down = self.orientation == -1 and self.y < self.target.y
        # Missile goes in straight line if past the target
        if going_down or going_up:
            # Looks for which direction to go on the unit circle (clockwise or counterclockwise)
            difference = abs(target_angle - self.direction)
            complement_difference = 360 - abs(difference)
            if not (-self.speed < difference < self.speed):
                delta = int(-self.speed / 4) * self.orientation if difference < complement_difference \
                    else int(self.speed / 4) * self.orientation
                self.direction -= delta



