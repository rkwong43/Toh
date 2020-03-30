import math

from src.entities.effects.charge_up import ChargeUp
from src.entities.ships.enemies.enemy import Enemy
from src.utils import config
from src.utils.ids.effect_id import EffectID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Terminus enemy fighter."""


class Terminus(Enemy):
    """Constructor to make the Terminus ship

    :param ship_size: size the ship should be
    :type ship_size: int
    :param x: starting x coordinate of ship
    :type x: int
    :param y: starting y coordinate of ship
    :type y: int
    :param hp: hit points of ship
    :type hp: int
    :param speed: speed it moves towards the ending position
    :type speed: int
    :param fire_rate: fire rate of the enemy
    :type fire_rate: int
    :param shield: shield health
    :type shield: int
    :param effects: list of effects in the game
    :type effects: List of Effect
    """

    def __init__(self, hp, shield, x, y, speed, ship_size, fire_rate, effects, *args):
        super().__init__(EnemyID.TERMINUS, hp, shield, x, y, speed, ship_size, fire_rate)
        # fire rate in seconds
        self.fire_rate = int(fire_rate * 5)
        self.projectile_type = ProjectileID.RAILGUN_BLAST
        self.effects = effects
        self.projectile_damage *= (30 / config.game_fps)

    """Moves, but adds a charge-up effect for when it's about to fire.
    """
    def move(self):
        super().move()
        if self.fire_rate - 16 == self.ticks:
            offset_x = int(math.sin(math.radians(self.angle)) * (self.size // 4))
            offset_y = int(math.cos(math.radians(self.angle)) * (self.size // 5))
            charge = ChargeUp(self.x + offset_x, self.y + offset_y, EffectID.RED_CHARGE)
            self.effects.append(charge)
