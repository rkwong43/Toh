from src.entities.ships.allies.ally import Ally
from src.utils import config
from src.utils.ids.ally_id import AllyID
from src.utils.ids.player_id import PlayerID
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

    def __init__(self, hp, shield, x, y, speed, fire_rate, ai, effects, **args):
        super().__init__(hp, shield, x, y, speed, fire_rate * 10)
        self.size = int(8 * config.ship_size)
        self.entity_id = AllyID.LONGSWORD
        self.projectile_type = ProjectileID.FRIENDLY_MISSILE
        self.fire_variance = 45
        self._ai = ai
        self._turrets = []
        self._effects = effects
        self._ships_spawned_total = 0

    """Spawns turrets for itself.
    """

    def spawn_turrets(self):
        return self._turrets

    """Doesn't rotate at all.
    """

    def rotate(self, target):
        pass

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
        if self._ai is not None:
            if self._ships_spawned_total < 6:
                for i in range(self.ships_spawned):
                    ship = self._ai.spawn_enemy(PlayerID.CITADEL)
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
