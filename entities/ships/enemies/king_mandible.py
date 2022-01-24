from entities.ships.enemies.burstfire_enemy import BurstFireEnemy
from utils import config

from utils.ids.enemy_id import EnemyID
from utils.ids.projectile_id import ProjectileID

"""Represents a King Mandible enemy fighter. Fires a burst of bullets."""


class KingMandible(BurstFireEnemy):
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

    def __init__(self, hp, shield, x, y, speed, fire_rate, **args):
        super().__init__(EnemyID.KING_MANDIBLE, hp, shield, x, y, speed, int(4 * config.ship_size), 4 * fire_rate, 60)
        self._fire_angle = -90
        self._phase = 1

    """Reloads the burst weapon.
    """

    def reload(self):
        self._burst_curr -= 1
        if self._burst_curr <= 0:
            self.ready_to_fire = False
            self._reload_curr -= 1
            self._fire_angle = -90

        if self._reload_curr <= 0:
            self._reload_curr = self._reload_speed
            self._burst_curr = self._burst_max
            self.ready_to_fire = True

    """Fires in a spinning circle around itself.
    """

    def fire(self, target, projectiles):
        temp = self.angle
        self.angle = self._fire_angle
        super().fire(target, projectiles)
        self.angle = temp
        self._fire_angle += 15
        if self._fire_angle == 360:
            self._fire_angle = 0

    """Changes weapon type when under 50% HP.
    """
    def damage(self, damage):
        super().damage(damage)
        if self.hp < self.max_hp // 2 and self._phase != 2:
            self._phase = 2
            self.projectile_type = ProjectileID.ENEMY_MISSILE
            self._burst_max *= 2
            self.projectile_speed += 5
            self._reload_speed //= 2
            self._reload_curr = 0
