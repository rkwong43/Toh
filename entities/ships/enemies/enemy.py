import math
import random

from src.entities.projectiles.bullet import Bullet
from src.entities.projectiles.diamond_dust import DiamondDust
from src.entities.projectiles.missile import Missile
from src.entities.ships.ship import Ship
from src.model.stats import ship_stats
from src.utils import config
from src.utils.ids.projectile_id import ProjectileID

"""Represents an enemy ship or structure."""


class Enemy(Ship):
    random.seed()
    """Constructor to make the enemy.

    :param ship_size: size the ship is
    :type ship_size: int
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
    :param entity_id: ID of enemy
    :type entity_id: EntityID
    """

    def __init__(self, entity_id, hp, shield, x, y, speed=0, ship_size=config.ship_size, fire_rate=config.game_fps):
        super().__init__(x, y, speed, hp, shield, ship_size)
        self.entity_id = entity_id
        ##################################################
        # Retrieving stats:
        stats = ship_stats.stats[entity_id]
        self.projectile_damage = stats["DAMAGE"]
        self.projectile_speed = stats["PROJECTILE SPEED"] * (30 / config.game_fps)
        self.score = stats["SCORE"]
        self.projectile_type = ProjectileID.ENEMY_BULLET
        # fire rate in seconds
        self.fire_rate = fire_rate
        # Angle it is facing
        self._angle = 0
        # If it is ready to fire again
        self.ready_to_fire = True
        # Angle offset to fire in
        # If greater than 0, fires in a cone of 2 * fire_variance degrees
        self.fire_variance = 0
        ##################################################
        # Determines the final moving position
        self.end_x, self.end_y = self._generate_pos()

    """Generates a new position to move into. Limited to the upper half of the playing screen.
    
    :returns: tuple of x and y pos
    :rtype: (int, int)
    """
    def _generate_pos(self):
        x = random.randint(config.ship_size, config.display_width - (2 * config.ship_size))
        y = random.randint(0, config.display_height / 2)
        return x, y

    """Moves the enemy to its predetermined location.
    """

    def move(self):
        if self.speed > 0:
            x_done = False
            if self.x < self.end_x - self.speed:
                self.x += self.speed
            elif self.x > self.end_x + self.speed:
                self.x -= self.speed
            else:
                x_done = True

            if self.y < self.end_y - self.speed:
                self.y += self.speed
            elif self.y > self.end_y + self.speed:
                self.y -= self.speed
            elif x_done:
                self.end_x, self.end_y = self._generate_pos()

    """Represents the angle the enemy is facing.
    
    :param target: target the enemy is facing
    :type target: Ship
    """

    def rotate(self, target):
        # Rotates the ship to face the target ship
        self._angle = -math.degrees(math.atan2(self.y - target.y, self.x - target.x)) - 90

    """Fires projectiles from the enemy to the given target, at the given speed, damage, and size.

    :param target: target area
    :type target: Ship
    :param projectiles: list of projectiles to append onto
    :type projectiles: List of Projectile
    """

    def fire(self, target, projectiles):
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
        angle = self._angle - 90 + offset
        weapon_type = self.projectile_type
        projectile = Bullet(self.projectile_speed, x_pos, y_pos,
                            angle + offset, self.projectile_damage,
                            weapon_type)
        if weapon_type == ProjectileID.ENEMY_MISSILE:
            projectile = Missile(self.projectile_speed, x_pos, y_pos,
                                 angle, self.projectile_damage,
                                 weapon_type, target)
        elif weapon_type == ProjectileID.DIAMOND_DUST:
            projectile = DiamondDust(self.projectile_speed, x_pos, y_pos,
                                     angle, self.projectile_damage,
                                     ProjectileID.ENEMY_BULLET, target)

        projectiles.append(projectile)
