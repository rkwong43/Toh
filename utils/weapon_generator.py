import random

from src.utils import config
from src.utils.ids.projectile_id import ProjectileID

projectile_types = [ProjectileID.FRIENDLY_MISSILE, ProjectileID.FRIENDLY_BULLET, ProjectileID.FRIENDLY_FLAK,
                    ProjectileID.HOMING_BULLET, ProjectileID.DIAMOND_DUST]
BURST_FIRE = 1  # Fires a burst then reloads
REGULAR = 2  # Continuously fires single rounds
SPREADER = 3  # Fires at a spread

"""Generates a random weapon with randoms stats. Does not include railgun type weapons.
"""


def generate_weapon():
    random.seed()
    result = {"PROJECTILE SPEED": random.randint(10, 25)}
    weapon_type = [BURST_FIRE, REGULAR, SPREADER][random.randint(0, 2)]
    random_fire_rate = random.randint(3, config.game_fps // 2)
    result["RELOAD"] = random_fire_rate
    if weapon_type == BURST_FIRE:
        bursts = random.randint(0, 12)
        result["BURSTS"] = bursts
        multiple_or_single = random.randint(0, 1)
        if multiple_or_single == 0:
            result["PROJECTILE COUNT"] = 1
            result["SPREAD"] = random.randint(0, 30)
        else:
            projectile_count = random.randint(2, 6)
            result["PROJECTILE COUNT"] = projectile_count
            result["SPREAD"] = random.randint(1, 6) * (projectile_count + 1)
    elif weapon_type == REGULAR:
        result["BURSTS"] = 0
        result["PROJECTILE COUNT"] = 1
        result["SPREAD"] = random.randint(0, 30)
    else:
        result["BURSTS"] = 0
        projectile_count = random.randint(2, 8)
        result["PROJECTILE COUNT"] = projectile_count
        result["SPREAD"] = random.randint(1, 6) * (projectile_count + 1)

    result["PROJECTILE TYPE"] = projectile_types[random.randint(0, len(projectile_types) - 1)]
    dps = random.randint(80, 300)
    bursts_modifier = result["BURSTS"] if result["BURSTS"] > 0 else 1
    result["DAMAGE"] = dps / ((config.game_fps / random_fire_rate) * (bursts_modifier * result["PROJECTILE COUNT"]))
    if result["DAMAGE"] == 0:
        result["DAMAGE"] = 1
    return result
