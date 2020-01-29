from enum import Enum, auto

"""Represents the IDs of different ships, projectiles, and game modes.
"""


class EntityID(Enum):
    # Different ID's to generalize different types of entities
    WEAPON = auto()
    SHIP = auto()
    # Player:
    CITADEL = auto()
    # Enemies
    MANDIBLE = auto()
    CRUCIBLE = auto()
    MANTIS = auto()
    MOSQUITO = auto()
    SUBJUGATOR = auto()
    SEER = auto()
    # Large ships
    ARBITRATOR = auto()
    TERMINUS = auto()
    JUDICATOR = auto()
    # Larger ships
    DESPOILER = auto()
    MOTHERSHIP = auto()
    # Largest ships
    TITAN = auto()

    # Projectiles
    FRIENDLY_BULLET = auto()
    ENEMY_BULLET = auto()
    FRIENDLY_FLAK = auto()
    ENEMY_FLAK = auto()
    FRIENDLY_MISSILE = auto()
    ENEMY_MISSILE = auto()
    BAD_MISSILE = auto()
    # Effects
    EXPLOSION = auto()
    TITAN_EXPLOSION = auto()
    RED_EXPLOSION = auto()
    BLUE_EXPLOSION = auto()
    POPUP = auto()
    RED_CHARGE = auto()
    # Screen effects
    SHIELD_TINT = auto()
    HP_TINT = auto()
    # Weapon types
    GUN = auto()
    MACHINE_GUN = auto()
    FLAK_GUN = auto()
    FLAK_CANNON = auto()
    SHOTGUN = auto()
    MISSILE_LAUNCHER = auto()
    MULTI_MISSILE = auto()
    BAD_MISSILE_LAUNCHER = auto()
    RAILGUN = auto()
    # Difficulties
    EASY = auto()
    NORMAL = auto()
    HARD = auto()
    # Game modes
    SURVIVAL = auto()
    MANDIBLE_MADNESS = auto()
    TITAN_SLAYER = auto()
    HEAVEN = auto()
    TUTORIAL = auto()
    # Menu IDs
    GALLERY = auto()
