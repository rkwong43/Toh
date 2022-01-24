from entities.ships.enemies.deities.deity import Deity
from utils.ids.enemy_id import EnemyID

""""Sin enemy deity.
"""


class Sin(Deity):
    def __init__(self, hp, fire_rate):
        super().__init__(EnemyID.MANDIBLE, hp, fire_rate)
        """
        Will also passively fire at the player.
        States:
        LUST = Gives itself a temporary shield (set, not add, do not change max shield)
        GLUTTONY = Fires homing bullets that heal itself if hit / Increased healing after using Pride
        GREED = Steals player's buffs (to be implemented with gear patch)
        SLOTH = Fires a projectile that slows the player's fire rate / slows player's movement speed after Pride
        WRATH = Fires variety of projectiles outwards / More projectiles after using Pride
        ENVY = Fires projectiles from the bottom of the screen upwards
        PRIDE = Happens at 50%, increases effects of each state
        SIN = Happens at death, uses every move. Surviving means victory
        """
