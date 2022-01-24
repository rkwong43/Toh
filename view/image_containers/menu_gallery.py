from utils.ids.enemy_id import EnemyID
from utils.ids.game_id import GameID
from utils.ids.player_id import PlayerID
from utils.ids.weapon_id import WeaponID
from model.stats import ship_stats
from model.stats import weapon_stats

"""Represents a description and image of an entity along with its associated stats.
"""


class MenuGallery:
    # Tags to not display
    _do_not_display = ["PROJECTILE TYPE", "DESCRIPTION", "PROJECTILE COUNT", "SHIP TYPE"]

    """Constructs the MenuGallery.

    :param entity_id: ID of entity to show
    :type entity_id: PlayerID or EnemyID or WeaponID
    """

    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.name = entity_id.name.replace("_", " ")
        self.stats = []
        self.root = None
        self.entity_type = GameID.SHIP
        self.description = self.form_description()

    """Returns the root of the gallery.
    
    :returns: root of gallery
    :rtype: MenuTree
    """

    def goto_root(self):
        return self.root

    """Returns itself because it currently has no other options.
    
    :returns: itself
    :rtype: MenuGallery
    """
    def select(self):
        return self

    """Returns the description of the entity this is describing,
    :returns: Description of the entity
    :rtype: str
    """

    def form_description(self):
        if self.entity_id in WeaponID:
            stats = weapon_stats.stats[self.entity_id]
            self.entity_type = GameID.WEAPON
        else:
            stats = ship_stats.stats[self.entity_id]
        for tag, value in stats.items():
            if tag in self._do_not_display:
                continue
            self.stats.append(tag + ": " + str(value))
        if self.entity_id in EnemyID:
            self.entity_type = GameID.ENEMY
        elif self.entity_id in PlayerID:
            self.entity_type = GameID.SHIP
        return stats["DESCRIPTION"]
