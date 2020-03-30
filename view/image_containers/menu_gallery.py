
from src.utils.ids.game_id import GameID
from src.utils.ids.weapon_id import WeaponID
from src.model.stats import ship_stats
from src.model.stats import weapon_stats

"""Represents a description and image of an entity along with its associated stats.
"""


class MenuGallery:
    """Constructs the MenuGallery.

    :param entity_id: ID of entity to show
    :type entity_id: EntityID
    """

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.name = entity_id.name.replace("_", " ")
        self.stats = []
        self.root = 0
        self.entity_type = GameID.SHIP
        self.description = self.form_description()

    """Returns the root of the gallery.
    
    :returns: root of gallery
    :rtype: MenuTree
    """

    def goto_root(self):
        return self.root

    """Returns -1 as a MenuGallery currently does not support selection or have any options.
    
    :returns: -1
    :rtype: int
    """
    def select(self):
        return -1

    """Returns the description of the entity this is describing,
    :returns: Description of the entity
    :rtype: str
    """

    def form_description(self):
        if self.entity_id in WeaponID:
            stats = weapon_stats.stats[self.entity_id]
            self.entity_type = GameID.WEAPON
            for tag, value in stats.items():
                if tag == "PROJECTILE TYPE" or tag == "DESCRIPTION":
                    continue
                self.stats.append(tag + ": " + str(value))
        else:
            self.entity_type = GameID.SHIP
            stats = ship_stats.stats[self.entity_id]
            for tag, value in stats.items():
                if tag == "SHIP TYPE" or tag == "DESCRIPTION":
                    continue
                self.stats.append(tag + ": " + str(value))

        return stats["DESCRIPTION"]
