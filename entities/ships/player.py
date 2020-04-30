from src.utils import config
from src.utils.direction import Direction
from src.entities.ships.ship import Ship

"""Represents the player ship that moves"""


class Player(Ship):
    """Constructor to make the player ship

    :param x: starting x coordinate of player
    :type x: int
    :param y: starting y coordinate of player
    :type y: int
    :param entity_id: ID of images to use!
    :type entity_id: EntityID
    """

    def __init__(self, x, y, hp, shield, entity_id, speed):
        super().__init__(x, y, speed, hp, shield, config.ship_size)
        self.max_hp = hp
        self.entity_id = entity_id
        # Current score/experience
        self.score = 0
        self.angle = 90
        self.damage_taken = 0
        self.hits_taken = 0
        self.shield_recharge_rate *= 2

    """Moves the player ship depending on the direction
    
    :param direction: enum direction of which the player should be moved (up, down, left, right)
    :type direction: Direction
    """

    def move_player(self, direction):
        y_delta = 0
        if direction == Direction.UP:
            y_delta -= self.speed
        elif direction == Direction.DOWN:
            y_delta += self.speed
        x_delta = 0
        if direction == Direction.LEFT:
            x_delta -= self.speed
        elif direction == Direction.RIGHT:
            x_delta += self.speed
        self.x += x_delta
        self.y += y_delta
        for effect in self.ship_effects:
            effect.x += x_delta
            effect.y += y_delta

    """Damages and records how much damage taken and keeps count of the hits taken.
    """

    def damage(self, damage):
        super().damage(damage)
        self.damage_taken += damage
        self.hits_taken += 1
