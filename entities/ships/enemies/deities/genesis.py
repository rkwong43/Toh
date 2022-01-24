from entities.ships.enemies.deities.deity import Deity
from utils.ids.enemy_id import EnemyID

""""Genesis enemy deity.
"""


class Genesis(Deity):
    def __init__(self, hp, fire_rate):
        super().__init__(EnemyID.MANDIBLE, hp, fire_rate)
        """
        Will also passively fire at the player.
        States:
        BIRTH = Spawn seraphs, will not take damage while enemies are alive, will fire at player
        CREATION = Fires railgun blasts from the top of the screen / after Origin, more projectiles and staggered speeds
        LIFE = In a rotating circle, spews out projectiles
        ORIGIN = At 50%, increases own attack frequency and efficacy of moves
        GENESIS = CREATION but from the sides and bottom as well, happens at death. Victory if surviving
        """
