from src.entities.ships.enemies.enemy import Enemy
from src.utils import config
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Mothership enemy fighter that spawns smaller Mandibles."""


class Mothership(Enemy):
    # How many ships it spawns:
    ships_spawned = 2
    """Constructor to make the Mothership

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
        super().__init__(EnemyID.MOTHERSHIP, hp, shield, x, y, speed, int(2 * config.ship_size), fire_rate)
        # fire rate in seconds
        self.fire_rate = fire_rate * 2
        self.projectile_type = ProjectileID.ENEMY_MISSILE
        self.fire_variance = 30
        self.ai = ai

    """Mothership fires multiple missiles at the target.

    :param target: Target to fire at.
    :type target: Ship
    :param projectiles: Projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
        temp = self.fire_variance
        temp_speed = self.projectile_speed
        # Fires 2 slow missiles
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        self.fire_variance = 0
        # Fires one fast missile
        self.projectile_speed = 15 * (30 / config.game_fps)
        super().fire(target, projectiles)
        if self.ai is not None:
            for i in range(self.ships_spawned):
                ship = self.ai.spawn_enemy(EnemyID.MANDIBLE)
                ship.x, ship.y = self.x, self.y
        self.fire_variance = temp
        self.projectile_speed = temp_speed
