
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
    :param fps: frames per second
    :type fps: int
    """

    def __init__(self, x, y, hp, shield, size, fps):
        self.speed = 0
        self.x = int(x)
        self.y = int(y)
        self.hp = hp
        self.max_hp = hp
        self.size = size
        self.isDamaged = False
        self.dead = False
        self.shield = shield
        # Maximum shield
        self.max_shield = shield
        self.shield_recharge_rate = (self.max_shield // 20) / fps
        self.shield_recharge_rate = 1 if self.shield_recharge_rate == 0 else self.shield_recharge_rate
        # Delay before shield recharges
        self.shield_delay = fps
        # Keeps count of when to regenerate
        self.shield_recharge = self.shield_delay

    """Lowers the health of the ship and switches states to a damaged one.
    
    :param damage: damage taken from the collision
    :type damage: int
    """
    def damage(self, damage):
        self.isDamaged = True
        # Intended mechanic, any amount of shield will block a huge chunk of damage
        # that will exceed the current shield value
        if self.shield > 0:
            self.shield -= damage
            self.shield_recharge = 0
        else:
            self.hp -= damage
        if self.hp <= 0:
            self.dead = True

    """Recharges the shield of the ship.
    """
    def recharge_shield(self):
        if not self.dead:
            # Delay to recharge shield
            if self.shield_recharge < self.shield_delay:
                self.shield_recharge += 1
            # Increases shield gradually until it hits the limit
            elif self.shield < self.max_shield:
                self.shield += self.shield_recharge_rate
                if self.shield > self.max_shield:
                    self.shield = self.max_shield
