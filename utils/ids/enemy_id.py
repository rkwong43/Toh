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
    SPECTRE = auto()
    # Large ships
    ARBITRATOR = auto()
    TERMINUS = auto()
    JUDICATOR = auto()
    # Larger ships
    DESPOILER = auto()
    MOTHERSHIP = auto()
    PHANTOM = auto()
    CYCLOPS = auto()
    # Largest ships
    TITAN = auto()
    # Bosses
    KING_MANDIBLE = auto()
    QUEEN_MANDIBLE = auto()
    # Spawner:
    # GENESIS = auto()
    # Destruction:
    # SIN = auto()
    # Both:
    # NIRVANA = auto()
