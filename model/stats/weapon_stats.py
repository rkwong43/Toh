from src.utils.entity_id import EntityID

"""Returns a dictionary of the given weapon's statistics.
:param entity_id: ID of weapon
:type entity_id: EntityID
:returns: dictionary of weapon statistics
:rtype: dictionary
"""


def get_weapon_stats(entity_id):
    result = {}
    if entity_id == EntityID.GUN:
        # DPS: 75
        result["PROJECTILE SPEED"] = 20
        result["SPREAD"] = 0
        result["PROJECTILE TYPE"] = EntityID.FRIENDLY_BULLET
        result["DAMAGE"] = 15
        result["RELOAD"] = 6
        result["PROJECTILE COUNT"] = 1
        result["DPS"] = 75
        result["DESCRIPTION"] = "Fires lethal blasts of plasma in a straight line."
        result["NAME"] = "GUN"
    elif entity_id == EntityID.FLAK_CANNON:
        # DPS: 90
        result["PROJECTILE SPEED"] = 10
        result["SPREAD"] = 25
        result["PROJECTILE TYPE"] = EntityID.FRIENDLY_FLAK
        result["DAMAGE"] = 10
        result["RELOAD"] = 10
        result["PROJECTILE COUNT"] = 3
        result["DPS"] = 90
        result["DESCRIPTION"] = "Fires an array of volatile plasma that detonate near enemies."
        result["NAME"] = "FLAK CANNON"
    elif entity_id == EntityID.MACHINE_GUN:
        # DPS: 80
        result["PROJECTILE SPEED"] = 15
        result["SPREAD"] = 10
        result["PROJECTILE TYPE"] = EntityID.FRIENDLY_BULLET
        result["DAMAGE"] = 8
        result["RELOAD"] = 3
        result["PROJECTILE COUNT"] = 1
        result["DPS"] = 80
        result["DESCRIPTION"] = "Fires an orb of explosive plasma that detonates near enemies."
        result["NAME"] = "MACHINE GUN"
    elif entity_id == EntityID.SHOTGUN:
        # DPS: 120
        result["PROJECTILE SPEED"] = 15
        result["SPREAD"] = 15
        result["PROJECTILE TYPE"] = EntityID.FRIENDLY_BULLET
        result["DAMAGE"] = 5
        result["RELOAD"] = 8
        result["PROJECTILE COUNT"] = 6
        result["DPS"] = 120
        result["DESCRIPTION"] = "Fires an inaccurate spread of plasma rounds."
        result["NAME"] = "SHOTGUN"
    elif entity_id == EntityID.FLAK_GUN:
        # DPS: 48
        result["PROJECTILE SPEED"] = 15
        result["SPREAD"] = 5
        result["PROJECTILE TYPE"] = EntityID.FRIENDLY_FLAK
        result["DAMAGE"] = 12
        result["RELOAD"] = 8
        result["PROJECTILE COUNT"] = 1
        result["DPS"] = 48
        result["DESCRIPTION"] = "Fires an orb of explosive plasma that detonates near enemies."
        result["NAME"] = "FLAK GUN"
    elif entity_id == EntityID.MISSILE_LAUNCHER:
        # DPS: 50
        result["PROJECTILE SPEED"] = 25
        result["SPREAD"] = 0
        result["PROJECTILE TYPE"] = EntityID.FRIENDLY_MISSILE
        result["DAMAGE"] = 25
        result["RELOAD"] = 16
        result["PROJECTILE COUNT"] = 1
        result["DPS"] = 50
        result["DESCRIPTION"] = "Launches a high-velocity plasma missile that homes in on foes."
        result["NAME"] = "MISSILE LAUNCHER"
    elif entity_id == EntityID.MULTI_MISSILE:
        # DPS: 40
        result["PROJECTILE SPEED"] = 18
        result["SPREAD"] = 20
        result["PROJECTILE TYPE"] = EntityID.FRIENDLY_MISSILE
        result["DAMAGE"] = 5
        result["RELOAD"] = 16
        result["PROJECTILE COUNT"] = 4
        result["DPS"] = 40
        result["DESCRIPTION"] = "Launches an array of homing plasma missiles at enemies."
        result["NAME"] = "MISSILE BATTERY"
    elif entity_id == EntityID.BAD_MISSILE_LAUNCHER:
        # DPS: 50
        result["PROJECTILE SPEED"] = 10
        result["SPREAD"] = 45
        result["PROJECTILE TYPE"] = EntityID.BAD_MISSILE
        result["DAMAGE"] = 5
        result["RELOAD"] = 16
        result["PROJECTILE COUNT"] = 5
        result["DPS"] = 50
        result["DESCRIPTION"] = "Creates a burst of compressed plasma shards that track enemies."
        result["NAME"] = "DIAMOND DUST"
    elif entity_id == EntityID.RAILGUN:
        # DPS: 25 - 100+ depending on size of enemy
        result["PROJECTILE SPEED"] = 40
        result["SPREAD"] = 0
        result["PROJECTILE TYPE"] = EntityID.RAILGUN
        result["DAMAGE"] = 25
        result["RELOAD"] = 32
        result["PROJECTILE COUNT"] = 1
        result["DPS"] = (25, 100)
        result["DESCRIPTION"] = "Generates a high-velocity blast of super-compressed plasma."
        result["NAME"] = "RAILGUN"
    return result
