import random

from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.model.stats import ship_stats
from src.utils import config, enemy_generator
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.game_id import GameID
from src.utils.ids.projectile_id import ProjectileID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
This is the game mode Mandible Madness
"""


class EnemyMandibleMadnessAI(EnemyWaveAI):
    # Ship stats
    # Mandible
    _mandible_stats = ship_stats.stats[EnemyID.MANDIBLE]
    _mandible_combat_rating = 10
    # These are the default scores for medium difficulty
    # Enemy combat rating is based on their score
    # This is the maximum combat rating currently allowed
    _max_combat_rating = 10

    # How often the enemies are buffed
    _enemy_buff_wave = 4

    # Max number of Mandibles that can be onscreen
    _max_mandibles = 12

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: EntityID
    """

    def __init__(self, model, difficulty):
        super().__init__(model, difficulty)
        self._change_difficulty(difficulty)

    """Changes the difficulty to the given setting.
    """

    def _change_difficulty(self, difficulty):
        fps = config.game_fps
        if difficulty == GameID.EASY:
            self._fire_rate_range = (fps, fps * 3)
            self._enemy_buff_wave = 6
            self._level_up_exp = 50
            self._max_mandibles = 8
        elif difficulty == GameID.HARD:
            self._max_combat_rating = 30
            self._combat_ratio = 20
            self._buff_enemies()
            self._enemy_buff_wave = 2
            self._fire_rate_range = (fps / 2, fps * 1.5)
            self._wave_rest = 0
            self._max_mandibles = 16

    """Increases the shield stats of most smaller enemies.
    """

    def buff_enemies(self):
        self._mandible_stats["SHIELD"] += 10
        self._mandible_stats["HP"] += 10
        if self._mandible_stats["SPEED"] < 10:
            self._mandible_stats["SPEED"] += 1

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def spawn_enemies(self):
        if self._wave == 0:
            self._model.popup_text("OH NO NOT THE MANDIBLES", -1, -1, 3)
        self._wave += 1
        if self._max_combat_rating // 10 >= self._max_mandibles:
            for i in range(self._max_mandibles):
                self.spawn_enemy(ProjectileID.ENEMY_BULLET)
            self.buff_enemies()
        else:
            rating = self._max_combat_rating

            while rating > 0:
                self.spawn_enemy(ProjectileID.ENEMY_BULLET)
                rating -= self._mandible_combat_rating
            self._max_combat_rating += self._combat_ratio
            # Doubles the enemies spawned every few waves and buffs them
        if self._wave % self._enemy_buff_wave == 0 and self._wave != 0:
            self.buff_enemies()
            self._model.popup_text("MORE MANDIBLES APPROACHING", -1, -1, 3)
            self._combat_ratio *= 2
            self._max_mandibles += 2
            self.spawn_enemy(ProjectileID.RAILGUN_BLAST)

    """Spawns a single Mandible.

    :param weapon: given weapon to give the Mandible
    :type weapon: EntityID
    """

    def spawn_enemy(self, weapon):
        # Creates a random starting position
        x_pos = random.randint(config.ship_size, config.display_width - config.ship_size)
        # The final coordinates it moves to
        # Sets their fire rate randomly, from .75 seconds to 2 seconds
        fire_rate = random.randint(self._fire_rate_range[0], self._fire_rate_range[1])
        ship = enemy_generator.generate_enemy(EnemyID.MANDIBLE, x_pos, -config.ship_size,
                                              hp=self._mandible_stats.get("HP"),
                                              shield=self._mandible_stats.get("SHIELD"),
                                              speed=self._mandible_stats.get("SPEED"),
                                              fire_rate=fire_rate)
        if weapon == ProjectileID.RAILGUN_BLAST:
            ship.hp *= 2
            ship.shield *= 1.5
            ship.projectile_speed *= 2
        ship.score_value = (self._mandible_combat_rating * self._wave) + self._mandible_combat_rating
        ship.projectile_damage += (self._wave // 2)
        ship.projectile_type = weapon
        self._model.enemy_ships.append(ship)
