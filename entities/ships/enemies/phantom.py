from src.entities.effects.charge_up import ChargeUp
from src.entities.projectiles.pulse import Pulse
from src.entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from src.utils import config
from src.utils.ids.effect_id import EffectID

from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Phantom enemy fighter. Fires pulses of energy."""


class Phantom(BurstFireEnemy):
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
        super().__init__(EnemyID.PHANTOM, hp, shield, x, y, speed, config.ship_size * 2, fire_rate * 4, 8,
                         burst_rate=6)
        self.fire_variance = 2
        self.stealth = True
        self.projectile_type = ProjectileID.PULSE
        self.effects = effects

    """Fires a burst of bullets.
    """
    def fire(self, target, projectiles):
        super().fire(target, projectiles)
        self.is_damaged = True
        self.stealth = False

    """Stealth as it moves.
    """
    def move(self):
        self.stealth = True
        super().move()

    """Returns a pulse projectile.
    
    :param target: target to fire pulse at.
    :type target: Ship or WayPoint
    :returns: Pulse projectile
    :rtype: Pulse
    """
    def _fire_pulse(self, target):
        radius = config.ship_size * 1.5 // 2
        offset = target.size // 2
        projectile = Pulse(self.projectile_speed, target.x + offset - radius, target.y + offset - radius,
                           self.projectile_damage, radius)
        charge = ChargeUp(projectile.x + projectile.size / 2, projectile.y + projectile.size / 2, EffectID.RED_AOE)
        dif = charge.charge_delay // self.projectile_speed
        charge.frame_multiplier = dif if dif > 0 else 1
        charge.max_frame = ((self.projectile_speed // 5) * 5) - 1
        self.effects.append(charge)
        return projectile
