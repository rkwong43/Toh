from enum import Enum, auto

"""Represents the IDs of different enemy ships.
"""


class EnemyID(Enum):
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