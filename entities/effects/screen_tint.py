from entities.effects.effect import Effect
from utils import config

"""Represents some sort of effect that persists for a standard amount of time in the game.
"""


class ScreenTint(Effect):
    """Constructor to make the Effect.

    :param x: x coordinate of effect
    :type x: int
    :param y: y coordinate of effect
    :type y: int
    :param entity_id: ID representing what effect it is
    :type entity_id: EntityID
    """

    def __init__(self, x, y, entity_id):
        super().__init__(x, y, entity_id)
        # Number of frames it lasts
        self.max_frame = 4 * int(config.game_fps / 30)
