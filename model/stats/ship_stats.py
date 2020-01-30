from src.utils.entity_id import EntityID

"""Returns a dictionary of the given ship's statistics.
:param entity_id: ID of ship
:type entity_id: EntityID
:returns: dictionary of ship statistics
:rtype: dictionary
"""


def get_ship_stats(entity_id):
    result = {}
    if entity_id == EntityID.MANDIBLE:
        result["HP"] = 10
        result["SHIELD"] = 10
        result["SPEED"] = 4
        result["DAMAGE"] = 10
        result["PROJECTILE SPEED"] = 10
        result["SCORE"] = 10
        result["DESCRIPTION"] = "Small multi-purpose vessel equipped with a plasma gun."
    elif entity_id == EntityID.MANTIS:
        result["HP"] = 15
        result["SHIELD"] = 20
        result["SPEED"] = 2
        result["DAMAGE"] = 10
        result["PROJECTILE SPEED"] = 15
        result["SCORE"] = 25
        result["DESCRIPTION"] = "Point-defense turret with a burst laser."
    elif entity_id == EntityID.MOSQUITO:
        # DPS: 80
        result["HP"] = 20
        result["SHIELD"] = 25
        result["SPEED"] = 5
        result["DAMAGE"] = 10
        result["PROJECTILE SPEED"] = 5
        result["SCORE"] = 30
        result["DESCRIPTION"] = "Small and fast fighter with area denial capabilities."
    elif entity_id == EntityID.CRUCIBLE:
        # DPS: 120
        result["HP"] = 60
        result["SHIELD"] = 60
        result["SPEED"] = 4
        result["DAMAGE"] = 10
        result["PROJECTILE SPEED"] = 8
        result["SCORE"] = 100
        result["DESCRIPTION"] = "Fighter with a dual rotary plasma gun designed for combat."
    elif entity_id == EntityID.SEER:
        result["HP"] = 30
        result["SHIELD"] = 50
        result["SPEED"] = 3
        result["DAMAGE"] = 30
        result["PROJECTILE SPEED"] = 40
        result["SCORE"] = 50
        result["DESCRIPTION"] = "Fighter specialized in long-range strikes with a high-powered sniper."
    elif entity_id == EntityID.SUBJUGATOR:
        result["HP"] = 40
        result["SHIELD"] = 40
        result["SPEED"] = 3
        result["DAMAGE"] = 25
        result["PROJECTILE SPEED"] = 10
        result["SCORE"] = 50
        result["DESCRIPTION"] = "Anti-ship fighter that fires homing missiles at its enemies."
    elif entity_id == EntityID.ARBITRATOR:
        result["HP"] = 250
        result["SHIELD"] = 200
        result["SPEED"] = 2
        result["DAMAGE"] = 10
        result["PROJECTILE SPEED"] = 10
        result["SCORE"] = 300
        result["DESCRIPTION"] = "Heavy gunship specialized in suppressing foes."
    elif entity_id == EntityID.TERMINUS:
        result["HP"] = 300
        result["SHIELD"] = 200
        result["SPEED"] = 1
        result["DAMAGE"] = 30
        result["PROJECTILE SPEED"] = 60
        result["SCORE"] = 400
        result["DESCRIPTION"] = "Orbital railgun platform capable of destroying any target."
    elif entity_id == EntityID.JUDICATOR:
        result["HP"] = 200
        result["SHIELD"] = 250
        result["SPEED"] = 1
        result["DAMAGE"] = 5
        result["PROJECTILE SPEED"] = 25
        result["SCORE"] = 350
        result["DESCRIPTION"] = "Heavy gunship mounted with a railgun and diamond dust generator."
    elif entity_id == EntityID.DESPOILER:
        result["HP"] = 450
        result["SHIELD"] = 400
        result["SPEED"] = 3
        result["DAMAGE"] = 6
        result["PROJECTILE SPEED"] = 20
        result["SCORE"] = 600
        result["DESCRIPTION"] = "Gunship designed to take down enemies with a barrage of missiles."
    elif entity_id == EntityID.MOTHERSHIP:
        result["HP"] = 500
        result["SHIELD"] = 500
        result["SPEED"] = 1
        result["DAMAGE"] = 25
        result["PROJECTILE SPEED"] = 10
        result["SCORE"] = 600
        result["DESCRIPTION"] = "Carrier with self-defense missiles designed to transport troops."
    elif entity_id == EntityID.TITAN:
        result["HP"] = 4500
        result["SHIELD"] = 500
        result["SPEED"] = 5
        result["DAMAGE"] = 15
        result["PROJECTILE SPEED"] = 10
        result["SCORE"] = 10000
        result["DESCRIPTION"] = "Calamity-class Warship with multiple turrets and defense systems."

    result["NAME"] = entity_id.name
    return result
