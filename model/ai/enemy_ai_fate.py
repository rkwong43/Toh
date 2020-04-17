import random

from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.utils import config, weapon_generator
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class EnemyFateAI(EnemyWaveAI):
    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: DifficultyID
    """

    def __init__(self, model, difficulty):
        super().__init__(model, difficulty)
        self._weapon_change_wave = 2

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def _spawn_enemies(self):
        if self._wave == 0:
            self._model.popup_text("WARNING: WEAPONS MALFUNCTION", 3)
        if self._wave % self._weapon_change_wave == 0:
            self._model.switch_weapon(weapon_generator.generate_weapon())
            self._model.popup_text("SYSTEM VARIANCE DETECTED", 3)
        rating = self._max_combat_rating
        # List of entity IDs of available enemies to grab from
        available_enemies = []
        for enemy, value in self._combat_ratings.items():
            if value <= rating:
                available_enemies.append(enemy)
        while len(available_enemies) > 0:
            # Chooses an EnemyID of an enemy to spawn
            chosen = random.randint(0, len(available_enemies) - 1)
            # Subtracts their score from the current combat rating
            enemy = available_enemies[chosen]
            combat_value = self._combat_ratings.get(available_enemies[chosen])
            if combat_value <= rating:
                if enemy == EnemyID.TITAN:
                    # 20% of spawning a Titan
                    if random.randint(1, 5) != 5:
                        available_enemies.remove(enemy)
                        continue
                    self._model.popup_text("WARNING: DEATH IMMINENT", 3)
                    self._stats[EnemyID.TITAN]["HP"] += 500
                rating -= combat_value
                available_enemies.remove(enemy)
                self.spawn_enemy(enemy)
            else:
                available_enemies.remove(enemy)
        self._max_combat_rating += self._combat_ratio
        # Changes the AI of the smaller ships after 20 waves
        if 200 - self._combat_ratio < self._max_combat_rating < 200 + self._combat_ratio:
            self._model.popup_text("WARNING: ENTERING DEEP SPACE", 3)
            # Buffs certain enemies
            self._stats[EnemyID.SUBJUGATOR]["SPEED"] += 1
        elif 400 - self._combat_ratio < self._max_combat_rating < 400 + self._combat_ratio:
            self._model.popup_text("WARNING: DEADLY THREATS DETECTED", 3)
        # Doubles the enemies spawned every given number of waves and buffs them
        if self._wave % self._enemy_buff_wave == 0 and self._wave != 0:
            self._buff_enemies()
            self._model.popup_text("WARNING: ENEMIES INCOMING", 3, y=int(config.display_height * .6))
            self._combat_ratio *= 2
