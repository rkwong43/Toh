from src.entities.ships.allies.ally import Ally
from src.utils import config, enemy_generator
from src.utils.ids.ally_id import AllyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents a Longsword friendly cruiser."""


class Longsword(Ally):
    # Number of ships it spawns
    ships_spawned = 1
    """Constructor to make the Longsword ship

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

    def __init__(self, hp, shield, x, y, speed, fire_rate, effects, **args):
        super().__init__(hp, shield, x, y, speed, fire_rate)
        self.size = int(8 * config.ship_size)
        self.entity_id = AllyID.LONGSWORD
        self.projectile_type = ProjectileID.FRIENDLY_MISSILE
        self.fire_variance = 60
        self._turrets = []
        self._effects = effects
        self._ships_spawned_total = 0

    """Spawns turrets for itself.
    """

    def spawn_turrets(self):
        x_pos = (self.x + (self.size / 2)) - config.ship_size
        for _ in range(2):
            for i in range(3):
                y_pos = self.y + (self.size / 2) - (i * config.ship_size)
                archer = enemy_generator.generate_enemy(AllyID.ARCHER, x_pos, y_pos, hp=self.hp + self.shield,
                                                        fire_rate=config.game_fps // 2)
                archer.projectile_damage = 8
                archer.remove_if_offscreen = False
                self._turrets.append(archer)
            x_pos += config.ship_size
        return self._turrets

    """Doesn't rotate at all.
    """

    def rotate(self, target):
        pass

    """Moves itself and its turrets. Only works with waypoints.
    """
    def move(self):
        if self.speed > 0:
            x_change = 0
            if self.x < self.waypoint.x - self.speed:
                self.x += self.speed
                x_change += self.speed
            elif self.x > self.waypoint.x + self.speed:
                self.x -= self.speed
                x_change -= self.speed
            y_change = 0
            if self.y < self.waypoint.y - self.speed:
                self.y += self.speed
                y_change += self.speed
            elif self.y > self.waypoint.y + self.speed:
                self.y -= self.speed
                y_change -= self.speed
            for turret in self._turrets:
                turret.x += x_change
                turret.y += y_change

    """Longsword doesn't do anything when firing.

    :param target: Target to fire at.
    :type target: Ship
    :param projectiles: Projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
        pass

    """Damages itself and removes turrets upon death.
    """

    def damage(self, damage):
        super().damage(damage)
        for turret in self._turrets:
            turret.damage(damage)

    """Kills all of its turrets if offscreen.
    """
    def offscreen(self):
        for turret in self._turrets:
            turret.is_dead = True
            turret.hp = 0
