from src.model.stats import gamemode_stats
from src.utils.ids.game_id import GameID
from src.view.menu_tree import MenuTree

"""Defines a selection screen that branches off from either other selection screens or a menu tree.
Consists of a list of items to the left, with a description and other statistics to the right.
Difference from a MenuTree is that this only has a single option forward.
"""


class MenuSelector(MenuTree):
    """Constructs the menu selector.

    :param options: The options to display
    :type options: [ID]
    :param name: The type of category this is under
    :type name: GameID
    :param next_menu: The next screen to go to.
    :type next_menu: MenuSelector or LoadoutMenu or None
    """

    def __init__(self, options, name, next_menu):
        super().__init__(name)
        self.options = options
        self._next_menu = next_menu
        try:
            self._next_menu.root = self
        except AttributeError:
            self._next_menu = None
        self._number_of_options = len(options)
        self._init_descriptions()

    """Initializes the descriptions for the current screen.
        """

    def _init_descriptions(self):
        for key in self.options:
            try:
                self.description[key] = gamemode_stats.descriptions[key]
            except KeyError:
                self.description[key] = None

    """Selects the option and returns the option selected.
    
    :returns: tuple of option selected and the next selector
    :rtype: ID, MenuSelector or LoadoutMenu
    """

    def select(self):
        self._next_menu.root = self
        return self.options[self._current_selection], self._next_menu

    """Returns all the options listed.

    :returns: options to display
    :rtype: [str]
    """

    def get_options(self):
        return [item.name.replace("_", " ") for item in self.options]

    """Retrieves the current item's ID.

   :returns: ID of the current item
   :rtype: ID
   """

    def get_curr_id(self):
        return self.options[self._current_selection]
