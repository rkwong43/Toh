

from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.model.stats import ship_stats
from src.utils import config
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
This is the game mode Mandible Madness
"""


class EnemyMandibleMadnessAI(EnemyWaveAI):

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: EntityID
    """

    def __init__(self, model, difficulty):
        self._mandible_stats = ship_stats.stats[EnemyID.MANDIBLE]
        super().__init__(model, difficulty)
        # Ship stats
        # Mandible
        self._mandible_combat_rating = 10
        # These are the default scores for medium difficulty
        # Enemy combat rating is based on their score
        # This is the maximum combat rating currently allowed
        self._max_combat_rating = 10

        # Max number of Mandibles that can be onscreen
        self._max_mandibles = 12

    """Changes the difficulty to the given setting.
    """

    def _change_difficulty(self, difficulty):
        fps = config.game_fps
        if difficulty == DifficultyID.EASY:
            self._fire_rate_range = (fps, fps * 3)
            self._enemy_buff_wave = 6
            self._level_up_exp = 50
            self._max_mandibles = 8
        elif difficulty == DifficultyID.HARD:
            self._max_combat_rating = 30
            self._combat_ratio = 20
            self._buff_enemies()
            self._enemy_buff_wave = 2
            self._fire_rate_range = (fps / 2, fps * 1.5)
            self._wave_rest = 0
            self._max_mandibles = 16

    """Increases the shield stats of most smaller enemies.
    """

    def _buff_enemies(self):
        self._mandible_stats["SHIELD"] += 10
        self._mandible_stats["HP"] += 10

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def _spawn_enemies(self):
        if self._wave == 0:
            self._model.popup_text("OH NO NOT THE MANDIBLES", 3)
        if self._max_combat_rating // 10 >= self._max_mandibles:
            for i in range(self._max_mandibles):
                self.spawn_enemy(ProjectileID.ENEMY_BULLET)
            self._buff_enemies()
        else:
            rating = self._max_combat_rating

            while rating > 0:
                self.spawn_enemy(ProjectileID.ENEMY_BULLET)
                rating -= self._mandible_combat_rating
            self._max_combat_rating += self._combat_ratio
            # Doubles the enemies spawned every few waves and buffs them
        if self._wave % self._enemy_buff_wave == 0 and self._wave != 0:
            self._buff_enemies()
            self._model.popup_text("MORE MANDIBLES APPROACHING", 3)
            self._combat_ratio *= 2
            self._max_mandibles += 2
            self.spawn_enemy(ProjectileID.RAILGUN_BLAST)

    """Spawns a single Mandible.

    :param weapon: given weapon to give the Mandible
    :type weapon: ProjectileID  
    """

    def spawn_enemy(self, entity_id):
        ship = super().spawn_enemy(EnemyID.MANDIBLE)
        if entity_id == ProjectileID.RAILGUN_BLAST:
            ship.hp *= 2
            ship.shield *= 1.5
            ship.projectile_speed *= 2
        ship.score_value = (self._mandible_combat_rating * self._wave) + self._mandible_combat_rating
        ship.projectile_damage += (self._wave // 2)
        ship.projectile_type = entity_id
        self._model.enemy_ships.append(ship)
