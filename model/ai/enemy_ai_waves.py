import random

from src.model.stats import ship_stats
from src.utils import config, enemy_generator
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class EnemyWaveAI:
    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: DifficultyID
    """

    def __init__(self, model, difficulty):
        # Combat ratings:
        self._combat_ratings = {EnemyID.MANDIBLE: 10, EnemyID.MANTIS: 40, EnemyID.CRUCIBLE: 100, EnemyID.MOSQUITO: 30,
                                EnemyID.SUBJUGATOR: 60, EnemyID.ARBITRATOR: 200, EnemyID.TERMINUS: 250,
                                EnemyID.SEER: 50,
                                EnemyID.DESPOILER: 400, EnemyID.MOTHERSHIP: 400, EnemyID.JUDICATOR: 300,
                                EnemyID.TITAN: 1000}
        # Initial wave
        self._wave = 0
        # These are the default scores for medium difficulty
        # Enemy combat rating is based on their score
        # This is the maximum combat rating currently allowed
        self._max_combat_rating = 20
        # Amount each wave increases the combat ratio
        self._combat_ratio = 10

        # Seconds between each wave
        self._wave_rest = 3

        # How often the enemies are buffed
        self._enemy_buff_wave = 25

        # Level up wave interval:
        self._level_up_exp = 100
        # Model to work with
        self._model = model
        self._ticks = 0
        random.seed()
        fps = config.game_fps
        # Range in fire rate for enemies, chosen randomly
        self._fire_rate_range = (int(fps * .75), int(fps * 2))
        # Makes a copy of the global stats
        self._stats = self._init_stats()

        self._change_difficulty(difficulty)

    """Changes the difficulty to the given setting.
    """

    def _change_difficulty(self, difficulty):
        fps = config.game_fps
        if difficulty == DifficultyID.EASY:
            self._fire_rate_range = (fps, fps * 3)
            self._enemy_buff_wave = 30
            self._level_up_exp = 50
        elif difficulty == DifficultyID.HARD:
            self._max_combat_rating = 100
            self._combat_ratio = 20
            self._buff_enemies()
            self._enemy_buff_wave = 10
            self._fire_rate_range = (fps / 2, fps * 1.5)
            self._wave_rest = 0

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        player = self._model.get_player()
        # Makes each enemy tick to fire their weapons
        # Also makes them move
        if player.score >= self._level_up_exp:
            self._model.level_up()
            self._level_up_exp *= 2
        for enemy in self._model.enemy_ships:
            enemy.ticks += 1
            # Fires their weapon if their individual tick rate matches their fire rate
            if enemy.ticks == enemy.fire_rate:
                enemy.ticks = 0
                # Fires projectile at player
                if enemy.ready_to_fire:
                    enemy.fire(player, self._model.enemy_projectiles)
                    self._model.play_sound(enemy.projectile_type)
        if len(self._model.enemy_ships) == 0:
            # Waiting for next wave:
            if self._wait_for_next_wave():
                self._spawn_enemies()
                self._wave += 1

    """Waits for the next wave. Returns true if ready.

    :returns: true if next wave is ready
    :rtype: bool
    """

    def _wait_for_next_wave(self):
        self._ticks += 1
        if self._ticks >= self._wave_rest * config.game_fps:
            self._ticks = 0
            return True
        else:
            return False

    """Increases the shield stats of most smaller enemies.
    """

    def _buff_enemies(self):
        self._stats[EnemyID.MANDIBLE]["SHIELD"] += 20
        self._stats[EnemyID.MANTIS]["SHIELD"] += 20
        self._stats[EnemyID.SEER]["SHIELD"] += 20
        self._stats[EnemyID.MOSQUITO]["SHIELD"] += 20
        self._stats[EnemyID.CRUCIBLE]["SHIELD"] += 20

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def _spawn_enemies(self):
        if self._wave == 0:
            self._model.popup_text("WARNING: ENEMIES DETECTED", 3)
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
                # 20% of spawning a Titan
                if enemy == EnemyID.TITAN:
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
            self._model.popup_text("WARNING: INCREASE IN ENEMY STRENGTH", 3, y=int(config.display_height * .6))
            self._combat_ratio *= 2

    """Spawns a single enemy ship depending on the given entity ID.
    :param entity_id: ID of the enemy to spawn
    :type entity_id: EnemyID
    :returns: the ship spawned
    :rtype: Ship
    :raises: ValueError if given entity ID does not correspond to a ship
    """

    def spawn_enemy(self, entity_id):
        enemy_stats = self._stats.get(entity_id)
        # Creates a random starting position
        x_pos = random.randint(config.ship_size, config.display_width - config.ship_size)
        # Sets their fire rate randomly, from .75 seconds to 2 seconds
        fire_rate = random.randint(self._fire_rate_range[0], self._fire_rate_range[1])
        y_pos = -config.ship_size
        if entity_id == EnemyID.TITAN:
            y_pos = -config.ship_size * 8
            x_pos = (config.display_width - (config.ship_size * 8)) // 2

        ship = enemy_generator.generate_enemy(entity_id, x_pos, y_pos, hp=enemy_stats["HP"],
                                              speed=enemy_stats["SPEED"], fire_rate=fire_rate,
                                              shield=enemy_stats["SHIELD"], ai=self, effects=self._model.get_effects())
        self._model.enemy_ships.append(ship)
        if entity_id == EnemyID.TITAN:
            self._model.enemy_ships.extend(ship.spawn_turrets())
        return ship

    """Initializes all stats of enemies and returns a dictionary of their values.

    :returns: Dictionary of enemy stats
    :rtype: {EnemyID, Dictionary}
    """

    def _init_stats(self):
        # Ship stats
        stats = {}
        for enemy in EnemyID:
            stats[enemy] = ship_stats.stats[enemy]
        return stats
