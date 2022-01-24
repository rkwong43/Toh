import random
from model.ai.enemy_ai_waves import EnemyWaveAI
from utils import config
from utils.ids.difficulty_id import DifficultyID
from utils.ids.enemy_id import EnemyID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
Heaven mode is only larger and difficult ships.
"""


class EnemyHeavenAI(EnemyWaveAI):
    # These are the default scores for medium difficulty
    # Enemy combat rating is based on their score

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: EntityID
    """

    def __init__(self, model, difficulty):
        # Model to work with
        super().__init__(model, difficulty)
        # This is the maximum combat rating currently allowed
        self._max_combat_rating = 200
        # Amount each wave increases the combat ratio
        self._combat_ratio = 50

        # How often the enemies are buffed
        self._enemy_buff_wave = 10

        self._combat_ratings = {EnemyID.SPECTRE: 100,
                                EnemyID.ARBITRATOR: 200, EnemyID.TERMINUS: 250, EnemyID.DESPOILER: 400,
                                EnemyID.MOTHERSHIP: 400, EnemyID.JUDICATOR: 300, EnemyID.PHANTOM: 400,
                                EnemyID.TITAN: 1000, EnemyID.KING_MANDIBLE: 1000, EnemyID.QUEEN_MANDIBLE: 1000}

    """Changes the difficulty to the given setting.
    """

    def _change_difficulty(self, difficulty):
        fps = config.game_fps
        if difficulty == DifficultyID.EASY:
            self._fire_rate_range = (fps, fps * 3)
            self._enemy_buff_wave = 15
            self._level_up_exp = 50
            for enemy, values in self._stats.items():
                if enemy != EnemyID.MANDIBLE:
                    values["SHIELD"] -= 50
                    values["HP"] -= 50
        elif difficulty == DifficultyID.HARD:
            self._max_combat_rating = 400
            self._combat_ratio = 100
            self._buff_enemies()
            self._enemy_buff_wave = 5
            self._fire_rate_range = (fps / 2, fps * 1.5)
            self._wave_rest = 0

    """Increases the shield stats of most smaller enemies.
    """

    def _buff_enemies(self):
        for enemy, values in self._stats.items():
            if enemy != EnemyID.MANDIBLE:
                values["HP"] += 100
                values["DAMAGE"] += 1

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def _spawn_enemies(self):
        if self._wave == 0:
            self._model.popup_text("WARNING: ENEMY FLEET DETECTED", 3)
        rating = self._max_combat_rating
        # List of entity IDs of available enemies to grab from
        available_enemies = []
        for enemy, value in self._combat_ratings.items():
            if value <= rating:
                available_enemies.append(enemy)
        while len(available_enemies) > 0:
            # Chooses an EntityID of an enemy to spawn
            chosen = random.randint(0, len(available_enemies) - 1)
            # Subtracts their score from the current combat rating
            enemy = available_enemies[chosen]
            combat_value = self._combat_ratings.get(available_enemies[chosen])
            if combat_value <= rating:
                rating -= combat_value
                if enemy == EnemyID.TITAN:
                    # 20% of spawning a Titan
                    if random.randint(1, 5) != 5:
                        available_enemies.remove(enemy)
                        continue
                    self._model.popup_text("WARNING: DEATH IMMINENT", 3)
                    self._stats[EnemyID.TITAN]["HP"] += 500
                    available_enemies.remove(enemy)
                self.spawn_enemy(enemy)
            else:
                available_enemies.remove(enemy)
        while rating > 0:
            self.spawn_enemy(EnemyID.CRUCIBLE)
            rating -= 50
        self._max_combat_rating += self._combat_ratio
        # Doubles the enemies spawned every given number of waves and buffs them
        if self._wave % self._enemy_buff_wave == 0 and self._wave != 0:
            self._buff_enemies()
            self._model.popup_text("WARNING: ENEMY QUANTITY INCREASED", 3, y=int(config.display_height * .6))
            self._combat_ratio *= 2
