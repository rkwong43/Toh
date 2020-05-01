from src.model.ai.challenge_template import ChallengeAI
from src.utils import config
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class EnemySpectralAI(ChallengeAI):
    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: DifficultyID
    """

    def __init__(self, model, difficulty):
        enemies_to_spawn = [[EnemyID.SPECTRE],
                            [EnemyID.SPECTRE] * 3,
                            [EnemyID.SPECTRE] * 6,
                            ([EnemyID.SPECTRE] * 4) + [EnemyID.PHANTOM],
                            ([EnemyID.SPECTRE] * 6) + [EnemyID.PHANTOM] * 2,
                            ([EnemyID.SPECTRE] * 8) + [EnemyID.PHANTOM] * 3]
        super().__init__(model, difficulty, enemies_to_spawn, "WARNING: UNKNOWN ENTITIES DETECTED",
                         "FINAL CLUSTER APPROACHING")
        self.time_decay = .99

    """Changes the difficulty to the given setting.
    """

    def _change_difficulty(self, difficulty):
        if difficulty == DifficultyID.EASY:
            self._stats[EnemyID.SPECTRE]["HP"] -= 20
            self.fire_rate = int(config.game_fps * 1.4)
        elif difficulty == DifficultyID.HARD:
            self._stats[EnemyID.SPECTRE]["HP"] += 50
            self.fire_rate = int(config.game_fps * .6)
        self._fire_rate_range = (self.fire_rate, self.fire_rate + self.fire_rate // 2)
