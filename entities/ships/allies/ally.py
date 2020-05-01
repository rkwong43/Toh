import math
import random

import pygame

from src.entities.projectiles.bullet import Bullet
from src.entities.projectiles.diamond_dust import DiamondDust
from src.entities.projectiles.missile import Missile
from src.entities.ships.ship import Ship
from src.utils import config
from src.utils.ids.player_id import PlayerID
from src.utils.ids.projectile_id import ProjectileID

"""A friendly allied ship.
"""


class Ally(Ship):
    """Constructs the ally.
    """

    def __init__(self, hp, shield, x, y, speed, fire_rate, *args, **kwargs):
        super().__init__(x, y, speed, hp, shield, config.ship_size)
        self.entity_id = PlayerID.CITADEL
        # TODO: Set up ship stats for generic players
        self.projectile_damage = 10
        self.projectile_speed = 15 * (30 / config.game_fps)
        self.score = 0
        self.projectile_type = ProjectileID.FRIENDLY_BULLET
        # fire rate in seconds
        self.fire_rate = fire_rate
        # Angle it is facing
        self.angle = 0
        # If it is ready to fire again
        self.ready_to_fire = True
        # Angle offset to fire in
        # If greater than 0, fires in a cone of 2 * fire_variance degrees
        self.fire_variance = 0
        # Ticks to determine when to fire
        self.ticks = 0

    """Fires at the angle the ship is facing.
    :param target: Target for missiles
    :type target: Ship
    :param projectiles: List of projectiles to append onto
    :type projectiles: [Projectile]
    """

    def fire(self, target, projectiles):
        if target is None:
            target = self.waypoint
        # Finds angle from source to target
        # If the enemy ship has any spread
        x_pos = self.x
        y_pos = self.y
        # Base ship size is 100x100 px
        # This is to accommodate larger ships
        default_size = config.ship_size
        if self.size > config.ship_size:
            x_pos = self.x + ((self.size - default_size) // 2)
            y_pos = self.y + ((self.size - default_size) // 2)
        offset = random.randint(-self.fire_variance, self.fire_variance)
        angle = self.angle + 90 + offset
        weapon_type = self.projectile_type
        projectile = Bullet(self.projectile_speed, x_pos, y_pos, angle + offset, self.projectile_damage, weapon_type)
        if weapon_type == ProjectileID.FRIENDLY_MISSILE:
            projectile = Missile(self.projectile_speed, x_pos, y_pos, angle, self.projectile_damage, weapon_type,
                                 target)
        elif weapon_type == ProjectileID.DIAMOND_DUST:
            projectile = DiamondDust(self.projectile_speed, x_pos, y_pos, angle, self.projectile_damage,
                                     ProjectileID.ENEMY_BULLET, target)

        projectiles.append(projectile)

    """Represents the angle the ship is facing.

        :param target: target the ship is facing
        :type target: Ship or Waypoint
        """

    def _rotate(self, target):
        # Rotates the ship to face the target ship
        # Rotates the ship to face the target ship
        # Adjustment for larger ships
        y = target.y
        x = target.x
        if target.size > config.ship_size:
            x += (target.size // 2) - config.ship_size // 2
            y += (target.size // 2) - config.ship_size // 2
        y_dist = self.y - y
        x_dist = self.x - x
        target_angle = -int(math.degrees(math.atan2(y_dist, x_dist))) + 90
        if abs(self.angle - target_angle) > self.rotation_speed:
            v1 = pygame.math.Vector2()
            v1.from_polar((1, self.angle))
            v2 = pygame.math.Vector2()
            v2.from_polar((1, target_angle))
            angle_change = -self.rotation_speed if v1.angle_to(v2) < 0 else self.rotation_speed
            self.angle += angle_change

    """Rotates the ship towards its waypoint.
        """

    def _rotate_to_wp(self, *args):
        self.angle = -math.degrees(math.atan2(self.y - self.waypoint.y, self.x - self.waypoint.x)) + 90

    """Generates a new position to move into. 

        :returns: tuple of x and y pos
        :rtype: (int, int)
        """

    def _generate_pos(self):
        x = random.randint(config.ship_size, config.display_width - (2 * config.ship_size))
        y = random.randint(config.display_height // 2, config.display_height - config.ship_size)
        return x, y
