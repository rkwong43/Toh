from src.utils.ids.ally_id import AllyID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.player_id import PlayerID

"""Holds the statistics and descriptions of all ships in the game.
"""

stats = {
    EnemyID.MANDIBLE: {"HP": 10, "SHIELD": 10, "SPEED": 4, "DAMAGE": 10, "PROJECTILE SPEED": 10, "SCORE": 10,
                       "DESCRIPTION": "Small multi-purpose vessel equipped with a plasma gun."},
    EnemyID.MANTIS: {"HP": 15, "SHIELD": 20, "SPEED": 2, "DAMAGE": 10, "PROJECTILE SPEED": 15, "SCORE": 25,
                     "DESCRIPTION": "Point-defense turret with a burst laser."},
    EnemyID.MOSQUITO: {"HP": 20, "SHIELD": 25, "SPEED": 5, "DAMAGE": 10, "PROJECTILE SPEED": 5, "SCORE": 30,
                       "DESCRIPTION": "Small and fast fighter with area denial capabilities."},
    EnemyID.CRUCIBLE: {"HP": 60, "SHIELD": 60, "SPEED": 3, "DAMAGE": 10, "PROJECTILE SPEED": 8, "SCORE": 100,
                       "DESCRIPTION": "Fighter with a dual rotary plasma gun designed for combat."},
    EnemyID.SEER: {"HP": 30, "SHIELD": 50, "SPEED": 3, "DAMAGE": 30, "PROJECTILE SPEED": 40, "SCORE": 50,
                   "DESCRIPTION": "Fighter specialized in long-range strikes."},
    EnemyID.SUBJUGATOR: {"HP": 40, "SHIELD": 40, "SPEED": 3, "DAMAGE": 25, "PROJECTILE SPEED": 10, "SCORE": 75,
                         "DESCRIPTION": "Anti-ship fighter that fires homing missiles at its enemies."},
    EnemyID.SPECTRE: {"HP": 100, "SHIELD": 50, "SPEED": 5, "DAMAGE": 15, "PROJECTILE SPEED": 20, "SCORE": 200,
                      "DESCRIPTION": "No information known."},
    EnemyID.ARBITRATOR: {"HP": 250, "SHIELD": 200, "SPEED": 3, "DAMAGE": 10, "PROJECTILE SPEED": 10, "SCORE": 300,
                         "DESCRIPTION": "Heavy gunship specialized in suppressing foes."},
    EnemyID.TERMINUS: {"HP": 300, "SHIELD": 200, "SPEED": 1, "DAMAGE": 30, "PROJECTILE SPEED": 60, "SCORE": 300,
                       "DESCRIPTION": "Orbital railgun platform capable of destroying any target."},
    EnemyID.JUDICATOR: {"HP": 200, "SHIELD": 250, "SPEED": 2, "DAMAGE": 3, "PROJECTILE SPEED": 25, "SCORE": 500,
                        "DESCRIPTION": "Heavy gunship mounted with a railgun and diamond dust generator."},
    EnemyID.DESPOILER: {"HP": 800, "SHIELD": 200, "SPEED": 3, "DAMAGE": 20, "PROJECTILE SPEED": 20, "SCORE": 1000,
                        "DESCRIPTION": "Gunship designed to take down enemies with a barrage of missiles."},
    EnemyID.MOTHERSHIP: {"HP": 1000, "SHIELD": 200, "SPEED": 1, "DAMAGE": 25, "PROJECTILE SPEED": 12, "SCORE": 1000,
                         "DESCRIPTION": "Ship carrier with self-defense missiles."},
    EnemyID.PHANTOM: {"HP": 1000, "SHIELD": 0, "SPEED": 4, "DAMAGE": 40, "PROJECTILE SPEED": 32, "SCORE": 1000,
                      "DESCRIPTION": "Description unavailable."},
    EnemyID.TITAN: {"HP": 4500, "SHIELD": 500, "SPEED": 5, "DAMAGE": 15, "PROJECTILE SPEED": 10, "SCORE": 10000,
                    "DESCRIPTION": "Calamity-class Warship with multiple turrets and defense systems."},
    ##################################################################
    PlayerID.CITADEL: {"HP": 100, "SHIELD": 100, "SPEED": 10, "DAMAGE MULTIPLIER": 1, "RELOAD MODIFIER": 1,
                       "DESCRIPTION": "Versatile ship with a modular weapon system."},
    PlayerID.GHOST: {"HP": 80, "SHIELD": 80, "SPEED": 16, "DAMAGE MULTIPLIER": 1.5, "RELOAD MODIFIER": .8,
                     "DESCRIPTION": "Quick interceptor designed for assassinations."},
    PlayerID.AEGIS: {"HP": 200, "SHIELD": 150, "SPEED": 8, "DAMAGE MULTIPLIER": 1.1, "RELOAD MODIFIER": .9,
                     "DESCRIPTION": "Heavy vanguard warship with increased defenses."},
    PlayerID.STORM: {"HP": 100, "SHIELD": 80, "SPEED": 12, "DAMAGE MULTIPLIER": 1, "RELOAD MODIFIER": 1.2,
                     "DESCRIPTION": "The storm will come."},
    PlayerID.ARCHANGEL: {"HP": 90, "SHIELD": 90, "SPEED": 10, "DAMAGE MULTIPLIER": 1.3, "RELOAD MODIFIER": 1,
                         "DESCRIPTION": "Harbinger of what's yet to come."},
    PlayerID.ORIGIN: {"HP": 50, "SHIELD": 50, "SPEED": 15, "DAMAGE MULTIPLIER": 1.5, "RELOAD MODIFIER": 1.2,
                      "DESCRIPTION": "All shall start anew once again."},
    PlayerID.ETERNITY: {"HP": 120, "SHIELD": 120, "SPEED": 12, "DAMAGE MULTIPLIER": 1.2, "RELOAD MODIFIER": 1.2,
                        "DESCRIPTION": "Its reign shall be eternal."},
    PlayerID.JUDGMENT: {"HP": 150, "SHIELD": 100, "SPEED": 10, "DAMAGE MULTIPLIER": 2, "RELOAD MODIFIER": .7,
                        "DESCRIPTION": "None shall judge."},
    ##################################################################
    AllyID.LONGSWORD: {"HP": 3000, "SHIELD": 2000, "SPEED": 2, "DAMAGE": 25, "PROJECTILE SPEED": 20, "SCORE": 0,
                       "DESCRIPTION": "The vanguard of the crusade."},
    AllyID.ARCHER: {"HP": 50, "SHIELD": 50, "SPEED": 1, "DAMAGE": 8, "PROJECTILE SPEED": 20, "SCORE": 0,
                    "DESCRIPTION": "Anti-ship batteries with dual cannons."}
}
