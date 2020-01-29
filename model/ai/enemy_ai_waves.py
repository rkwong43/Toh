import random

from src.entities.ships.enemies.arbitrator import Arbitrator
from src.entities.ships.enemies.crucible import Crucible
from src.entities.ships.enemies.despoiler import Despoiler
from src.entities.ships.enemies.judicator import Judicator
from src.entities.ships.enemies.mandible import Mandible
from src.entities.ships.enemies.mantis import Mantis
from src.entities.ships.enemies.mosquito import Mosquito
from src.entities.ships.enemies.mothership import Mothership
from src.entities.ships.enemies.seer import Seer
from src.entities.ships.enemies.subjugator import Subjugator
from src.entities.ships.enemies.terminus import Terminus
from src.entities.ships.enemies.titan import Titan
from src.entity_id import EntityID
from src.model.stats.ship_stats import get_ship_stats

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class EnemyWaveAI:
    # Ship stats
    # Mandible
    mandible_stats = get_ship_stats(EntityID.MANDIBLE)
    # Mantis
    mantis_stats = get_ship_stats(EntityID.MANTIS)
    # Crucible
    crucible_stats = get_ship_stats(EntityID.CRUCIBLE)
    # Mosquito
    mosquito_stats = get_ship_stats(EntityID.MOSQUITO)
    # Subjugator
    subjugator_stats = get_ship_stats(EntityID.SUBJUGATOR)
    # Seer
    seer_stats = get_ship_stats(EntityID.SEER)
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
    # Stats container:
    stats = {EntityID.MANDIBLE: mandible_stats, EntityID.MANTIS: mantis_stats, EntityID.CRUCIBLE: crucible_stats,
             EntityID.MOSQUITO: mosquito_stats, EntityID.SUBJUGATOR: subjugator_stats, EntityID.ARBITRATOR:
                 arbitrator_stats, EntityID.TERMINUS: terminus_stats, EntityID.SEER: seer_stats, EntityID.MOTHERSHIP:
                 mothership_stats, EntityID.DESPOILER: despoiler_stats, EntityID.JUDICATOR: judicator_stats,
             EntityID.TITAN: titan_stats}
    # Combat ratings:
    combat_ratings = {EntityID.MANDIBLE: 10, EntityID.MANTIS: 40, EntityID.CRUCIBLE: 100, EntityID.MOSQUITO: 30,
                      EntityID.SUBJUGATOR: 60, EntityID.ARBITRATOR: 200, EntityID.TERMINUS: 250, EntityID.SEER: 50,
                      EntityID.DESPOILER: 400, EntityID.MOTHERSHIP: 400, EntityID.JUDICATOR: 300, EntityID.TITAN: 1000}
    # If these ships move again
    mandible_moves_again = False
    mantis_moves_again = False
    # Initial wave
    wave = 0
    # These are the default scores for medium difficulty
    # Enemy combat rating is based on their score
    # This is the maximum combat rating currently allowed
    max_combat_rating = 20
    # Amount each wave increases the combat ratio
    combat_ratio = 10

    # Seconds between each wave
    wave_rest = 3

    # How often the enemies are buffed
    enemy_buff_wave = 25

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
        self.model = model
        self.ticks = 0
        random.seed()
        fps = self.model.fps
        # Range in fire rate for enemies, chosen randomly
        self.fire_rate_range = (int(fps * .75), int(fps * 2))
        self.change_difficulty(difficulty)
        # Adjusts the speed of enemies
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
            self.enemy_buff_wave = 30
            self.level_up_exp = 50
        elif difficulty == EntityID.HARD:
            self.max_combat_rating = 100
            self.combat_ratio = 20
            self.buff_enemies()
            self.enemy_buff_wave = 10
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
        self.mandible_stats["SHIELD"] += 10
        self.mosquito_stats["SHIELD"] += 10
        self.subjugator_stats["SHIELD"] += 10
        self.crucible_stats["SHIELD"] += 10
        self.mantis_stats["SHIELD"] += 10

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def spawn_enemies(self):
        if self.wave == 0:
            self.model.popup_text("WARNING: ENEMIES DETECTED", -1, -1, 3)
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
                if enemy == EntityID.TITAN:
                    self.model.popup_text("WARNING: DEATH IMMINENT", -1, -1, 3)
                rating -= combat_value
                available_enemies.remove(enemy)
                self.spawn_enemy(enemy)
                self.titan_stats["HP"] += 500
            else:
                available_enemies.remove(enemy)
        self.max_combat_rating += self.combat_ratio
        # Changes the AI of the smaller ships after 20 waves
        if 200 - self.combat_ratio < self.max_combat_rating < 200 + self.combat_ratio:
            self.mandible_moves_again = True
            self.mantis_moves_again = True
            self.model.popup_text("WARNING: ENTERING DEEP SPACE", -1, -1, 3)
            # Buffs certain enemies
            self.subjugator_stats["SPEED"] += 1
        elif 400 - self.combat_ratio < self.max_combat_rating < 400 + self.combat_ratio:
            self.model.popup_text("WARNING: DEADLY THREATS DETECTED", -1, -1, 3)
        # Doubles the enemies spawned every given number of waves and buffs them
        if self.wave % self.enemy_buff_wave == 0 and self.wave != 0:
            self.buff_enemies()
            self.model.popup_text("REINFORCEMENTS DETECTED", -1, self.model.height // 3, 3)
            self.combat_ratio *= 2

    """Generates a random (x,y) coordinate within the upper half of the screen.
    :returns: an (x,y) position within the upper half of the screen
    :rtype: (int, int)
    """

    def generate_pos(self):
        x = random.randint(self.model.ship_size, self.model.width - self.model.ship_size)
        y = random.randint(0, self.model.height / 3)
        return x, y

    """Spawns a single enemy ship depending on the given entity ID.
    :param entity_id: ID of the enemy to spawn
    :type entity_id: EntityID
    :returns: the ship spawned
    :rtype: Ship
    """

    def spawn_enemy(self, entity_id):
        enemy_stats = self.stats.get(entity_id)
        # Creates a random starting position
        x_pos = random.randint(self.model.ship_size, self.model.width - self.model.ship_size)
        # The final coordinates it moves to
        new_pos = self.generate_pos()
        final_x = new_pos[0]
        final_y = new_pos[1]
        # Sets their fire rate randomly, from .75 seconds to 2 seconds
        fire_rate = random.randint(self.fire_rate_range[0], self.fire_rate_range[1])
        ship = 0
        # TODO: Parameterize
        if entity_id == EntityID.MANDIBLE:
            ship = Mandible(self.model.ship_size, x_pos, -self.model.ship_size, enemy_stats.get("HP"), final_x, final_y,
                            enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"),
                            self.mandible_moves_again, self.model.fps)
        elif entity_id == EntityID.MANTIS:
            ship = Mantis(self.model.ship_size, x_pos, 0, enemy_stats.get("HP"), x_pos, final_y,
                          enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.mantis_moves_again,
                          self.model.fps)
        elif entity_id == EntityID.CRUCIBLE:
            ship = Crucible(self.model.ship_size, x_pos, 0, enemy_stats.get("HP"), final_x, final_y,
                            enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps)
        elif entity_id == EntityID.MOSQUITO:
            ship = Mosquito(self.model.ship_size, x_pos, 0, enemy_stats.get("HP"), final_x, final_y,
                            enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps)
        elif entity_id == EntityID.SUBJUGATOR:
            ship = Subjugator(self.model.ship_size, x_pos, 0, enemy_stats.get("HP"), final_x, final_y,
                              enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps)
        elif entity_id == EntityID.ARBITRATOR:
            ship = Arbitrator(self.model.ship_size * 1.5, x_pos, -self.model.ship_size * 1.5, enemy_stats.get("HP"),
                              final_x, final_y,
                              enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps)
        elif entity_id == EntityID.TERMINUS:
            ship = Terminus(self.model.ship_size * 1.5, x_pos, -self.model.ship_size * 1.5, enemy_stats.get("HP"),
                            final_x, final_y,
                            enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps,
                            self.model.effects)
        elif entity_id == EntityID.SEER:
            ship = Seer(self.model.ship_size, x_pos, 0, enemy_stats.get("HP"), x_pos, final_y,
                        enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps)
        elif entity_id == EntityID.JUDICATOR:
            ship = Judicator(self.model.ship_size * 1.5, x_pos, -self.model.ship_size * 1.5, enemy_stats.get("HP"),
                             final_x, final_y,
                             enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps,
                             self.model.effects)
        elif entity_id == EntityID.MOTHERSHIP:
            ship = Mothership(self.model.ship_size * 2, x_pos, -self.model.ship_size * 2, enemy_stats.get("HP"),
                              final_x, final_y,
                              enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps, self)
        elif entity_id == EntityID.DESPOILER:
            ship = Despoiler(self.model.ship_size * 2, x_pos, -self.model.ship_size * 2, enemy_stats.get("HP"), final_x,
                             final_y,
                             enemy_stats.get("SPEED"), fire_rate, enemy_stats.get("SHIELD"), self.model.fps)
        elif entity_id == EntityID.TITAN:
            middle_of_screen = (self.model.width - (self.model.ship_size * 8)) // 2
            ship = Titan(self.model.ship_size * 8, middle_of_screen, -self.model.ship_size * 8, enemy_stats.get("HP"),
                         middle_of_screen, -self.model.ship_size * 8, enemy_stats.get("SPEED"),
                         fire_rate, enemy_stats.get("SHIELD"),
                         self.model.fps, self, self.model.effects)
        self.model.enemy_ships.append(ship)
        return ship
