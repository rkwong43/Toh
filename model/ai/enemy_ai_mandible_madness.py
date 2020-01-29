import random

from src.entities.ships.enemies.mandible import Mandible
from src.entity_id import EntityID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
This is the game mode Mandible Madness
"""


class EnemyMandibleMadnessAI:
    # Ship stats
    # Mandible
    mandible_stats = {"HP": 10, "SHIELD": 10, "SPEED": 4}
    mandible_combat_rating = 10
    # Initial wave
    wave = 0
    # These are the default scores for medium difficulty
    # Enemy combat rating is based on their score
    # This is the maximum combat rating currently allowed
    max_combat_rating = 10
    # Amount each wave increases the combat ratio
    combat_ratio = 10

    # Seconds between each wave
    wave_rest = 3

    # How often the enemies are buffed
    enemy_buff_wave = 4

    # Level up wave interval:
    level_up_exp = 100
    # Max number of Mandibles that can be onscreen
    max_mandibles = 12

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
        self.fire_rate_range = (fps * .75, fps * 2)
        self.change_difficulty(difficulty)
        self.mandible_stats["SPEED"] *= (32 / fps)

    """Changes the difficulty to the given setting.
    """

    def change_difficulty(self, difficulty):
        fps = self.model.fps
        if difficulty == EntityID.EASY:
            self.fire_rate_range = (fps, fps * 3)
            self.enemy_buff_wave = 6
            self.level_up_exp = 50
            self.max_mandibles = 8
        elif difficulty == EntityID.HARD:
            self.max_combat_rating = 30
            self.combat_ratio = 20
            self.buff_enemies()
            self.enemy_buff_wave = 2
            self.fire_rate_range = (fps / 2, fps * 1.5)
            self.wave_rest = 0
            self.max_mandibles = 16

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
                    self.model.bullet_sound.play()
        if len(self.model.enemy_ships) == 0:
            # Leveling up!
            if self.wait_for_next_wave():
                self.spawn_enemies()

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
        self.mandible_stats["HP"] += 10
        if self.mandible_stats["SPEED"] < 10:
            self.mandible_stats["SPEED"] += 1

    """Spawns enemy ships based on the wave number. Number of enemies spawned increases with higher wave counts.
    """

    def spawn_enemies(self):
        if self.wave == 0:
            self.model.popup_text("OH NO NOT THE MANDIBLES", -1, -1, 3)
        self.wave += 1
        if self.max_combat_rating // 10 >= self.max_mandibles:
            for i in range(self.max_mandibles):
                self.spawn_enemy(EntityID.ENEMY_BULLET)
            self.buff_enemies()
        else:
            rating = self.max_combat_rating

            while rating > 0:
                self.spawn_enemy(EntityID.ENEMY_BULLET)
                rating -= self.mandible_combat_rating
            self.max_combat_rating += self.combat_ratio
            # Doubles the enemies spawned every few waves and buffs them
        if self.wave % self.enemy_buff_wave == 0 and self.wave != 0:
            self.buff_enemies()
            self.model.popup_text("MORE MANDIBLES APPROACHING", -1, -1, 3)
            self.combat_ratio *= 2
            self.max_mandibles += 2
            self.spawn_enemy(EntityID.RAILGUN)

    """Generates a random (x,y) coordinate within the upper half of the screen.
    :returns: an (x,y) position within the upper half of the screen
    :rtype: (int, int)
    """

    def generate_pos(self):
        x = random.randint(self.model.ship_size, self.model.width - self.model.ship_size)
        y = random.randint(0, self.model.height / 3)
        return x, y

    """Spawns a single Mandible.
    
    :param weapon: given weapon to give the Mandible
    :type weapon: EntityID
    """

    def spawn_enemy(self, weapon):
        # Creates a random starting position
        x_pos = random.randint(self.model.ship_size, self.model.width - self.model.ship_size)
        # The final coordinates it moves to
        new_pos = self.generate_pos()
        final_x = new_pos[0]
        final_y = new_pos[1]
        # Sets their fire rate randomly, from .75 seconds to 2 seconds
        fire_rate = random.randint(self.fire_rate_range[0], self.fire_rate_range[1])
        ship = Mandible(self.model.ship_size, x_pos, 0, self.mandible_stats.get("HP"), final_x, final_y,
                        self.mandible_stats.get("SPEED"), fire_rate, self.mandible_stats.get("SHIELD"),
                        True, self.model.fps)
        if weapon == EntityID.RAILGUN:
            ship.hp *= 2
            ship.shield *= 1.5
            ship.projectile_speed *= 2
        ship.score_value = (self.mandible_combat_rating * self.wave) + self.mandible_combat_rating
        ship.projectile_damage += (self.wave // 2)
        ship.projectile_type = weapon
        self.model.enemy_ships.append(ship)
