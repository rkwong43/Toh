from src.entities.effects.effect import Effect
from src.utils.entity_id import EntityID

"""Represents a text popup that lasts a certain amount of time in the game.
"""


class PopUp(Effect):
    """Constructor to make the Effect.

    :param text: what text to render
    :type text: str
    :param fps: Frames per second of the game
    :type fps: int
    :param seconds: seconds to display for
    :type seconds: int
    :param x: x coordinate to put the center at
    :type x: int
    :param y: y coordinate to put the center at
    :type y: int
    """

    def __init__(self, text, fps, seconds, x, y):
        super().__init__(x, y, EntityID.POPUP)
        # Where their intended center is
        self.center_x = x
        self.center_y = y
        self.curr_frame = 0
        # Number of frames it lasts
        self.max_frame = fps * seconds
        self.text = text
