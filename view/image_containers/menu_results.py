from utils.ids.game_id import GameID

"""Defines a score screen.
"""


class MenuResults:
    """Constructs the menu.

    :param stats: The statistics to display.
    :type stats: Dictionary
    """

    def __init__(self, stats):
        self.name = GameID.RESULTS
        self.stats = stats
