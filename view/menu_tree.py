from src.model.stats import gamemode_stats
from src.utils.direction import Direction

"""Represents a tree of menus.
"""


class MenuTree:
    """Constructs this layer of the tree.

    :param options: dict of options to display on this layer of menus.
    :type options: {ID : MenuTree or MenuSelector}
    :param name: type of category this is under
    :type name: GameID
    """

    def __init__(self, name, options=None):
        if options is None:
            options = {}
        self.name = name
        self.options = options
        # Roots are assigned by parents
        self.root = None
        for child in self.options.values():
            try:
                child.root = self
            except (AttributeError, TypeError):
                continue
        self._current_selection = 0
        self._number_of_options = len(options)

        self.description = {}
        for key in self.options.keys():
            try:
                self.description[key] = gamemode_stats.descriptions[key]
            except KeyError:
                self.description[key] = None

    """Goes back up a layer.
    
    :returns: root if any
    :rtype: MenuTree
    """

    def goto_root(self):
        self._current_selection = 0
        return self.root

    """Adds a child node to this node.
    
    :param options: Options to give to the child
    :type options: list of str
    :param name: which option this child corresponds to
    """

    """Switches what is selected.
    
    :param direction: which way to go
    :type direction: Direction
    """

    def switch_selection(self, direction):
        if direction == Direction.UP:
            self._current_selection = self._current_selection - 1 \
                if self._current_selection - 1 >= 0 else self._number_of_options - 1
        elif direction == Direction.DOWN:
            self._current_selection = self._current_selection + 1 \
                if self._current_selection + 1 < self._number_of_options else 0

    """Returns the current selection's child.
    
    :returns: Current option selected
    :rtype: MenuTree or MenuSelector
    """

    def select(self):
        next_menu = list(self.options.items())[self._current_selection]
        try:
            next_menu[1].root = self
        except AttributeError:
            return next_menu[0], None
        return next_menu

    """Returns all the options listed.
    
    :returns: options to display
    :rtype: [str]
    """
    def get_options(self):
        result = []
        for k, v in self.options.items():
            result.append(k.name.replace("_", " "))
        return result

    """Returns the current selection on the menu.
    
    :returns: the currently selected option
    :rtype: int
    """
    def get_current_selection(self):
        return self._current_selection
