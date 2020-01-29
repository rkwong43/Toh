import math

from src.entities.projectiles.projectile import Projectile

"""A missile that moves down/up at a constant rate but tracks the closest target in the x-position."""


class Missile(Projectile):
    """Constructor that initializes the missile.

    :param direction: angle the bullet should be going
    :type direction: int
    :param target: target to follow
    :type target: Ship
    """

    def __init__(self, speed, x, y, direction, damage, size, entity_id, target):
        super().__init__(speed, x, y, damage, size, entity_id)
        self.direction = direction
        # -1 if going up, 1 if going down
        self.orientation = 1
        if self.direction < 0:
            self.orientation = -1
        self.has_splash = True
        self.target = target
        self.size = size
        # How many ticks does the missile have to prep before tracking
        self.ticks = 4
        self.y_change = -math.sin(math.radians(direction)) * speed
        self.x_change = math.cos(math.radians(direction)) * speed
        self.target_destroyed = False

    """Moves the missile depending on where the enemy is.
    """

    def move(self):
        # Has a prepping distance before tracking
        if self.ticks > 0:
            self.x += self.x_change
            self.y += self.y_change
            self.ticks -= 1
        else:
            # No target
            if self.target == 0:
                self.x += self.x_change
                self.y += self.y_change
                self.target_destroyed = True
            elif self.target.dead:
                # Target is dead
                self.move_along_angle()
                self.target_destroyed = True
            else:
                # Target is alive
                target_center = (self.target.x, self.target.y)
                if self.target.size > 100:
                    target_center = (self.target.x + + ((self.target.size - 100) // 2),
                                     self.target.y + ((self.target.size - 100) // 2))
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
        # Up (-y)
        going_up = self.orientation == 1 and self.y > self.target.y
        # Down (+y)
        going_down = self.orientation == -1 and self.y < self.target.y
        # Missile goes in straight line if past the target
        if going_down or going_up:
            curr_angle = self.direction
            # Converts both to range [0, 360)
            if curr_angle < 0:
                curr_angle += 360
            if target_angle < 0:
                target_angle += 360
            difference = abs(target_angle - curr_angle)
            complement_difference = 360 - abs(difference)
            if not (-self.speed < difference < self.speed):
                delta = 0
                if difference < complement_difference:
                    delta = int(-self.speed / 4) * self.orientation
                elif difference > complement_difference:
                    delta = int(self.speed / 4) * self.orientation
                curr_angle += delta
                # Converts back to range (-180, 180)
                if curr_angle < 0:
                    curr_angle += 360
                elif curr_angle > 360:
                    curr_angle -= 360
                if curr_angle > 180:
                    self.direction = curr_angle - 360
                else:
                    self.direction = curr_angle



