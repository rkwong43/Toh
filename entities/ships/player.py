from src.utils.direction import Direction
from src.entities.ships.ship import Ship

"""Represents the player ship that moves"""


class Player(Ship):

    """Constructor to make the player ship

    :param ship_size: size the image should be scaled to
    :type ship_size: int
    :param x: starting x coordinate of player
    :type x: int
    :param y: starting y coordinate of player
    :type y: int
    :param entity_id: ID of images to use!
    :type entity_id: EntityID
    :param fps: Frames per second
    :type fps: int
    """

    def __init__(self, ship_size, x, y, hp, shield, entity_id, fps, speed):
        super().__init__(x, y, hp, shield, ship_size, fps)
        self.max_hp = hp
        self.entity_id = entity_id
        self.speed = speed * (32 / fps)
        self.score = 0
        self.angle = 90

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
