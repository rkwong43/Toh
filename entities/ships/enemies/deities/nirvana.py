from src.entities.ships.enemies.deities.deity import Deity
from src.utils.ids.enemy_id import EnemyID

""""Nirvana enemy deity.
"""


class Nirvana(Deity):
    def __init__(self, hp, fire_rate):
        super().__init__(EnemyID.MANDIBLE, hp, fire_rate)
        """
        States:
        ENLIGHTENMENT = Forms a heart, will detonate and deal massive damage if not destroyed / Fires at player
        OBLIVION = Fires rapid railgun blasts at player / 
        EMPYREAN = 
        DIVINITY = 
        IMMORTALITY = Spawns multiple "hearts", will not take damage until hearts are destroyed
        ASCENSION = At 50% increases own stats and move efficacy
        ETERNITY = 
        INFINITY = 
        HEAVEN = Railgun blasts from every cardinal direction
        NIRVANA = 
        """
