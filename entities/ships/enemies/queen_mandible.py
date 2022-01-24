from entities.ships.enemies.enemy import Enemy
from utils import config
from utils.ids.enemy_id import EnemyID
from utils.ids.projectile_id import ProjectileID

"""Represents a Queen Mandible carrier.
"""


class QueenMandible(Enemy):
    """Constructor to make the Queen Mandible.

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
    :param ai: enemy AI to control
    :type ai: EnemyAI
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, ai, **args):
        super().__init__(EnemyID.QUEEN_MANDIBLE, hp, shield, x, y, speed, int(4 * config.ship_size), 4 * fire_rate)
        # fire rate in seconds
        self.projectile_type = ProjectileID.ENEMY_MISSILE
        self.fire_variance = 45
        self._ai = ai
        self._phase = 1
        # How many ships it spawns:
        self.ships_spawned = 2

    """Mothership fires multiple missiles at the target.

    :param target: Target to fire at.
    :type target: Ship
    :param projectiles: Projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
        temp_speed = self.projectile_speed
        # Fires 2 slow missiles
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        # Fires two fast missiles
        if self.hp < self.max_hp // 2:
            self.projectile_speed = 15 * (30 / config.game_fps)
            super().fire(target, projectiles)
            super().fire(target, projectiles)
        if self._ai is not None:
            for i in range(self.ships_spawned):
                ship = self._ai.spawn_enemy(EnemyID.MANDIBLE)
                ship.x, ship.y = self.x + self.size // 2, self.y + self.size // 2
        self.projectile_speed = temp_speed

    """Increases fire rate when less than 50% HP
    """
    def damage(self, damage):
        super().damage(damage)
        if self.hp < self.max_hp // 2 and self._phase != 2:
            self._phase = 2
            self.fire_rate //= 2
            self.ticks = 0
