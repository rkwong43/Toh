from entities.ships.allies.aegis import Aegis
from entities.ships.allies.archer import Archer
from entities.ships.allies.citadel import Citadel
from entities.ships.allies.longsword import Longsword
from entities.ships.enemies.arbitrator import Arbitrator
from entities.ships.enemies.crucible import Crucible
from entities.ships.enemies.cyclops import Cyclops
from entities.ships.enemies.despoiler import Despoiler
from entities.ships.enemies.judicator import Judicator
from entities.ships.enemies.king_mandible import KingMandible
from entities.ships.enemies.mandible import Mandible
from entities.ships.enemies.mantis import Mantis
from entities.ships.enemies.mosquito import Mosquito
from entities.ships.enemies.mothership import Mothership
from entities.ships.enemies.phantom import Phantom
from entities.ships.enemies.queen_mandible import QueenMandible
from entities.ships.enemies.seer import Seer
from entities.ships.enemies.spectre import Spectre
from entities.ships.enemies.subjugator import Subjugator
from entities.ships.enemies.terminus import Terminus
from entities.ships.enemies.titan import Titan
from utils import config
from utils.ids.ally_id import AllyID
from utils.ids.enemy_id import EnemyID
from utils.ids.player_id import PlayerID

entities = {EnemyID.MANDIBLE: Mandible,
            EnemyID.MANTIS: Mantis,
            EnemyID.CRUCIBLE: Crucible,
            EnemyID.SUBJUGATOR: Subjugator,
            EnemyID.MOSQUITO: Mosquito,
            EnemyID.SEER: Seer,
            EnemyID.SPECTRE: Spectre,
            EnemyID.ARBITRATOR: Arbitrator,
            EnemyID.TERMINUS: Terminus,
            EnemyID.JUDICATOR: Judicator,
            EnemyID.MOTHERSHIP: Mothership,
            EnemyID.DESPOILER: Despoiler,
            EnemyID.PHANTOM: Phantom,
            EnemyID.TITAN: Titan,
            EnemyID.KING_MANDIBLE: KingMandible,
            EnemyID.QUEEN_MANDIBLE: QueenMandible,
            EnemyID.CYCLOPS: Cyclops,
            PlayerID.CITADEL: Citadel,
            PlayerID.AEGIS: Aegis,
            AllyID.LONGSWORD: Longsword,
            AllyID.ARCHER: Archer
            }

"""Generates the specified enemy and returns it.

:param entity_id: ID of the enemy
:type entity_id: EnemyID
:param x: starting x pos
:type x: int
:param y: starting y pos
:type y: int
:param hp: hit points, default 10000
:type hp: int
:param speed: movement speed, default 0
:type speed: int
:param fire_rate: rate of fire of the enemy, default 0
:type fire_rate: int
:param shield: shield points of enemy, default 0
:type shield: int
"""


def generate_enemy(entity_id, x, y, hp=10000, speed=0, fire_rate=config.game_fps, shield=0, ai=None, effects=None):
    enemy = entities[entity_id](hp, shield, x, y, speed, fire_rate, ai=ai, effects=effects)
    return enemy
