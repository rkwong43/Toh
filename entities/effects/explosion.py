from src.entities.effects.effect import Effect
from src.utils import config

"""Represents an explosion. Is 4 frames in length"""


class Explosion(Effect):

    """Constructor to make the explosion.

    :param x: center x coordinate of explosion
    :type x: int
    :param y: center y coordinate of explosion
    :type y: int
    :param entity_id: ID representing what effect it is
    :type entity_id: EntityID
    """

    def __init__(self, x, y, entity_id):
        super().__init__(x - config.ship_size * .75, y - config.ship_size * .75, entity_id)
        # Explosions have 5 frames of animation
        self.max_frame = 5 * int(config.game_fps / 30) - 1


