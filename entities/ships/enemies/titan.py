from src.entities.ships.enemies.enemy import Enemy
from src.utils import config, enemy_generator
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Titan enemy cruiser."""


class Titan(Enemy):
    # Number of ships it spawns
    ships_spawned = 1
    """Constructor to make the Titan ship

    :param x: starting x coordinate of ship
    :type x: int
    :param y: starting y coordinate of ship
    :type y: int
    :param hp: hit points of ship
    :type hp: int
    :param end_x: ending x position
    :type end_x: int
    :param end_y: ending y position
    :type end_y: int
    :param speed: speed it moves towards the ending position
    :type speed: int
    :param fire_rate: fire rate of the enemy
    :type fire_rate: int
    :param shield: shield health
    :type shield: int
    :param fps: frames per second
    :type fps: int
    :param ai: enemy AI to control
    :type ai: EnemyAI
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, ai, effects, **args):
        super().__init__(EnemyID.TITAN, hp, shield, x, y, speed, int(8 * config.ship_size), fire_rate)
        # fire rate in seconds
        self.fire_rate = fire_rate * 8
        self.projectile_type = ProjectileID.ENEMY_MISSILE
        self.fire_variance = 45
        self._ai = ai
        self._turrets = []
        self._effects = effects
        self._ships_spawned_total = 0

    """Spawns turrets for itself.
    """

    def spawn_turrets(self):
        # Terminus center turret
        base_size = config.ship_size
        center_x = self.x + (self.size // 2)
        left_x = center_x - base_size
        right_x = center_x + base_size
        center_y = self.y + (self.size // 2)
        # Mantis side turrets
        # Upper middle
        mantis1 = enemy_generator.generate_enemy(EnemyID.SUBJUGATOR, left_x - (base_size // 2), center_y - base_size,
                                                 hp=self.max_hp, shield=self.max_shield, fire_rate=self.fire_rate // 5)
        mantis2 = enemy_generator.generate_enemy(EnemyID.SUBJUGATOR, right_x - (base_size // 2), center_y - base_size,
                                                 hp=self.max_hp, shield=self.max_shield, fire_rate=self.fire_rate // 5)
        # Lower middle
        mantis3 = enemy_generator.generate_enemy(EnemyID.MANTIS, left_x - base_size, center_y, hp=self.max_hp,
                                                 shield=self.max_shield, fire_rate=self.fire_rate // 4)
        mantis4 = enemy_generator.generate_enemy(EnemyID.MANTIS, right_x, center_y, hp=self.max_hp,
                                                 shield=self.max_shield, fire_rate=self.fire_rate // 4)
        # Far left
        mantis5 = enemy_generator.generate_enemy(EnemyID.MANTIS, left_x - (1.5 * base_size), center_y - base_size,
                                                 hp=self.max_hp, shield=self.max_shield, fire_rate=self.fire_rate // 3)
        # Far right
        mantis6 = enemy_generator.generate_enemy(EnemyID.MANTIS, right_x + (base_size // 2), center_y - base_size,
                                                 hp=self.max_hp, shield=self.max_shield, fire_rate=self.fire_rate // 3)
        # Middle
        mantis7 = enemy_generator.generate_enemy(EnemyID.MANTIS, center_x - (base_size // 2), center_y, hp=self.max_hp,
                                                 shield=self.max_shield, fire_rate=self.fire_rate // 6)
        # Middle Terminus
        terminus = enemy_generator.generate_enemy(EnemyID.TERMINUS, center_x - (.75 * base_size), center_y - base_size,
                                                  hp=self.max_hp, shield=self.max_shield, fire_rate=self.fire_rate // 4,
                                                  effects=self._effects)
        terminus.projectile_damage = 20
        self._turrets = [mantis1, mantis2, mantis3, mantis4, mantis5, mantis6, mantis7, terminus]
        return self._turrets

    """Doesn't rotate at all.
    """

    def rotate(self, target):
        pass

    """Moves itself and has its children move too.
    """

    def move(self):
        # Just moves down:
        if self.y != -self.size // 4:
            self.y += self.speed
            for turret in self._turrets:
                turret.y += self.speed

    """Despoiler fires multiple missiles at the target.

    :param target: Target to fire at.
    :type target: Ship
    :param projectiles: Projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
        temp = self.fire_variance
        temp_speed = self.projectile_speed
        # Fires 3 missiles
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        self.fire_variance = 0
        self.projectile_speed = int(15 * (30 / config.game_fps))
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        if self._ships_spawned_total < 3:
            for i in range(self.ships_spawned):
                ship = self._ai.spawn_enemy(EnemyID.CRUCIBLE)
                ship.x, ship.y = self.x + (self.size // 2), self.y + (self.size // 2)
            self._ships_spawned_total += 1
        self.fire_variance = temp
        self.projectile_speed = temp_speed

    """Damages itself and removes turrets upon death.
    """

    def damage(self, damage):
        super().damage(damage)
        for turret in self._turrets:
            turret.damage(damage)
