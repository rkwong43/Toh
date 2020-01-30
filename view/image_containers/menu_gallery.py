from src.utils.entity_id import EntityID
from src.model.stats.ship_stats import get_ship_stats
from src.model.stats.weapon_stats import get_weapon_stats

"""Represents a description and image of an entity along with its associated stats.
"""


class MenuGallery:
    """Constructs the MenuGallery.

    :param entity_id: ID of entity to show
    :type entity_id: EntityID
    """

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.name = entity_id.name
        self.stats = []
        self.root = 0
        self.entity_type = EntityID.SHIP
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
        weapon_stats = get_weapon_stats(self.entity_id)
        if len(weapon_stats) > 0:
            self.entity_type = EntityID.WEAPON
            for tag, value in weapon_stats.items():
                if tag == "PROJECTILE TYPE" or tag == "DESCRIPTION" or tag == "NAME":
                    continue
                self.stats.append(tag + ": " + str(value))
            self.name = weapon_stats["NAME"]
            return weapon_stats["DESCRIPTION"]
        else:
            self.entity_type = EntityID.SHIP
            ship_stats = get_ship_stats(self.entity_id)
            for tag, value in ship_stats.items():
                if tag == "SHIP TYPE" or tag == "DESCRIPTION" or tag == "NAME":
                    continue
                self.stats.append(tag + ": " + str(value))
            self.name = ship_stats["NAME"]
            return ship_stats["DESCRIPTION"]
