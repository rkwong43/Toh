
from src.model.model import Model
from src.utils import config, enemy_generator
from src.utils.ids.difficulty_id import DifficultyID
from src.utils.ids.effect_id import EffectID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.gamemode_id import GameModeID
from src.utils.ids.player_id import PlayerID
from src.utils.ids.weapon_id import WeaponID

"""Represents the model that handles displaying weapons or enemies in a gallery type menu.
"""


class MenuModel(Model):
    # If a weapon or enemy is being showcased
    _showcase_weapon = False
    _showcase_enemy = False

    """Initializes the model with the width and height of the window and the size of ships

    :param width: width of window
    :type width: int
    :param height: height of window
    :type height: int
    :param ship_size: size ships should be scaled to
    :type ship_size: int
    :param fps: frames per second
    :type fps: int
    """

    def __init__(self):
        super().__init__(DifficultyID.EASY, GameModeID.CLASSIC)
        self._player_ship.x = config.display_width
        self._play = False

    """Sets the current playing state.
    
    :param start: True if playing, false otherwise
    :type start: bool
    """
    def set_play(self, start):
        self._play = start

    """Represents a tick in the game. Handles reloads and moves all projectiles and updates the AI module to
    move enemies. Also rotates enemies to face the player.
    """

    def tick(self):
        if self._play:
            # Moves all projectiles
            for projectile in self.friendly_projectiles + self.enemy_projectiles:
                projectile.move()
            # Has enemies immediately fire when ready
            if self._showcase_enemy:
                for ship in self.enemy_ships:
                    ship.move()
                    ship.ticks += 1
                    if ship.ticks == ship.fire_rate:
                        ship.ticks = 0
                        if ship.ready_to_fire:
                            self.play_sound(ship.projectile_type)
                            ship.fire(self._player_ship, self.enemy_projectiles)
            # Reloads the player's weapon depending on its fire speed
            else:
                if self._reload < self._reload_time:
                    self._reload += 1
                elif self._reload == self._reload_time:
                    self._projectile_generator()
                    self._reload = 0
            # Checks collisions between projectiles and ships
            self._remove_off_screen_objects()
            for ship in self.enemy_ships:
                ship.is_damaged = False
            self._player_ship.is_damaged = False
            self._check_collisions()

    """Switches the player's weapon to the given type.

    :param weapon: weapon type
    :type weapon: EntityID
    """

    def switch_weapon(self, weapon):
        super().switch_weapon(weapon)
        if not self._showcase_weapon:
            self._showcase_weapon = True
            self._showcase_enemy = False
        if len(self.enemy_ships) == 0:
            self.clear()
            self._player_stats["DAMAGE"] = 0
            self._player_ship.x = x_pos = config.display_width / 4
            self._player_ship.y = config.display_height * .75
            x_pos -= config.ship_size
            for i in range(3):
                mandible = enemy_generator.generate_enemy(EnemyID.MANDIBLE, x_pos + (i * config.ship_size),
                                                          config.display_height / 3)
                self.enemy_ships.append(mandible)

    """Spawns a ship and places it in a predetermined position.

    :param entity_id: ID of ship to spawn
    :type entity_id: EntityID
    """

    def spawn_ship(self, entity_id):
        if not self._showcase_enemy:
            self._showcase_enemy = True
            self._showcase_weapon = False
        if len(self.enemy_ships) == 0:
            self.clear()
            self._player_ship.x = config.display_width / 4
            self._player_ship.y = config.display_height * .75
            x_pos = config.display_width / 4

            if entity_id in [EnemyID.ARBITRATOR, EnemyID.TERMINUS, EnemyID.JUDICATOR]:
                ship = enemy_generator.generate_enemy(entity_id, x_pos - (config.ship_size // 4),
                                                      config.display_height / 3, effects=self.effects)
            elif entity_id in [EnemyID.MOTHERSHIP, EnemyID.DESPOILER]:
                ship = enemy_generator.generate_enemy(entity_id, x_pos - (config.ship_size // 2),
                                                      config.display_height / 3, effects=self.effects)
            elif entity_id in EnemyID:
                ship = enemy_generator.generate_enemy(entity_id, x_pos, config.display_height / 3)
            else:
                self.spawn_player(entity_id)
                return
            ship.projectile_damage = 0
            self.enemy_ships.append(ship)

    """Renders the player ship.
    :param entity_id: ID of player ship
    :type entity_id: EntityID
    :param x: x position
    :type x: int
    :param y: y position
    :type y: int
    """

    def spawn_player(self, entity_id, x=config.display_width / 4, y=config.display_height / 2):
        self._player_ship.x = x
        self._player_ship.y = y
        self._player_ship.entity_id = entity_id

    """Checks for any projectile collisions between ships and ship collisions. If the ship is destroyed, adds an
       explosion effect to the effects list.
       """

    def _check_collisions(self):
        # Checks friendly projectiles vs. enemy ships
        self.friendly_projectiles[:] = [projectile for projectile in self.friendly_projectiles
                                        if
                                        not self._check_if_hit(projectile, self.enemy_ships, EffectID.BLUE_EXPLOSION)]
        # Checks enemy projectiles vs. friendly ships
        self.enemy_projectiles[:] = [projectile for projectile in self.enemy_projectiles
                                     if not self._check_if_hit(projectile, self.friendly_ships, EffectID.RED_EXPLOSION)]
