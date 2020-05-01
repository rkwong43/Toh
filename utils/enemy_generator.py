from src.entities.ships.allies.aegis import Aegis
from src.entities.ships.allies.archer import Archer
from src.entities.ships.allies.citadel import Citadel
from src.entities.ships.allies.longsword import Longsword
from src.entities.ships.enemies.arbitrator import Arbitrator
from src.entities.ships.enemies.crucible import Crucible
from src.entities.ships.enemies.despoiler import Despoiler
from src.entities.ships.enemies.judicator import Judicator
from src.entities.ships.enemies.king_mandible import KingMandible
from src.entities.ships.enemies.mandible import Mandible
from src.entities.ships.enemies.mantis import Mantis
from src.entities.ships.enemies.mosquito import Mosquito
from src.entities.ships.enemies.mothership import Mothership
from src.entities.ships.enemies.phantom import Phantom
from src.entities.ships.enemies.queen_mandible import QueenMandible
from src.entities.ships.enemies.seer import Seer
from src.entities.ships.enemies.spectre import Spectre
from src.entities.ships.enemies.subjugator import Subjugator
from src.entities.ships.enemies.terminus import Terminus
from src.entities.ships.enemies.titan import Titan
from src.utils import config
from src.utils.ids.ally_id import AllyID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.player_id import PlayerID

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
