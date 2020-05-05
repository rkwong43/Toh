from src.model.ai.challenge_template import ChallengeAI
from src.utils import config
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
This is the game mode Mandible Madness.
"""


class EnemyMandibleMadnessAI(ChallengeAI):

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: EntityID
    """

    def __init__(self, model, difficulty):
        enemies_to_spawn = [[EnemyID.MANDIBLE],
                            [EnemyID.MANDIBLE] * 2,
                            [EnemyID.MANDIBLE] * 4,
                            [EnemyID.MANDIBLE] * 8,
                            [EnemyID.MANDIBLE] * 16,
                            [EnemyID.MOTHERSHIP],
                            [EnemyID.MOTHERSHIP] * 2,
                            [EnemyID.MOTHERSHIP] * 3,
                            [EnemyID.KING_MANDIBLE, EnemyID.QUEEN_MANDIBLE] + [EnemyID.MANDIBLE] * 8]
        super().__init__(model, difficulty, enemies_to_spawn, "PREPARE TO ENGAGE SWARM",
                         "DANGER: ROYALS DETECTED")
        self.time_decay = .99

    """Changes the difficulty to the given setting.
    """

    def _change_difficulty(self, difficulty):
        self._stats[EnemyID.MOTHERSHIP]["HP"] //= 2
        if difficulty == DifficultyID.EASY:
            self._stats[EnemyID.MANDIBLE]["HP"] += 10
            self.fire_rate = int(config.game_fps * 1.4)
        elif difficulty == DifficultyID.HARD:
            self._stats[EnemyID.MANDIBLE]["HP"] += 30
            self.fire_rate = int(config.game_fps * .6)
        self._fire_rate_range = (self.fire_rate, self.fire_rate + self.fire_rate // 2)
