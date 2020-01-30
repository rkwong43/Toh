import random
from src.utils.entity_id import EntityID
from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.model.stats.ship_stats import get_ship_stats

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
Heaven mode is only larger and difficult ships.
"""


class EnemyHeavenAI(EnemyWaveAI):
    # Ship stats
    # Default values for hard mode
    # Crucible
    crucible_stats = get_ship_stats(EntityID.CRUCIBLE)
    # Arbitrator
    arbitrator_stats = get_ship_stats(EntityID.ARBITRATOR)
    # Terminus
    terminus_stats = get_ship_stats(EntityID.TERMINUS)
    # Despoiler
    despoiler_stats = get_ship_stats(EntityID.DESPOILER)
    # Mothership
    mothership_stats = get_ship_stats(EntityID.MOTHERSHIP)
    # Judicator
    judicator_stats = get_ship_stats(EntityID.JUDICATOR)
    # Titan
    titan_stats = get_ship_stats(EntityID.TITAN)
    # Mandible
    mandible_stats = get_ship_stats(EntityID.MANDIBLE)
    # Stats container:
    stats = {EntityID.ARBITRATOR: arbitrator_stats, EntityID.TERMINUS: terminus_stats,
             EntityID.MOTHERSHIP: mothership_stats, EntityID.DESPOILER: despoiler_stats,
             EntityID.JUDICATOR: judicator_stats, EntityID.TITAN: titan_stats,
             EntityID.CRUCIBLE: crucible_stats, EntityID.MANDIBLE: mandible_stats}
    # Combat ratings:
    combat_ratings = {EntityID.ARBITRATOR: 200, EntityID.TERMINUS: 250, EntityID.DESPOILER: 400,
                      EntityID.MOTHERSHIP: 400, EntityID.JUDICATOR: 300, EntityID.TITAN: 1000}
    # Initial wave
    wave = 0
    # These are the default scores for medium difficulty
    # Enemy combat rating is based on their score
    # This is the maximum combat rating currently allowed
    max_combat_rating = 200
    # Amount each wave increases the combat ratio
    combat_ratio = 50

    # Seconds between each wave
    wave_rest = 3

    # How often the enemies are buffed
    enemy_buff_wave = 10

    # Level up wave interval:
    level_up_exp = 100

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: EntityID
    """

    def __init__(self, model, difficulty):
        # Model to work with
        super().__init__(model, difficulty)
        self.change_difficulty(difficulty)
        # Adjusts the speed of enemies
        fps = model.fps
        for stats in self.stats.values():
            stats["SPEED"] *= (30 / fps)
            if stats["SPEED"] == 0:
                stats["SPEED"] = 1

    """Changes the difficulty to the given setting.
    """

    def change_difficulty(self, difficulty):
        fps = self.model.fps
        if difficulty == EntityID.EASY:
            self.fire_rate_range = (fps, fps * 3)
            self.enemy_buff_wave = 15
            self.level_up_exp = 50
            for enemy, values in self.stats.items():
                if enemy != EntityID.MANDIBLE:
                    values["SHIELD"] -= 50
                    values["HP"] -= 50
        elif difficulty == EntityID.NORMAL:
            for enemy, values in self.stats.items():
                if enemy != EntityID.MANDIBLE:
                    values["SHIELD"] -= 50
                    values["HP"] -= 50
        elif difficulty == EntityID.HARD:
            self.max_combat_rating = 400
            self.combat_ratio = 100
            self.buff_enemies()
            for enemy, values in self.stats.items():
                if enemy != EntityID.MANDIBLE:
                    values["SHIELD"] += 50
                    values["HP"] += 50
            self.enemy_buff_wave = 5
            self.fire_rate_range = (fps / 2, fps * 1.5)
            self.wave_rest = 0

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        player = self.model.player_ship
        # Makes each enemy tick to fire their weapons
        # Also makes them move
        if player.score >= self.level_up_exp:
            self.model.level_up()
            self.level_up_exp *= 2
        for enemy in self.model.enemy_ships:
            enemy.ticks += 1
            # Provides continuous movement for certain enemies
            if enemy.finished_moving and enemy.move_again:
                # Generates a new position to move to
                new_pos = self.generate_pos()
                enemy.end_x = new_pos[0]
                enemy.end_y = new_pos[1]
                enemy.finished_moving = False
            enemy.move()
            # Fires their weapon if their individual tick rate matches their fire rate
            if enemy.ticks == enemy.fire_rate:
                enemy.ticks = 0
                # Fires projectile at player
                if enemy.ready_to_fire:
                    enemy.fire(player, self.model.enemy_projectiles)
                    if enemy.projectile_type == EntityID.ENEMY_BULLET or enemy.projectile_type == EntityID.ENEMY_FLAK:
                        self.model.bullet_sound.play()
                    elif enemy.projectile_type == EntityID.ENEMY_MISSILE:
                        self.model.missile_sound.play()
                    elif enemy.projectile_type == EntityID.RAILGUN:
                        self.model.railgun_sound.play()
        if len(self.model.enemy_ships) == 0:
            # Leveling up!
            if self.wait_for_next_wave():
                self.spawn_enemies()
                self.wave += 1

    """Waits for the next wave. Returns true if ready.

    :returns: true if next wave is ready
    :rtype: bool
    """

    def wait_for_next_wave(self):
        self.ticks += 1
        if self.ticks >= self.wave_rest * self.model.fps:
            self.ticks = 0
            return True
        else:
            return False

    """Increases the shield stats of most smaller enemies.
    """

    def buff_enemies(self):
        for enemy, values in self.stats.items():
            if enemy != EntityID.MANDIBLE:
                values["SHIELD"] += 50

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def spawn_enemies(self):
        if self.wave == 0:
            self.model.popup_text("WARNING: ENEMY FLEET DETECTED", -1, -1, 3)
        rating = self.max_combat_rating
        # List of entity IDs of available enemies to grab from
        available_enemies = []
        for enemy, value in self.combat_ratings.items():
            if value <= rating:
                available_enemies.append(enemy)
        while len(available_enemies) > 0:
            # Chooses an EntityID of an enemy to spawn
            chosen = random.randint(0, len(available_enemies) - 1)
            # Subtracts their score from the current combat rating
            enemy = available_enemies[chosen]
            combat_value = self.combat_ratings.get(available_enemies[chosen])
            if combat_value <= rating:
                rating -= combat_value
                self.spawn_enemy(enemy)
                if enemy == EntityID.TITAN:
                    self.model.popup_text("WARNING: DEATH IMMINENT", -1, -1, 3)
                    self.titan_stats["HP"] += 500
                    available_enemies.remove(enemy)
            else:
                available_enemies.remove(enemy)
        self.max_combat_rating += self.combat_ratio
        # Doubles the enemies spawned every given number of waves and buffs them
        if self.wave % self.enemy_buff_wave == 0 and self.wave != 0:
            self.buff_enemies()
            self.model.popup_text("REINFORCEMENTS DETECTED", -1, int(self.model.height * .6), 3)
            self.combat_ratio *= 2
