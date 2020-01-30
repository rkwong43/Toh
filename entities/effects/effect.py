"""Represents some sort of effect that persists for a standard amount of time in the game.
"""


class Effect:
    """Constructor to make the Effect.

    :param x: x coordinate of effect
    :type x: int
    :param y: y coordinate of effect
    :type y: int
    :param entity_id: ID representing what effect it is
    :type entity_id: EntityID
    """

    def __init__(self, x, y, entity_id):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.curr_frame = 0
        # Number of frames it lasts
        self.max_frame = 0

    """Returns whether to animate the frame or not.
    
    :returns: whether to animate it or not
    :rtype: bool
    """

    def animate(self):
        return self.curr_frame < self.max_frame
