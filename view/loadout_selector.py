from src.utils import config
from src.utils.direction import Direction
from src.utils.ids.game_id import GameID
from src.utils.ids.player_id import PlayerID
from src.utils.ids.weapon_id import WeaponID
from src.view.menu_selector import MenuSelector

"""Defines a loadout selection screen. Currently supports picking a ship and a weapon.
Currently only supports taking the currently unlocked weapons and ships.
"""


class LoadoutSelector(MenuSelector):
    """Initializes the loadout selector.
    """

    # TODO: In future for challenges, have specified loadouts available
    def __init__(self):
        super().__init__([], GameID.LOADOUT, None)
        weapons = [weapon for weapon in WeaponID]
        ships = [ship for ship in PlayerID]
        self.options = [ships, weapons]
        # Selection is a tuple because can move screens
        self._current_selection = [ships.index(config.player_ship), weapons.index(config.weapon)]
        print(self._current_selection)
        self._number_of_options = [len(choices) for choices in self.options]
        self.current_list = 0
        # TODO: Description and stuff on the side

    """Selects the current loadout!
    """

    def select(self):
        config.player_ship = self.options[0][self._current_selection[0]]
        config.weapon = self.options[1][self._current_selection[1]]
        return None, None

    """Switches what is selected.

    :param direction: which way to go
    :type direction: Direction
    """

    def switch_selection(self, direction):
        if direction == Direction.LEFT:
            self.current_list = self.current_list - 1 if self.current_list != 0 else len(self.options) - 1
        elif direction == Direction.RIGHT:
            self.current_list = self.current_list + 1 if self.current_list != len(self.options) - 1 else 0
        else:
            curr = self._current_selection[self.current_list]
            if direction == Direction.UP:
                self._current_selection[self.current_list] = curr - 1 \
                    if curr - 1 >= 0 else self._number_of_options[self.current_list] - 1
            elif direction == Direction.DOWN:
                self._current_selection[self.current_list] = curr + 1 \
                    if curr + 1 < self._number_of_options[self.current_list] else 0

    """Returns the current options chosen.

   :returns: options to display
   :rtype: [ID]
   """

    def get_options(self):
        result = []
        for i in range(len(self._current_selection)):
            result.append(self.options[i][self._current_selection[i]])
        return result
