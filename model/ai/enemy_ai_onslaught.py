import random

from src.entities.ships.waypoint import Waypoint
from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.utils import config, enemy_generator
from src.utils.ids.ally_id import AllyID
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.player_id import PlayerID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class EnemyOnslaughtAI(EnemyWaveAI):
    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: DifficultyID
    """

    def __init__(self, model, difficulty):
        super().__init__(model, difficulty)
        random.seed()
        # Additional enemies not in Classic
        self._combat_ratings[EnemyID.SPECTRE] = 100
        self._combat_ratings[EnemyID.PHANTOM] = 400
        self._combat_ratings[EnemyID.KING_MANDIBLE] = 1000
        self._combat_ratings[EnemyID.QUEEN_MANDIBLE] = 1000
        self._friendly_spawn_ticks = 0
        self._max_combat_rating += 100
        self._max_combat_rating *= 3
        self._combat_ratio *= 2
        self._buff_enemies()

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        self._friendly_spawn_ticks += 1
        if self._friendly_spawn_ticks >= config.game_fps:
            self._friendly_spawn_ticks = 0
            self.spawn_ally()
        player = self._model.get_player()
        # Makes each enemy tick to fire their weapons
        # Also makes them move
        if player.score >= self._level_up_exp:
            self._model.level_up()
            self._level_up_exp *= 2
        if len(self._model.enemy_ships) == 0:
            # Waiting for next wave:
            if self._wait_for_next_wave():
                self._spawn_enemies()
                self._wave += 1

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def _spawn_enemies(self):
        if self._wave == 0:
            cluster_name = str(random.randint(10, 99))
            self._model.popup_text("APPROACHING ENEMY SUPERCLUSTER-" + cluster_name, 3)
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
            self._model.popup_text("WARNING: HEAVY ENEMY PRESENCE", 3)
        # Doubles the enemies spawned every given number of waves and buffs them
        if self._wave % self._enemy_buff_wave == 0 and self._wave != 0:
            self._buff_enemies()
            self._model.popup_text("WARNING: INCREASING OPPOSITION", 3, y=int(config.display_height * .6))
            self._combat_ratio *= 2

    """Increases the shield stats of most smaller enemies.
    """

    def _buff_enemies(self):
        for k, v in self._stats.items():
            v["SHIELD"] += max(int(v["SHIELD"] // 5), 10)
            v["DAMAGE"] += 1

    """Spawns an ally!
    """

    def spawn_ally(self):
        # 20% chance of spawning small ships randomly
        if random.randint(1, 5) == 5:
            random_ship_quantity = random.randint(1, 4)
            x_posns = []
            for _ in range(random_ship_quantity):
                random_speed = random.randint(5, 10)
                rand_x = 0
                good_x = False
                while not good_x:
                    rand_x = random.randint(0, config.display_width - config.ship_size)
                    try:
                        for posn in x_posns:
                            if posn - config.ship_size < rand_x < posn + config.ship_size:
                                raise ValueError
                    except ValueError:
                        continue
                    good_x = True
                ship_id = PlayerID.CITADEL
                if random.randint(1, 4) == 4:
                    ship_id = PlayerID.AEGIS
                ship = enemy_generator.generate_enemy(ship_id,
                                                      rand_x,
                                                      config.display_height,
                                                      speed=random_speed,
                                                      hp=30,
                                                      shield=30,
                                                      fire_rate=config.game_fps // 2)
                x_posns.append(rand_x)
                ship.set_waypoint(wp=Waypoint(rand_x, -config.display_height))
                self._model.friendly_ships.append(ship)
        # 5% chance of spawning a Longsword
        if random.randint(1, 20) == 20:
            # Only allows 1 on screen at once
            for ship in self._model.friendly_ships:
                if ship.entity_id == AllyID.LONGSWORD:
                    return
            rand_x = random.randint(-config.display_width // 2, config.display_width // 2)
            ship = enemy_generator.generate_enemy(AllyID.LONGSWORD,
                                                  rand_x,
                                                  config.display_height,
                                                  speed=2,
                                                  hp=2000,
                                                  shield=500)
            ship.set_waypoint(wp=Waypoint(rand_x, -config.ship_size * 12))
            self._model.friendly_ships.append(ship)
            self._model.friendly_ships.extend(ship.spawn_turrets())
        # 10% chance of spawning a persistent ally
        if random.randint(1, 10) == 10 and len(self._model.friendly_ships) < 12:
            hp = 50
            rand_x = random.randint(0, config.display_width - config.ship_size)
            ship_id = PlayerID.CITADEL
            if random.randint(1, 4) == 4:
                ship_id = PlayerID.AEGIS
                hp *= 2
            ship = enemy_generator.generate_enemy(ship_id,
                                                  rand_x,
                                                  config.display_height,
                                                  speed=5,
                                                  hp=hp,
                                                  shield=20,
                                                  fire_rate=config.game_fps // 2)
            self._model.friendly_ships.append(ship)
        # 10% chance of spawning an Archer turret
        if random.randint(1, 10) == 10 and len(self._model.friendly_ships) < 12:
            hp = 50
            rand_x = random.randint(0, config.display_width - config.ship_size)
            ship_id = AllyID.ARCHER
            ship = enemy_generator.generate_enemy(ship_id,
                                                  rand_x,
                                                  config.display_height,
                                                  speed=5,
                                                  hp=hp,
                                                  shield=20,
                                                  fire_rate=config.game_fps // 2)
            self._model.friendly_ships.append(ship)
