import math
import os
import random

import pygame

from src.entities.effects.charge_up import ChargeUp
from src.entities.effects.explosion import Explosion
from src.entities.effects.popup import PopUp
from src.entities.effects.screen_tint import ScreenTint
from src.entities.projectiles.bullet import Bullet
from src.entities.projectiles.diamond_dust import DiamondDust
from src.entities.projectiles.missile import Missile
from src.entities.ships.player import Player
from src.model.ai.enemy_ai_fate import EnemyFateAI
from src.model.ai.enemy_ai_heaven import EnemyHeavenAI
from src.model.ai.enemy_ai_mandible_madness import EnemyMandibleMadnessAI
from src.model.ai.enemy_ai_onslaught import EnemyOnslaughtAI
from src.model.ai.enemy_ai_spectral import EnemySpectralAI
from src.model.ai.enemy_ai_titan_slayer import EnemyTitanSlayerAI
from src.model.ai.enemy_ai_tutorial import EnemyTutorialAI
from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.model.stats import ship_stats, weapon_stats
from src.utils import config, score_storage
from src.utils.direction import Direction
from src.utils.ids.ally_id import AllyID
from src.utils.ids.effect_id import EffectID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.game_id import GameID
from src.utils.ids.gamemode_id import GameModeID
from src.utils.ids.projectile_id import ProjectileID
from src.utils.ids.weapon_id import WeaponID

"""Represents the model that handles controlling the player, firing, enemies, and other game mechanics such as
health, leveling experience, and game events such as spawning more enemies
"""


class Model:
    current_path = os.path.dirname(__file__)  # where this file is located
    outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the Model folder
    resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
    sound_path = os.path.join(resource_path, 'sounds')  # the sounds folder path
    # Time based game modes
    _time_based_game_modes = [GameModeID.TITAN_SLAYER, GameModeID.SPECTRAL, GameModeID.MANDIBLE_MADNESS]
    # Friendly ships
    friendly_ships = []

    """Initializes the model with the width and height of the window and the size of ships

    :param difficulty: Difficulty mode of the AI
    :type difficulty: DifficultyID
    :param game_mode: Game mode to play
    :type game_mode: GameModeID or GameID
    """

    def __init__(self, difficulty, game_mode):
        # Friendly ships
        # Enemy ships
        self.enemy_ships = []
        # Enemy projectiles
        self.enemy_projectiles = []
        # Friendly projectiles
        self.friendly_projectiles = []
        # Effects
        self.effects = []
        """
        Player statistics:
        Speed: projectile movement speed
        Damage: projectile damage
        Count: projectile count aka how many fired per round
        Spread: +- projectile offset from where the player is shooting (angle)
        Type: Type of projectile fired
        Weapon: Current weapon
        DMod: Damage modifier in which the projectile damage is multiplied by
        RMod: Reload modifier in which the weapon reload time is affected by
        """
        self._player_stats = {"SPEED": 10, "DAMAGE": 10, "COUNT": 1, "SPREAD": 0, "TYPE": ProjectileID.FRIENDLY_BULLET,
                              "WEAPON": WeaponID.GUN, "DMOD": 1, "RMOD": 1, "BURSTS": 1}
        # Game over?
        self._game_over = False
        # Initializing the player and its bonuses from ship choice
        self._reload_bonus, self._damage_bonus, self._player_ship = self._init_player(config.player_ship)
        # The current enemy AI module
        self._AI = self._init_enemy_ai(game_mode, difficulty)
        self._game_mode = game_mode
        self._difficulty = difficulty

        # Reload time for the player's weapon, measured in frames
        self._reload_time = 0
        # Current progress until weapon is reloaded
        self._reload = 0

        # Sounds
        self.sounds = {}
        for file_name, volume in {"bullet": .05, "missile": .05, "explosion": .3, "railgun": .5}.items():
            path = os.path.join(self.sound_path, file_name + '_sound.ogg')
            sound = pygame.mixer.Sound(file=path)
            sound.set_volume(volume)
            self.sounds[file_name.upper()] = sound

        # Action queue
        self._queue = []
        # For ships from the menu
        for ship in self.friendly_ships:
            ship.ready_to_fire = True
            ship.ticks = 0

        # Final game stats
        self._final_stats = {"SCORE": 0, "WEAPON": '', "MODE": '', "LEVEL": 1, "ENEMIES SLAIN": 0, "TITANS SLAIN": 0,
                             "SHOTS FIRED": 0, "DAMAGE TAKEN": 0, "HITS TAKEN": 0, "HIGH SCORE": False}

    """Initializes the player's ship.

    :param player_id: The ID of the ship the player chose.
    :type player_id: PlayerID
    :returns: Tuple of reload bonus, damage bonus, and the player ship object
    :rtype: int, int, Player
    """

    def _init_player(self, player_id):
        player_stats = ship_stats.stats[player_id]
        # Bonuses from ship choice
        reload = 1 - (player_stats["RELOAD MODIFIER"] - 1)
        damage = player_stats["DAMAGE MULTIPLIER"]
        player = Player(config.display_width / 2 - config.ship_size / 2, config.display_height / 2, player_stats["HP"],
                        player_stats["SHIELD"], player_id, player_stats["SPEED"])
        return reload, damage, player

    """Initializes the enemy artificial intelligence behavior depending on the given gamemode.
    :param game_mode: Game mode to grab the AI from.
    :type game_mode: EntityID
    :param difficulty: The difficulty of the game
    :type difficulty: EntityID
    :returns: the enemy AI
    :rtype: EnemyAI
    :raises: ValueError if given GameID isn't supported yet
    """

    def _init_enemy_ai(self, game_mode, difficulty):
        AI_modules = {GameModeID.CLASSIC: EnemyWaveAI, GameModeID.MANDIBLE_MADNESS: EnemyMandibleMadnessAI,
                      GameModeID.TITAN_SLAYER: EnemyTitanSlayerAI, GameModeID.HEAVEN: EnemyHeavenAI,
                      GameID.TUTORIAL: EnemyTutorialAI, GameModeID.FATE: EnemyFateAI,
                      GameModeID.ONSLAUGHT: EnemyOnslaughtAI, GameModeID.SPECTRAL: EnemySpectralAI}
        AI = AI_modules[game_mode](self, difficulty)
        return AI

    """Represents a tick in the game. Handles reloads and moves all projectiles and updates the AI module to
    move enemies. Also rotates enemies to face the player.
    """

    def tick(self):
        if not self._game_over:
            # Action queue
            self._queue[:] = [action for action in self._queue if self._process_action(action)]
            # Rotates enemies, recharges their shields, and checks if they're dead
            self.enemy_ships[:] = [enemy for enemy in self.enemy_ships
                                   if not self._process_ship(enemy, self.get_friendlies(), self.enemy_projectiles)]
            self.friendly_ships[:] = [ship for ship in self.friendly_ships
                                      if not self._process_ship(ship, self.enemy_ships, self.friendly_projectiles)]

            self._process_player()
            # Moves all projectiles and filters them if they're offscreen
        self.friendly_projectiles[:] = [projectile for projectile in self.friendly_projectiles
                                        if not self._process_friendly_projectile(projectile)]
        self.enemy_projectiles[:] = [projectile for projectile in self.enemy_projectiles
                                     if not self._process_enemy_projectile(projectile)]

    """Processes the player, checking its health, making the AI tick, and deciding when to end the game.
    """
    def _process_player(self):
        # Processing the player
        if self._player_ship.hp > 0:
            self._AI.tick()
            # Reloads the player's weapon depending on its fire speed
            if self._reload < self._reload_time:
                self._reload += 1
            # Recharges shield for player
            self._player_ship.recharge_shield()
            # If the player is damaged, then plays a screen effect
            if self._player_ship.is_damaged:
                self._play_screen_effect()
            self._player_ship.is_damaged = False
        elif not self._game_over:
            size = self._player_ship.size // 2
            self.effects.append(Explosion(self._player_ship.x + size, self._player_ship.y + size,
                                          EffectID.BLUE_EXPLOSION))
            self._game_over = True
            self.popup_text("Game Over", 4)

    """Processes friendly ships. Also handles their firing and reloads.
    
    :param ship: Friendly ship
    :type ship: Ally
    :param targets: Possible targets for the ship
    :type targets: [Ship]
    :param projectiles: Projectile list to append onto
    :type projectiles: [Projectile]
    :returns: if the ship should be removed or not
    :rtype: bool
    """

    def _process_ship(self, ship, targets, projectiles):
        result = self._is_dead(ship, targets)
        if result:
            return result
        else:
            ship.is_damaged = False
            ship.ticks += 1
            if ship.ticks == ship.fire_rate:
                ship.ticks = 0
                if ship.ready_to_fire:
                    ship.fire(self.find_closest_target(ship, targets), projectiles)
                    self.play_sound(ship.projectile_type)
            return False

    """Processes commands in the queue.
    
    :param action:
    :type action: {str : Direction, str : int}
    """

    def _process_action(self, action):
        commands = {Direction.FIRE: self._projectile_generator}
        action["FRAME"] -= 1
        if action["FRAME"] == 0:
            commands[action["COMMAND"]]()
            return False
        return True

    """Plays the corresponding sound effect for the projectile fired.

    :param entity_id: ID of the projectile
    :type entity_id: ProjectileID
    """

    def play_sound(self, entity_id):
        if entity_id in [ProjectileID.FRIENDLY_FLAK, ProjectileID.FRIENDLY_BULLET,
                         ProjectileID.ENEMY_FLAK, ProjectileID.ENEMY_BULLET, ProjectileID.HOMING_BULLET,
                         ProjectileID.DIAMOND_DUST]:
            self.sounds["BULLET"].play()
        elif entity_id in [ProjectileID.ENEMY_MISSILE, ProjectileID.FRIENDLY_MISSILE]:
            self.sounds["MISSILE"].play()
        elif entity_id in [ProjectileID.RAILGUN_BLAST]:
            self.sounds["RAILGUN"].play()

    """Removes effects that are over.
    """

    def remove_effects(self):
        # Filters the effects for objects to offload
        self.effects[:] = [effect for effect in self.effects if effect.animate()]

    """Determines if the given enemy ship is dead, and adds to the player score if true.

    :param ship: Ship to check if dead
    :type ship: Ship
    :param targets: List of possible targets for the ship
    :type targets: [Ship]
    :returns: if ship is dead
    :rtype: bool
    """

    def _is_dead(self, ship, targets):
        if ship.is_dead:
            # Adds to score if necessary
            if ship.entity_id in EnemyID:
                self._player_ship.score += ship.score
                self._final_stats["ENEMIES SLAIN"] += 1
            self.sounds["EXPLOSION"].play()
            center_x = ship.x + ship.size // 2
            center_y = ship.y + ship.size // 2
            self.effects.append(Explosion(center_x, center_y,
                                          EffectID.EXPLOSION))
            # Clears all if a Titan is killed
            if ship.entity_id == EnemyID.TITAN:
                self.popup_text("TITAN SLAIN", 3)
                self.effects.append(Explosion(ship.x, ship.y, EffectID.TITAN_EXPLOSION))
                self._final_stats["TITANS SLAIN"] += 1
            elif ship.entity_id == AllyID.LONGSWORD:
                self.effects.append(Explosion(ship.x, ship.y, EffectID.TITAN_EXPLOSION))

        else:
            ship.move()
            closest_target = self.find_closest_target(ship, targets)
            ship.rotate(closest_target)
            ship.recharge_shield()
            ship.is_damaged = False
        return ship.is_dead or self._ship_is_off_screen(ship)

    """Moves the player ship and other actions depending on what directions are given.

    :param keys: list of directions to handle
    :type keys: list of Direction
    """

    def move_player(self, keys):
        # Player
        # Firing
        if Direction.FIRE in keys:
            if not self._player_ship.is_dead:
                if self._reload == self._reload_time:
                    self._reload = 0
                    # TODO: Add constant for charge up weapons
                    if self._player_stats["TYPE"] == ProjectileID.RAILGUN_BLAST:
                        self._queue.append({"COMMAND": Direction.FIRE, "FRAME": ChargeUp.charge_delay})
                        charge_effect = ChargeUp(self._player_ship.x + self._player_ship.size // 2,
                                                 self._player_ship.y + self._player_ship.size // 5,
                                                 EffectID.BLUE_CHARGE)
                        self._player_ship.ship_effects.append(charge_effect)
                        self.effects.append(charge_effect)
                    else:
                        for i in range(self._player_stats["BURSTS"]):
                            self._queue.append({"COMMAND": Direction.FIRE, "FRAME": i * 2})
                        self._projectile_generator()
        # Up and down
        size = config.ship_size
        if Direction.UP in keys and self._boundary_check(Direction.UP, size):
            self._player_ship.move_player(Direction.UP)
        elif Direction.DOWN in keys and self._boundary_check(Direction.DOWN, size):
            self._player_ship.move_player(Direction.DOWN)

        # Left and right
        if Direction.LEFT in keys and self._boundary_check(Direction.LEFT, size):
            self._player_ship.move_player(Direction.LEFT)
        elif Direction.RIGHT in keys and self._boundary_check(Direction.RIGHT, size):
            self._player_ship.move_player(Direction.RIGHT)

    """Helper to process ships off screen.
    
    :param ship: Ship
    :type ship: Ship
    :returns: true if the ship is off screen
    :rtype: bool
    """

    def _ship_is_off_screen(self, ship):
        result = self._is_off_screen(ship)
        if result:
            ship.offscreen()
        return result

    """Helper to process projectiles, removing them if they're off screen. Also moves them.
    
    :param projectile: Projectile to move
    :type projectile: Projectile
    :returns: True if the projectile is off screen
    :rtype: bool
    """

    def _process_friendly_projectile(self, projectile):
        projectile.move()
        return self._is_off_screen(projectile) or self._check_if_hit(projectile, self.enemy_ships,
                                                                     EffectID.BLUE_EXPLOSION)

    def _process_enemy_projectile(self, projectile):
        projectile.move()
        return self._is_off_screen(projectile) or self._check_if_hit(projectile, self.get_friendlies(),
                                                                     EffectID.RED_EXPLOSION)

    """Checks if the given entity is off screen.

    :param entity: entity to check
    :type entity: Entity
    """

    def _is_off_screen(self, entity):
        if not entity.remove_if_offscreen:
            return False
        size = entity.size // 2
        center = (entity.x + size, entity.y + size)
        # if off screen:
        x_off = center[0] > config.display_width + size or center[0] < -size
        y_off = center[1] > config.display_height + size or center[1] < -size
        return x_off or y_off

    """Checks whether to remove the projectile.

    :param projectile: Projectile to check
    :type projectile: Projectile
    :param ships: List of ships to check if any were hit
    :type ships: List of Ship
    :param splash_color: color explosion for projectiles to use, also adjusts score of player if blue
    :type splash_color: EntityID
    :returns: True if projectile is to be removed, false otherwise
    :rtype: bool
    """

    def _check_if_hit(self, projectile, ships, splash_color):
        weapon_type = projectile.entity_id
        ship_size = config.ship_size
        radius = projectile.size // 2
        proj_center = (projectile.x + radius, projectile.y + radius)
        if weapon_type == ProjectileID.RAILGUN_BLAST:
            self.effects.append(Explosion(proj_center[0],
                                          proj_center[1],
                                          splash_color))
        elif weapon_type == ProjectileID.FRIENDLY_MISSILE or weapon_type == ProjectileID.ENEMY_MISSILE:
            # Projectile is missile and its target has been destroyed, gives it a new target
            if projectile.target_destroyed:
                projectile.acquire_target(self.find_closest_target(projectile, self.enemy_ships))
        elif weapon_type == ProjectileID.PULSE:
            if projectile.curr_charge != projectile.charge_time:
                return False
            else:
                self.effects.append(Explosion(proj_center[0],
                                              proj_center[1],
                                              splash_color))
                self.sounds["EXPLOSION"].play()
        for ship in ships:
            # Hit box
            ship_bounding_box = ship.size / 4
            # Radius for air burst
            air_burst_distance = projectile.air_burst and self._check_distance(projectile, ship, int(ship_size * .7))
            # Checks if the projectile makes direct contact with the ship or is in air burst range
            if self._check_distance(projectile, ship, ship_bounding_box) or air_burst_distance:
                # Damages the ship
                ship.damage(projectile.damage)
                # Creates an explosion around the projectile
                if projectile.has_splash:
                    # Calculates what ships receive splash damage
                    self._check_splash_damage(projectile, ship, ships)
                    self.effects.append(Explosion(proj_center[0],
                                                  proj_center[1],
                                                  splash_color))
                    self.sounds["EXPLOSION"].play()
                # Removes projectile if it is not a railgun shot
                if projectile.entity_id not in [ProjectileID.RAILGUN_BLAST, ProjectileID.PULSE]:
                    return True
                elif ship.entity_id == EnemyID.TITAN or ship.entity_id == AllyID.LONGSWORD:
                    # Railgun hits larger ship
                    ship.damage(projectile.damage * 4)
                    return True
        return False

    """Plays a particular screen tint effect depending on what damage the player has taken.
    Blue for shield damage, red for health damage.
    """

    def _play_screen_effect(self):
        # PLays a blue or red tint depending on if the player has shield left
        tint = ScreenTint(0, 0, EffectID.SHIELD_TINT) if self._player_ship.shield > 0 else \
            ScreenTint(0, 0, EffectID.HP_TINT)
        # Checks if the current tint is already playing
        # Allows layer of tints for more intensity
        tint_number = 0
        for effect in self.effects:
            if effect.entity_id == tint.entity_id:
                tint_number += 1
        if tint_number <= 6:
            self.effects.append(tint)

    """Checks if the projectile's splash damage collides with any surrounding ships

    :param projectile: projectile to check
    :type projectile: Projectile
    :param ship_to_remove: ship to disregard from the checked list
    :type ship_to_remove: Ship
    :param ships: other ships to check for splash damage
    :type ships: List of Ship
    """

    def _check_splash_damage(self, projectile, ship_to_remove, ships):
        for ship in ships:
            if ship == ship_to_remove:
                continue
            if self._check_distance(projectile, ship, config.ship_size * .75):
                ship.damage(projectile.damage)

    """Checks if the projectile and ship are within a given distance.

    :param projectile: projectile to check
    :type projectile: Projectile
    :param ship: ship to check
    :type ship: Ship
    :param dist: distance
    :type dist: int
    :returns: if the projectile and ship are within the given distance (less than or equal to)
    :rtype: bool
    """

    def _check_distance(self, projectile, ship, dist):
        proj_size = projectile.size / 2
        ship_size = ship.size / 2
        x1 = projectile.x + proj_size
        y1 = projectile.y + proj_size
        x2 = ship.x + ship_size
        y2 = ship.y + ship_size
        distance = int(abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)))
        return distance <= dist

    """Switches the player's weapon to the given type.

    :param weapon: weapon type
    :type weapon: EntityID
    """

    def switch_weapon(self, weapon):
        # Grabs the weapon stats and sets buffer for frame rate
        stats = weapon_stats.stats[weapon] if weapon in WeaponID else weapon
        self._player_stats["SPEED"] = int(stats["PROJECTILE SPEED"] * (30 / config.game_fps))
        self._player_stats["SPREAD"] = stats["SPREAD"]
        self._player_stats["TYPE"] = stats["PROJECTILE TYPE"]
        self._player_stats["DAMAGE"] = int(stats["DAMAGE"] * self._player_stats["DMOD"] * self._damage_bonus)
        self._reload_time = int(stats["RELOAD"] * self._player_stats["RMOD"] *
                                (config.ship_size / 30) * self._reload_bonus)
        self._player_stats["COUNT"] = stats["PROJECTILE COUNT"]
        # Sets the reload times
        if self._reload_time <= 0:
            self._reload_time = 1
        elif self._reload > self._reload_time:
            self._reload = self._reload_time

        self._player_stats["WEAPON"] = weapon

        self._player_stats["BURSTS"] = stats["BURSTS"]

    """Generates projectiles based on the current type and given angle.
    """

    def _projectile_generator(self):
        stats = self._player_stats
        player_angle = self._player_ship.angle
        # Offset and angle partitions based on number of projectiles
        firing_position = self._player_ship.y - config.ship_size / 4
        # Generating the required number of projectiles:
        if stats["COUNT"] > 1:
            partition = int(((2 * stats["SPREAD"]) / (stats["COUNT"] + 1)))
            offset = -stats["SPREAD"] + partition
            for _ in range(stats["COUNT"]):
                projectile = self._generate_projectile(stats["SPEED"], self._player_ship.x, firing_position,
                                                       offset + player_angle,
                                                       stats["DAMAGE"], stats["TYPE"])
                offset += partition
                self.friendly_projectiles.append(projectile)
        else:
            offset = random.randint(-stats["SPREAD"], stats["SPREAD"])
            self.friendly_projectiles.append(
                self._generate_projectile(stats["SPEED"], self._player_ship.x, firing_position, offset + player_angle,
                                          stats["DAMAGE"], stats["TYPE"]))

    """Generates a single projectile and returns it.
    
    :param speed: speed the projectile will move
    :type speed: int
    :param x: starting x position
    :type x: int
    :param y: starting y position
    :type y: int
    :param angle: angle in which it will travel
    :type angle: int
    :param damage: damage it will deal
    :type damage: int
    :param entity_id: ID of the projectile type
    :type entity_id: ProjectileID
    :raises: ValueError if current projectile type is not supported
    """

    def _generate_projectile(self, speed, x, y, angle, damage, entity_id):
        self._final_stats["SHOTS FIRED"] += 1
        self.play_sound(entity_id)
        if entity_id == ProjectileID.FRIENDLY_BULLET or entity_id == ProjectileID.FRIENDLY_FLAK:
            return Bullet(speed, x, y, angle, damage, entity_id)
        elif entity_id == ProjectileID.FRIENDLY_MISSILE:
            closest_enemy = self.find_closest_target(self._player_ship, self.enemy_ships)
            return Missile(speed, x, y, angle, damage, entity_id, closest_enemy)
        elif entity_id == ProjectileID.DIAMOND_DUST:
            closest_enemy = self.find_closest_target(self._player_ship, self.enemy_ships)
            return DiamondDust(speed, x, y, angle, damage, ProjectileID.FRIENDLY_BULLET, closest_enemy)
        elif entity_id == ProjectileID.HOMING_BULLET:
            closest_enemy = self.find_closest_target(self._player_ship, self.enemy_ships)
            return Missile(speed, x, y, angle, damage, ProjectileID.FRIENDLY_BULLET, closest_enemy)
        elif entity_id == ProjectileID.RAILGUN_BLAST:
            return Bullet(speed, x, y, angle, damage, ProjectileID.RAILGUN_BLAST)
        else:
            raise ValueError("Invalid projectile type:", entity_id)

    """Finds the closest ship to the given entity. Used primarily for missile tracking.

    :param source: Source ship or projectile to use as origin
    :type source: Ship or Projectile
    :param ships: Ships to search in
    :type ships: [Ship]
    :returns: closest enemy to the source, or none
    :rtype: Ship or None
    """

    def find_closest_target(self, source, ships):
        x = source.x
        y = source.y
        minimum = config.display_width * 3
        closest_ship = None
        # Iterates through the list of enemy ships linearly and finds the closest one
        # using distance
        for ship in ships:
            ship_x = ship.x
            ship_y = ship.y
            distance = int(abs(math.sqrt((x - ship_x) ** 2 + (y - ship_y) ** 2)))
            if distance <= minimum and not ship.stealth:
                minimum = distance
                closest_ship = ship
        return closest_ship

    """Checks if the player is off screen.

    :param direction: what direction the entity is going to move
    :type direction: Direction
    :param offset: offset of the size to check
    :type offset: int
    :returns: boolean of whether the ship is at the boundary of the screen or not
    :rtype: boolean
    :raises: ValueError if given direction is not valid
    """

    def _boundary_check(self, direction, offset):
        directions = {Direction.UP: lambda entity: entity.y - entity.speed > 0,
                      Direction.DOWN: lambda entity: entity.y + entity.speed < config.display_height - offset,
                      Direction.RIGHT: lambda entity: entity.x + entity.speed < config.display_width - offset,
                      Direction.LEFT: lambda entity: entity.x - entity.speed > 0
                      }
        return directions[direction](self._player_ship)

    """Levels the player up! Modifies the reload and damage modifiers, along with health and shield.
    """

    def level_up(self):
        self._final_stats["LEVEL"] += 1
        player = self._player_ship
        # Increases max HP and restores it
        player.max_hp += 10
        player.hp = player.max_hp
        # Increases max shield and restores it
        player.max_shield += 10
        player.shield_recharge_rate = (player.max_shield // 10 / config.game_fps)
        player.shield = player.max_shield
        # Increases damage and fire rate
        self._player_stats["DMOD"] += .1
        self._player_stats["RMOD"] -= .05
        if self._player_stats["RMOD"] <= 0:
            self._player_stats["RMOD"] -= .1
        self.popup_text("SYSTEM UPGRADED", 3, y=config.display_height // 3)
        # Refreshes the weapon stats for the player
        self.switch_weapon(self._player_stats["WEAPON"])

    """Adds a certain text to play for a certain length of time at the given position.

    :param text: Text to display
    :type text: str
    :param x: x position, if -1, defaults to middle of screen
    :type x: int
    :param y: y position, if -1, defaults to middle of screen
    :type y: int
    :param seconds: how many seconds to show the text for
    :type seconds: int
    """

    def popup_text(self, text, seconds, x=config.display_width // 2, y=config.display_height // 2):
        # Moves the popup down if it is in the same space as another popup
        for effect in self.effects:
            if effect.entity_id == EffectID.POPUP:
                if effect.y == y and effect.text != text:
                    y += config.ship_size
        self.effects.append(PopUp(text, seconds, x, y))

    """Returns all the projectiles in play.

    :returns: list of projectiles in game
    :rtype: list of Projectile
    """

    def get_projectiles(self):
        return self.enemy_projectiles + self.friendly_projectiles

    """Returns all ships excluding the player.
    :returns: list of enemy ships
    :rtype: list of Ship
    """

    def get_ships(self):
        return self.enemy_ships + self.friendly_ships

    """Returns all effects.
    :returns: list of effects
    :rtype: list of Explosion
    """

    def get_effects(self):
        return self.effects

    """Returns the player ship.
    
    :returns: Player
    :rtype: Player
    """

    def get_player(self):
        return self._player_ship

    """Resets the model, emptying all lists of entities other than the player.
    """

    def clear(self):
        del self.enemy_ships[:]
        del self.enemy_projectiles[:]
        del self.friendly_projectiles[:]
        del self.effects[:]
        del self.friendly_ships[:]

    """Pauses the game by displaying a text field and prompt to exit to title screen.
    """

    def pause(self):
        self.clear_popups()
        self.popup_text("PAUSED", 1 / config.game_fps, y=config.display_height // 3)
        self.popup_text("[BACKSPACE] TO RETURN TO TITLE",
                        1 / config.game_fps, y=(config.display_height // 3) + (config.ship_size // 2))

    """Clears all popup texts in the effects.
    """

    def clear_popups(self):
        self.effects[:] = [effect for effect in self.effects if not effect.entity_id == EffectID.POPUP]

    """Is it game over?
    
    :returns: true if the game is over, false otherwise
    :rtype bool:
    """

    def is_game_over(self):
        return self._game_over

    """Ends the game.
    """

    def end_game(self):
        self._game_over = True

    """Returns the dictionary of final stats.
    
    :returns: Dictionary of final stats
    :type: Dictionary
    """

    def get_score(self):
        self.clear()
        # TODO: Future game modes that are time based
        if self._game_mode in self._time_based_game_modes:
            if not self._player_ship.is_dead and len(self.enemy_ships) == 0 and self._AI.cleared:
                # y = 100000 (something less than 1 but close to it)^t
                score = int(self._AI.time_decay ** self._AI.get_time() * 100000)
            else:
                score = 0
        else:
            score = self._player_ship.score
        self._final_stats["MODE"] = self._game_mode.name.replace('_', ' ')
        self._final_stats["WEAPON"] = self._player_stats["WEAPON"].name
        self._final_stats["SCORE"] = score
        self._final_stats["DAMAGE TAKEN"] = int(self._player_ship.damage_taken)
        self._final_stats["HITS TAKEN"] = self._player_ship.hits_taken
        curr_score = score_storage.data["SCORES"][str(self._game_mode.value)][str(self._difficulty.value)]
        if score > curr_score["SCORE"]:
            self._final_stats["HIGH SCORE"] = True
            curr_score["SCORE"] = score
            curr_score["SHIP"] = self._player_ship.entity_id.value
            if self._game_mode != GameModeID.FATE:
                curr_score["WEAPON"] = self._player_stats["WEAPON"].value
            score_storage.save_data()
        return self._final_stats

    """Returns all friendly targets.
    
    :returns: List of friendly targets
    :rtype: [Ship]
    """

    def get_friendlies(self):
        return self.friendly_ships + [self._player_ship]
