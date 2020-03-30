
"""Represents a generic ship.
"""
from src.utils import config


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
