import random

from src.entities.effects.charge_up import ChargeUp
from src.entities.projectiles.pulse import Pulse
from src.entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from src.utils import config
from src.utils.ids.effect_id import EffectID

from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Cyclops enemy fighter. Fires pulses of energy."""


class Cyclops(BurstFireEnemy):
    """Constructor to make the enemy.

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
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, effects, **args):
        super().__init__(EnemyID.CYCLOPS, hp, shield, x, y, speed, config.ship_size * 3, fire_rate * 3, 6,
                         burst_rate=2)
        self.projectile_type = ProjectileID.PULSE
        self.effects = effects
        random.seed()

    """Fires a bunch of pulse rounds.
    """

    def fire(self, target, projectiles):
        for _ in range(4):
            super().fire(target, projectiles)

    """Fires a pulse round near the target.
    """

    def _fire_pulse(self, target):
        radius = config.ship_size * 1.5 // 2
        offset = target.size // 2
        rand_x = random.randint(-2 * config.ship_size, 2 * config.ship_size)
        rand_y = random.randint(-2 * config.ship_size, 2 * config.ship_size)
        projectile = Pulse(self.projectile_speed, target.x + rand_x + offset - radius, target.y + rand_y +
                           offset - radius,
                           self.projectile_damage, radius)
        charge = ChargeUp(projectile.x + projectile.size / 2, projectile.y + projectile.size / 2, EffectID.RED_AOE)
        dif = 2 * self.projectile_speed // charge.charge_frames
        charge.frame_multiplier = dif if dif > 0 else 2
        charge.max_frame = ((self.projectile_speed // 5) * 5) - 1
        self.effects.append(charge)
        return projectile
