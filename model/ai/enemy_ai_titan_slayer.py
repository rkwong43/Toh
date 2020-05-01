
from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.utils import config
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class EnemyTitanSlayerAI(EnemyWaveAI):

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: DifficultyID
    """

    def __init__(self, model, difficulty):
        # Model to work with
        self.fire_rate = config.game_fps
        super().__init__(model, difficulty)
        self.started_game = False
        self.time_decay = .96
        self.cleared = False

    """Changes the difficulty to the given setting.
    """

    def _change_difficulty(self, difficulty):
        if difficulty == DifficultyID.EASY:
            self._stats[EnemyID.TITAN] = {"HP": 3000, "SHIELD": 500, "SPEED": 5}
            self.fire_rate = int(config.game_fps * 1.4)
        elif difficulty == DifficultyID.HARD:
            self._stats[EnemyID.TITAN] = {"HP": 6000, "SHIELD": 500, "SPEED": 5}
            self.fire_rate = int(config.game_fps * .6)
        self._fire_rate_range = (self.fire_rate, self.fire_rate)

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        if not self.started_game:
            self.spawn_enemy(EnemyID.TITAN)
            self.started_game = True
            self._model.popup_text("WARNING: DEATH IMMINENT", 3)
        self._ticks += 1
        if len(self._model.enemy_ships) == 0 and not self._model.is_game_over():
            self.cleared = True
            victory_time = "VICTORY: " + str(self._ticks // config.game_fps) + " SECONDS"
            self._model.popup_text(victory_time, 5, y=config.display_height * (2 / 3))
            self._model.end_game()

    """Grabs the time.
    
    :returns: time in seconds
    :rtype: int
    """
    def get_time(self):
        return self._ticks // config.game_fps
