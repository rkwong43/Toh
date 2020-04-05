from src.entities.projectiles.bullet import Bullet
from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.utils import config
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.projectile_id import ProjectileID

"""Represents the AI model used to control enemies. Works hand in hand with the model.
This is an AI to guide the player along basic controls.
"""


class EnemyTutorialAI(EnemyWaveAI):
    # Tutorial stages
    # Movement
    # Firing
    # Killing an enemy
    # Leveling up
    # Shield/HP
    tutorial_stage = -1
    # Tutorial started?
    started = False
    # Continue tutorial?
    continue_tutorial = True

    """Constructor for the AI. Takes in the model used to run the game.

    :param model: model used to run the game and grab information from
    :type model: Model
    """

    def __init__(self, model, *args):
        # Model to work with
        super().__init__(model, DifficultyID.EASY)
        self.fps = config.game_fps
        self.popup_ticks = 0
        self.popup_duration = self.fps * 3
        self.player_pos = (model.get_player().x, model.get_player().y)

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        if not self.started:
            self._model.popup_text("COMBAT SIMULATOR INITIATED", -1, -1, 3)
            self.started = True
        self.popup_ticks += 1
        if self.popup_ticks == self.popup_duration and self.continue_tutorial:
            self.tutorial_stage += 1
            self._model.clear_popups()
            self.advance_tutorial()
        player = self._model.get_player()
        old_pos = self.player_pos
        self.player_pos = (player.x, player.y)
        if self.tutorial_stage == 0 and self.player_pos != old_pos:
            self.tutorial_stage += 1
            self._model.clear_popups()
            self.advance_tutorial()
        elif self.tutorial_stage == 1 and len(self._model.friendly_projectiles) != 0:
            self.tutorial_stage += 1
            self._model.clear_popups()
            self.advance_tutorial()
        elif self.tutorial_stage == 2 and len(self._model.enemy_ships) == 0:
            self.tutorial_stage += 1
            self._model.level_up()
            self._model.clear_popups()
            self.advance_tutorial()
        elif self.tutorial_stage == 3 and self.popup_ticks >= self.popup_duration:
            self.tutorial_stage += 1
            self.advance_tutorial()
        elif self.tutorial_stage == 4 and self.popup_ticks == self.popup_duration:
            self.tutorial_stage += 1
            self.advance_tutorial()
        elif self.tutorial_stage == 5 and self.popup_ticks == self.popup_duration:
            self.tutorial_stage += 1
            self.advance_tutorial()
        player.recharge_shield()
        for enemy in self._model.enemy_ships:
            enemy.ticks += 1
            # Provides continuous movement for certain enemies
            enemy.move()
            # Fires their weapon if their individual tick rate matches their fire rate
            if enemy.ticks == enemy.fire_rate:
                enemy.ticks = 0
                # Fires projectile at player
                if enemy.ready_to_fire:
                    enemy.fire(player, self._model.enemy_projectiles)
                    self._model.play_sound(enemy.projectile_type)

    """Advances the stage of the tutorial this is in.
    """

    def advance_tutorial(self):
        if self.tutorial_stage == 0:
            self._model.popup_text("MOVE USING [WASD] KEYS", -1, -1, 60)
        elif self.tutorial_stage == 1:
            self._model.popup_text("FIRE YOUR WEAPON USING [SPACE]", -1, -1, 60)
        elif self.tutorial_stage == 2:
            self._model.popup_text("ELIMINATE THE ENEMY", -1, -1, 60)
            ship = super().spawn_enemy(EnemyID.MANDIBLE)
            ship.hp = 30
        elif self.tutorial_stage == 3:
            self._model.popup_text("LEVELING WILL INCREASE DAMAGE, ", -1, -1, 6)
            self._model.popup_text("FIRING SPEED, HEALTH, AND SHIELD", -1, config.display_height * .6, 6)
            self.popup_duration = self.fps * 6
            self.popup_ticks = 0
        elif self.tutorial_stage == 4:
            self._model.popup_text("SHIELD WILL REGENERATE OVER TIME", -1, -1, 10)
            self._model.popup_text("HEALTH REGENERATES UPON LEVELING", -1, config.display_height * .6, 10)
            flak = Bullet(10, self.player_pos[0], self.player_pos[1], -90, 150, ProjectileID.ENEMY_FLAK)
            flak2 = Bullet(10, self.player_pos[0], self.player_pos[1], -90, 50, ProjectileID.ENEMY_FLAK)
            self._model.enemy_projectiles.append(flak)
            self._model.enemy_projectiles.append(flak2)
            self.popup_duration = self.fps * 10
            self.popup_ticks = 0
        elif self.tutorial_stage == 5:
            self._model.level_up()
            self.popup_duration = self.fps * 3
            self.popup_ticks = 0
        elif self.tutorial_stage == 6:
            self._model.popup_text("COMBAT SIMULATOR TERMINATED", -1, -1, 3)
            self._model.popup_text("[ESC] TO PAUSE AND EXIT", -1, config.display_height * .6, 8)
        else:
            raise ValueError("Invalid tutorial stage")

        self.continue_tutorial = True
