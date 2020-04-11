import math

from src.utils import config

# Constants for state of movement and rotations
NO_WAYPOINT = 1
MOVE_WAYPOINT = 2
FIRE_WAYPOINT = 3
MOVE_AND_FIRE_WAYPOINT = 4

"""Represents a generic ship.
"""


class Ship:
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
        # Size of the ship (not scaling, should be a value in pixels)
        self.size = size
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
        self.shield_delay = config.game_fps
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

    """Represents the angle the ship is facing.

    :param target: target the ship is facing
    :type target: Ship or Waypoint
    """

    def _rotate(self, target):
        # Rotates the ship to face the target ship
        self.angle = -math.degrees(math.atan2(self.y - target.y, self.x - target.x)) - 90

    """Rotates the ship depending on its current state.
    
    :param target: target the ship is facing
    :type target: Ship or Waypoint
    """
    def rotate(self, target):
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
