import random

from src.entities.ships.enemies.crucible import Crucible
from src.entities.ships.enemies.mandible import Mandible
from src.entities.ships.enemies.titan import Titan
from src.entity_id import EntityID
from src.model.ai.enemy_ai_waves import EnemyWaveAI

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI where number of enemies are spawned in waves. Defeating a wave will spawn the next one.
"""


class EnemyTitanSlayerAI(EnemyWaveAI):

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    :param difficulty: The difficulty setting
    :type difficulty: EntityID
    """

    def __init__(self, model, difficulty):
        # Model to work with
        super().__init__(model, difficulty)
        fps = self.model.fps
        self.fire_rate = fps * 1.25
        self.change_difficulty(difficulty)
        self.started_game = False

    """Changes the difficulty to the given setting.
    """

    def change_difficulty(self, difficulty):
        fps = self.model.fps
        if difficulty == EntityID.EASY:
            self.titan_stats = {"HP": 3000, "SHIELD": 500, "SPEED": 5}
            self.fire_rate = fps * 2
        elif difficulty == EntityID.HARD:
            self.titan_stats = {"HP": 6000, "SHIELD": 500, "SPEED": 5}
            self.fire_rate = fps * .75

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        if not self.started_game:
            self.spawn_enemy(EntityID.TITAN)
            self.started_game = True
            self.model.popup_text("WARNING: DEATH IMMINENT", -1, -1, 3)
        player = self.model.player_ship
        self.ticks += 1
        # Makes each enemy tick to fire their weapons
        # Also makes them move
        for enemy in self.model.enemy_ships:
            enemy.ticks += 1
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
        if len(self.model.enemy_ships) == 0 and not self.model.game_over:
            victory_time = "VICTORY: " + str(self.ticks // self.model.fps) + " SECONDS"
            self.model.popup_text(victory_time, -1, self.model.height * (2 / 3), 5)
            self.model.game_over = True

    """Spawns a single Titan or Mandible.
    :param entity_id: ID of ship to spawn.
    :returns: the ship spawned
    :rtype: Ship
    """

    """Spawns a single enemy ship depending on the given entity ID
        :param entity_id: ID of the enemy to spawn
        :type entity_id: EntityID
        :returns: the ship spawned
        :rtype: Ship
        """

    def spawn_enemy(self, entity_id):
        # Creates a random starting position
        # The final coordinates it moves to
        new_pos = self.generate_pos()
        final_x = new_pos[0]
        final_y = new_pos[1]
        # Sets their fire rate randomly
        fire_rate = random.randint(int(self.fire_rate), int(self.fire_rate * 1.5))
        ship = None
        # TODO: Parameterize
        if entity_id == EntityID.CRUCIBLE:
            ship = Crucible(self.model.ship_size, 0, -self.model.ship_size, self.crucible_stats.get("HP"), final_x,
                            final_y, self.crucible_stats.get("SPEED"), fire_rate, self.crucible_stats.get("SHIELD"),
                            self.model.fps)

        elif entity_id == EntityID.TITAN:
            middle_of_screen = (self.model.width - (self.model.ship_size * 8)) // 2
            ship = Titan(self.model.ship_size * 8, middle_of_screen, -self.model.ship_size * 8,
                         self.titan_stats.get("HP"),
                         middle_of_screen, -self.model.ship_size * 8, self.titan_stats.get("SPEED"),
                         self.fire_rate, self.titan_stats.get("SHIELD"),
                         self.model.fps, self, self.model.effects)
        self.model.enemy_ships.append(ship)
        return ship
