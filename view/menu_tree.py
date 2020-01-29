
"""Represents a tree of menus.
"""
from src.direction import Direction


class MenuTree:
    """Constructs this layer of the tree.

    :param options: list of options to display on this layer of menus.
    :type options: list of str
    :param children: child nodes
    :type children: list of MenuTree or EntityID
    :param name: type of category this is under
    :type name: EntityID
    """
    def __init__(self, options, children, name):
        self.name = name
        self.options = options
        self.root = None
        # Children notation: either hold EntityIDs for their options, 0 for going to difficulty selection, or -1
        # if it does nothing
        self.children = children
        assert(len(children) == len(options))
        self.current_selection = 0
        self.number_of_options = len(options)

    """Goes back up a layer.
    
    :returns: root if any
    :rtype: MenuTree
    """
    def goto_root(self):
        self.current_selection = 0
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
            self.current_selection -= 1
            if self.current_selection < 0:
                self.current_selection = self.number_of_options - 1
        elif direction == Direction.DOWN:
            self.current_selection += 1
            if self.current_selection >= self.number_of_options:
                self.current_selection = 0

    """Returns the current selection's child.
    
    :returns: Current option selected
    :rtype: MenuTree or EntityID or int
    """
    def select(self):
        return self.children[self.current_selection]
