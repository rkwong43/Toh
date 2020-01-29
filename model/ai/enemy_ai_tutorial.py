from src.entities.projectiles.bullet import Bullet
from src.entity_id import EntityID
from src.model.ai.enemy_ai_waves import EnemyWaveAI

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

    def __init__(self, model):
        # Model to work with
        super().__init__(model, EntityID.EASY)
        self.fps = self.model.fps
        self.popup_ticks = 0
        self.popup_duration = self.fps * 3
        self.player_pos = (model.player_ship.x, model.player_ship.y)

    """Represents a tick to keep track of enemy spawning, firing, and movement.
    """

    def tick(self):
        if not self.started:
            self.model.popup_text("COMBAT SIMULATOR INITIATED", -1, -1, 3)
            self.started = True
        self.popup_ticks += 1
        if self.popup_ticks == self.popup_duration and self.continue_tutorial:
            self.tutorial_stage += 1
            self.model.effects = []
            self.advance_tutorial()
        player = self.model.player_ship
        old_pos = self.player_pos
        self.player_pos = (player.x, player.y)
        if self.tutorial_stage == 0 and self.player_pos != old_pos:
            self.tutorial_stage += 1
            self.model.effects = []
            self.advance_tutorial()
        elif self.tutorial_stage == 1 and len(self.model.friendly_projectiles) != 0:
            self.tutorial_stage += 1
            self.model.effects = []
            self.advance_tutorial()
        elif self.tutorial_stage == 2 and len(self.model.enemy_ships) == 0:
            self.tutorial_stage += 1
            self.model.level_up()
            self.model.effects = []
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
        for enemy in self.model.enemy_ships:
            enemy.ticks += 1
            # Provides continuous movement for certain enemies
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

    """Advances the stage of the tutorial this is in.
    """

    def advance_tutorial(self):
        if self.tutorial_stage == 0:
            self.model.popup_text("MOVE USING [WASD] KEYS", -1, -1, 60)
        elif self.tutorial_stage == 1:
            self.model.popup_text("FIRE YOUR WEAPON USING [SPACE]", -1, -1, 60)
        elif self.tutorial_stage == 2:
            self.model.popup_text("ELIMINATE THE ENEMY", -1, -1, 60)
            ship = super().spawn_enemy(EntityID.MANDIBLE)
            ship.hp = 30
        elif self.tutorial_stage == 3:
            self.model.popup_text("LEVELING WILL INCREASE DAMAGE, ", -1, -1, 6)
            self.model.popup_text("FIRING SPEED, HEALTH, AND SHIELD", -1, self.model.height * .6, 6)
            self.popup_duration = self.fps * 6
            self.popup_ticks = 0
        elif self.tutorial_stage == 4:
            self.model.popup_text("SHIELD WILL REGENERATE OVER TIME", -1, -1, 10)
            self.model.popup_text("HEALTH REGENERATES UPON LEVELING", -1, self.model.height * .6, 10)
            flak = Bullet(10, self.player_pos[0], self.player_pos[1], -90, 150, 100, EntityID.ENEMY_FLAK)
            flak2 = Bullet(10, self.player_pos[0], self.player_pos[1], -90, 50, 100, EntityID.ENEMY_FLAK)
            self.model.enemy_projectiles.append(flak)
            self.model.enemy_projectiles.append(flak2)
            self.popup_duration = self.fps * 10
            self.popup_ticks = 0
        elif self.tutorial_stage == 5:
            self.model.level_up()
            self.popup_duration = self.fps * 3
            self.popup_ticks = 0
        elif self.tutorial_stage == 6:
            self.model.popup_text("COMBAT SIMULATOR TERMINATED", -1, -1, 3)
            self.model.popup_text("[ESC] TO PAUSE AND EXIT", -1, self.model.height * .6, 8)

        self.continue_tutorial = True
