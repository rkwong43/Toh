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

    """Moves the player ship depending on the direction
    
    :param direction: enum direction of which the player should be moved (up, down, left, right)
    :type direction: Direction
    """

    def move_player(self, direction):
        if direction == Direction.UP:
            self.y -= self.speed
        elif direction == Direction.DOWN:
            self.y += self.speed

        if direction == Direction.LEFT:
            self.x -= self.speed
        elif direction == Direction.RIGHT:
            self.x += self.speed

    """Damages and records how much damage taken and keeps count of the hits taken.
    """

    def damage(self, damage):
        super().damage(damage)
        self.damage_taken += damage
        self.hits_taken += 1
