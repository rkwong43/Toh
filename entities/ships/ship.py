import math
import random

import pygame

from src.utils import config

# Constants for state of movement and rotations
NO_WAYPOINT = 1
MOVE_WAYPOINT = 2
FIRE_WAYPOINT = 3
MOVE_AND_FIRE_WAYPOINT = 4

"""Represents a generic ship.
"""


class Ship:
    random.seed()
    """Constructor to make the ship.

    :param x: starting x coordinate of ship
    :type x: int
    :param y: starting y coordinate of ship
    :type y: int
    :param hp: hit points of the ship
    :type hp: int
    :param shield: shield points of the ship
    :type shield: int
    :param size: size of ship
    :type size: int
    """

    def __init__(self, x, y, speed, hp, shield, size):
        # Speed, constant along an angle (vector)
        self.speed = speed * (30 / config.game_fps)
        # Position
        self.x = int(x)
        self.y = int(y)
        self.end_x = 0
        self.end_y = 0
        # Size of the ship (not scaling, should be a value in pixels)
        self.size = size
        self.angle = -90
        #############################################
        # Health
        self.hp = hp
        self.max_hp = hp
        #############################################
        # Shield
        self.shield = shield
        # Maximum shield
        self.max_shield = shield
        # Shield recharge rate
        self.shield_recharge_rate = (self.max_shield // 20) / config.game_fps
        self.shield_recharge_rate = 1 if self.shield_recharge_rate == 0 else self.shield_recharge_rate
        # Delay before shield recharges
        self.shield_delay = config.game_fps * 2
        # Keeps count of when to regenerate
        self.shield_recharge = self.shield_delay
        #############################################
        # Status indicators
        # is_damaged is used for telling when the shop
        self.is_damaged = False
        self.is_dead = False

        # Current waypoint
        self.waypoint = None
        self._wp_state = NO_WAYPOINT

        # Rotation states
        self._wp_rotations = {NO_WAYPOINT: self._rotate,
                              MOVE_WAYPOINT: self._rotate,
                              FIRE_WAYPOINT: self._rotate_to_wp,
                              MOVE_AND_FIRE_WAYPOINT: self._rotate_to_wp
                              }
        # Movement states
        self._wp_movement = {NO_WAYPOINT: self._move,
                             MOVE_WAYPOINT: self._move_to_wp,
                             FIRE_WAYPOINT: self._move,
                             MOVE_AND_FIRE_WAYPOINT: self._move_to_wp
                             }
        # If it should be removed when offscreen
        self.remove_if_offscreen = True
        # If in a form of stealth
        self.stealth = False
        self.rotation_speed = 3 * (60 / config.game_fps)

    """Represents the angle the ship is facing.

    :param target: target the ship is facing
    :type target: Ship or Waypoint
    """

    def _rotate(self, target):
        # Rotates the ship to face the target ship
        # Adjustment for larger ships
        if target.size > 2 * config.ship_size:
            y = target.y + target.size / 2
            x = target.x + target.size / 2
        else:
            y = target.y
            x = target.x
        y_dist = self.y - y
        x_dist = self.x - x
        target_angle = -int(math.degrees(math.atan2(y_dist, x_dist))) - 90
        if abs(self.angle - target_angle) > self.rotation_speed:
            v1 = pygame.math.Vector2()
            v1.from_polar((1, self.angle))
            v2 = pygame.math.Vector2()
            v2.from_polar((1, target_angle))
            angle_change = -self.rotation_speed if v1.angle_to(v2) < 0 else self.rotation_speed
            self.angle += angle_change

    """Rotates the ship depending on its current state.
    
    :param target: target the ship is facing
    :type target: Ship or Waypoint
    """

    def rotate(self, target):
        if target is not None:
            self._wp_rotations[self._wp_state](target)

    """Rotates the ship towards its waypoint.
    """

    def _rotate_to_wp(self, *args):
        self.angle = -math.degrees(math.atan2(self.y - self.waypoint.y, self.x - self.waypoint.x)) - 90

    """Lowers the health of the ship and switches states to a damaged one.
    
    :param damage: damage taken from the collision
    :type damage: int
    """

    def damage(self, damage):
        self.is_damaged = True
        # Intended mechanic, any amount of shield will block a huge chunk of damage
        # that will exceed the current shield value
        if self.shield > 0:
            self.shield -= damage
            self.shield_recharge = 0
        else:
            self.hp -= damage
        # Indicating that the ship is destroyed
        if self.hp <= 0:
            self.is_dead = True

    """Recharges the shield of the ship.
    """

    def recharge_shield(self):
        # Delay to recharge shield
        if self.shield_recharge < self.shield_delay:
            self.shield_recharge += 1
        # Increases shield gradually until it hits the limit
        elif self.shield < self.max_shield:
            self.shield += self.shield_recharge_rate
            # Makes sure it caps to account for rounding errors
            if self.shield > self.max_shield:
                self.shield = self.max_shield

    """Sets the ship's waypoint.
    
    :param wp: waypoint to travel to
    :type wp: Waypoint
    :param fire_at: if the ship will fire at the waypoint rather than the player
    :type fire_at: bool
    :param move_to: if the ship moves towards the waypoint
    :type move_to: bool
    """

    def set_waypoint(self, wp=None, fire_at=False, move_to=True):
        if wp is not None:
            self.waypoint = wp
        if fire_at and not move_to:
            self._wp_state = FIRE_WAYPOINT
        elif not fire_at and move_to:
            self._wp_state = MOVE_WAYPOINT
        elif fire_at and move_to:
            self._wp_state = MOVE_AND_FIRE_WAYPOINT
        else:
            self._wp_state = NO_WAYPOINT

    """Moves the ship.
    """

    def move(self):
        self._wp_movement[self._wp_state]()

    """Moves the ship randomly to a generated position on the screen.
    """

    def _move(self):
        if self.speed > 0:
            x_done = False
            if self.x < self.end_x - self.speed:
                self.x += self.speed
            elif self.x > self.end_x + self.speed:
                self.x -= self.speed
            else:
                x_done = True

            if self.y < self.end_y - self.speed:
                self.y += self.speed
            elif self.y > self.end_y + self.speed:
                self.y -= self.speed
            elif x_done:
                self.end_x, self.end_y = self._generate_pos()

    """Moves the ship towards its waypoint.
    """

    def _move_to_wp(self):
        if self.speed > 0:
            if self.x < self.waypoint.x - self.speed:
                self.x += self.speed
            elif self.x > self.waypoint.x + self.speed:
                self.x -= self.speed

            if self.y < self.waypoint.y - self.speed:
                self.y += self.speed
            elif self.y > self.waypoint.y + self.speed:
                self.y -= self.speed

    """Generates a new position to move into. 

    :returns: tuple of x and y pos
    :rtype: (int, int)
    """

    def _generate_pos(self):
        x = random.randint(config.ship_size, config.display_width - (2 * config.ship_size))
        y = random.randint(0, config.display_height - config.ship_size)
        return x, y

    """Spins the ship in circles.
    """

    def _spin(self, target):
        self.angle += self.rotation_speed
        if self.angle > 360:
            self.angle -= 360

    """Does nothing unless it specifically has a command for being offscreen.
    """

    def offscreen(self):
        pass
