import random

from entities.effects.charge_up import ChargeUp
from entities.projectiles.bullet import Bullet
from entities.projectiles.diamond_dust import DiamondDust
from entities.projectiles.missile import Missile
from entities.projectiles.pulse import Pulse
from entities.ships.ship import Ship
from model.stats import ship_stats
from utils import config
from utils.ids.effect_id import EffectID
from utils.ids.projectile_id import ProjectileID

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
        self.angle = 0
        # If it is ready to fire again
        self.ready_to_fire = True
        # Angle offset to fire in
        # If greater than 0, fires in a cone of 2 * fire_variance degrees
        self.fire_variance = 0
        # Ticks to determine when to fire
        self.ticks = 0
        ##################################################
        # Determines the final moving position
        self.end_x, self.end_y = self._generate_pos()

    """Generates a new position to move into. Limited to the upper half of the playing screen.
    
    :returns: tuple of x and y pos
    :rtype: (int, int)
    """
    def _generate_pos(self):
        x = random.randint(0, config.display_width - self.size)
        y = random.randint(0, -self.size // 2 + config.display_height // 2)
        return x, y

    """Fires projectiles from the enemy to the given target, at the given speed, damage, and size.

    :param target: target area
    :type target: Ship
    :param projectiles: list of projectiles to append onto
    :type projectiles: List of Projectile
    :returns: The projectiles fired
    :rtype: Projectile
    """

    def fire(self, target, projectiles):
        if target is None:
            target = self.waypoint
        # Finds angle from source to target
        # If the enemy ship has any spread
        x_pos = self.x
        y_pos = self.y
        # This is to accommodate larger ships
        default_size = config.ship_size
        if self.size > config.ship_size:
            x_pos = self.x + ((self.size - default_size) // 2)
            y_pos = self.y + ((self.size - default_size) // 2)
        offset = random.randint(-self.fire_variance, self.fire_variance)
        angle = self.angle - 90 + offset
        weapon_type = self.projectile_type
        projectile = Bullet(self.projectile_speed, x_pos, y_pos, angle + offset, self.projectile_damage, weapon_type)
        if weapon_type == ProjectileID.ENEMY_MISSILE:
            projectile = Missile(self.projectile_speed, x_pos, y_pos, angle, self.projectile_damage, weapon_type,
                                 target)
        elif weapon_type == ProjectileID.DIAMOND_DUST:
            projectile = DiamondDust(self.projectile_speed, x_pos, y_pos, angle, self.projectile_damage,
                                     ProjectileID.ENEMY_BULLET, target)
        elif weapon_type == ProjectileID.PULSE:
            projectile = self._fire_pulse(target)
        projectiles.append(projectile)
        return projectile

    """Returns a pulse projectile.
    
    :param target: target to fire pulse at.
    :type target: Ship or WayPoint
    :returns: Pulse projectile
    :rtype: Pulse
    """
    def _fire_pulse(self, target):
        radius = config.ship_size * 1.5 // 2
        offset = target.size // 2
        rand_x = random.randint(-self.fire_variance, self.fire_variance)
        rand_y = random.randint(-self.fire_variance, self.fire_variance)
        projectile = Pulse(self.projectile_speed, target.x + rand_x + offset - radius, target.y + rand_y +
                           offset - radius,
                           self.projectile_damage, radius)
        charge = ChargeUp(projectile.x + projectile.size / 2, projectile.y + projectile.size / 2, EffectID.RED_AOE)
        dif = 2 * self.projectile_speed // charge.charge_frames
        charge.frame_multiplier = dif if dif > 0 else 2
        charge.max_frame = ((self.projectile_speed // 5) * 5) - 1
        self.effects.append(charge)
        return projectile
