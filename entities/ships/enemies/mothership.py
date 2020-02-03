from src.entities.ships.enemies.enemy import Enemy
from src.utils.entity_id import EntityID

"""Represents a Mothership enemy fighter that spawns smaller Mandibles."""


class Mothership(Enemy):
    # How many ships it spawns:
    ships_spawned = 2
    """Constructor to make the Mothership

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

    def __init__(self, ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, fps, ai):
        super().__init__(ship_size, x, y, hp, end_x, end_y, speed, fire_rate, shield, True, fps, EntityID.MOTHERSHIP)
        # fire rate in seconds
        self.fire_rate = fire_rate * 2
        self.projectile_type = EntityID.ENEMY_MISSILE
        self.fire_variance = 30
        self.ai = ai


    """Despoiler fires multiple flak rounds at the target.

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
        self.fire_variance = 0
        self.projectile_speed = 15 * (32 / self.fps)
        super().fire(target, projectiles)
        if self.ai is not None:
            for i in range(self.ships_spawned):
                ship = self.ai.spawn_enemy(EntityID.MANDIBLE)
                ship.x, ship.y = self.x, self.y
        self.fire_variance = temp
        self.projectile_speed = temp_speed
