from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.utils import config
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class ChallengeAI(EnemyWaveAI):
    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: DifficultyID
    :param enemies: The enemies spawned per wave
    :param start_text: Message that pops up at the beginning of the wave
    :type start_text: str
    :param end_text: Message that pops up at the final wave
    :type end_text: str
    """

    def __init__(self, model, difficulty, enemies, start_text, end_text):
        # Model to work with
        self.fire_rate = config.game_fps
        super().__init__(model, difficulty)
        self.started_game = False
        self._enemies = enemies
        self._start_text = start_text
        self._final_wave_text = end_text
        self.cleared = False

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        if not self.started_game:
            self.started_game = True
            self._next_wave()
            self._model.popup_text(self._start_text, 3)
        self._ticks += 1
        if len(self._model.enemy_ships) == 0 and len(self._enemies) == 0 \
                and not self._model.is_game_over():
            self.cleared = True
            victory_time = "VICTORY: " + str(self._ticks // config.game_fps) + " SECONDS"
            self._model.popup_text(victory_time, 5, y=config.display_height * (2 / 3))
            self._model.end_game()
        elif len(self._model.enemy_ships) == 0 and not self._model.is_game_over():
            self._next_wave()

    """Grabs the time.

    :returns: time in seconds
    :rtype: int
    """

    def get_time(self):
        return self._ticks // config.game_fps

    """Starts the current wave!
    """

    def _next_wave(self):
        if len(self._enemies) == 1:
            self._model.popup_text(self._final_wave_text, 3)
        enemies_to_spawn = self._enemies.pop(0)
        for enemy in enemies_to_spawn:
            self.spawn_enemy(enemy)
