from src.entities.ships.enemies.enemy import Enemy
from src.entities.ships.enemies.mantis import Mantis
from src.entities.ships.enemies.terminus import Terminus
from src.entity_id import EntityID

"""Represents a Titan enemy cruiser."""


class Titan(Enemy):
    # Number of ships it spawns
    ships_spawned = 1
    """Constructor to make the Titan ship

    :param ship_size: size the ship should be
    :type ship_size: int
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

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, fps, ai, effects):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, False, fps, EntityID.TITAN)
        self.entity_id = EntityID.TITAN
        # fire rate in seconds
        self.fire_rate = fire_rate * 8
        self.projectile_type = EntityID.ENEMY_MISSILE
        self.fire_variance = 45
        self.ai = ai
        self.turrets = []
        self.effects = effects

    """Spawns turrets for itself.
    """

    def spawn_turrets(self):
        # Terminus center turret
        base_size = self.ai.model.ship_size
        center_x = self.x + (self.size // 2)
        left_x = center_x - base_size
        right_x = center_x + base_size
        center_y = self.y + (self.size // 2)
        # Mantis side turrets
        # Upper middle
        mantis1 = Mantis(base_size, left_x - (base_size // 2), center_y - base_size, self.max_hp, 0, 0, 0,
                         self.fire_rate // 7, 0,
                         False, self.fps)
        mantis2 = Mantis(base_size, right_x - (base_size // 2), center_y - base_size, self.max_hp, 0, 0, 0,
                         self.fire_rate // 7, 0,
                         False, self.fps)
        # Lower middle
        mantis3 = Mantis(base_size, left_x - base_size, center_y, self.max_hp, 0, 0, 0,
                         self.fire_rate // 6, 0,
                         False, self.fps)
        mantis4 = Mantis(base_size, right_x, center_y, self.max_hp, 0, 0, 0,
                         self.fire_rate // 6, 0,
                         False, self.fps)
        # Far left
        mantis5 = Mantis(base_size, left_x - (1.5 * base_size), center_y - base_size, self.max_hp, 0, 0,
                         0, self.fire_rate // 5, 0, False, self.fps)
        mantis5.burst_max = 8
        mantis5.burst_curr = 8
        # Far right
        mantis6 = Mantis(base_size, right_x + (base_size // 2), center_y - base_size, self.max_hp, 0, 0,
                         0, self.fire_rate // 5, 0, False, self.fps)
        mantis6.burst_max = 8
        mantis6.burst_curr = 8
        # Middle
        mantis7 = Mantis(base_size, center_x - (base_size // 2), center_y, self.max_hp, 0, 0, 0,
                         self.fire_rate // 8, 0, False, self.fps)
        # Middle Terminus
        terminus = Terminus(base_size * 1.5, center_x - (base_size * .75),
                            center_y - base_size, self.max_hp, center_x - (base_size * .75),
                            center_y, 0, self.fire_rate // 6, 0, self.fps, self.effects)
        terminus.move_again = False
        terminus.projectile_damage = 20
        self.turrets = [mantis1, mantis2, mantis3, mantis4, mantis5, mantis6, mantis7, terminus]
        for ship in self.turrets:
            ship.finished_moving = True
        self.ai.model.enemy_ships.extend(self.turrets)

    """Doesn't rotate at all.
    """

    def rotate(self, target):
        pass

    """Moves itself and has its children move too.
    """

    def move(self):
        if len(self.turrets) == 0:
            self.spawn_turrets()
        # Just moves down:
        if self.y != -self.size // 4:
            self.y += self.speed
            for turret in self.turrets:
                turret.y += self.speed

    """Despoiler fires multiple missiles at the target.

    :param target: Target to fire at.
    :type target: Ship
    :param projectiles: Projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
        temp = self.fire_variance
        # Fires 3 missiles
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        super().fire(target, projectiles)
        self.fire_variance = 0
        self.projectile_speed = 15 * (32 / self.fps)
        super().fire(target, projectiles)
        if self.ships_spawned < 6:
            for i in range(self.ships_spawned):
                ship = self.ai.spawn_enemy(EntityID.CRUCIBLE)
                ship.x, ship.y = self.x + (self.size // 2), self.y + (self.size // 2)
        self.fire_variance = temp
