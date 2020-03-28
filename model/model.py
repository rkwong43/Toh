import math
import os
import random

import pygame

from src.entities.effects.explosion import Explosion
from src.entities.effects.popup import PopUp
from src.entities.effects.screen_tint import ScreenTint
from src.entities.projectiles.bullet import Bullet
from src.entities.projectiles.missile import Missile
from src.entities.ships.player import Player
from src.ids.effect_id import EffectID
from src.ids.enemy_id import EnemyID
from src.ids.game_id import GameID
from src.ids.projectile_id import ProjectileID
from src.ids.weapon_id import WeaponID
from src.model.ai.enemy_ai_heaven import EnemyHeavenAI
from src.model.ai.enemy_ai_mandible_madness import EnemyMandibleMadnessAI
from src.model.ai.enemy_ai_titan_slayer import EnemyTitanSlayerAI
from src.model.ai.enemy_ai_tutorial import EnemyTutorialAI
from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.model.stats.ship_stats import get_ship_stats
from src.model.stats.weapon_stats import get_weapon_stats
from src.utils.direction import Direction

"""Represents the model that handles controlling the player, firing, enemies, and other game mechanics such as
health, leveling experience, and game events such as spawning more enemies
"""


# Current
# TODO: Add descriptions to menu
# TODO: REFACTOR EVERYTHING
# TODO: Write player ship choice and high scores to a JSON file?
# TODO: Have a builder for enemy ships?
# TODO: ADD MENU CLICK SOUND
# TODO: ADD MORE GAME MODES AND OPTIONS
# TODO: Maybe a reversal game mode with switched sides?
# TODO: Use profiler to see what's giving the big performance hits


# Future:
# TODO: Spatial partitioning? Quadtrees?
# TODO: Story mode (dialogue etc)
# Story: Arms race, first level enemies do nothing. They steadily arm themselves and develop weapons to fight back
# TODO: Resolution support
# TODO: More enemy types?
# TODO: make your own ship?


# TODO: Maybe if performance suffers, remove shields for enemies

# CURRENT SHIP IDEAS FOR PLAYER
# More HP and Shield, slower movement
# Less HP, faster
# Slower ship, more damage
# Faster ship, less shield, faster fire rate
# less HP and shield, more fire rate and damage
# Increase all stats, very slow movement

class Model:
    # Friendly ships and player
    friendly_ships = []
    # Enemy ships
    enemy_ships = []
    # Enemy projectiles
    enemy_projectiles = []
    # Friendly projectiles
    friendly_projectiles = []
    # Effects
    effects = []

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
    _player_stats = {"SPEED": 10, "DAMAGE": 10, "COUNT": 1, "SPREAD": 0, "TYPE": ProjectileID.FRIENDLY_BULLET,
                     "WEAPON": WeaponID.GUN, "DMOD": 1, "RMOD": 1}
    # Game over?
    game_over = False

    """Initializes the model with the width and height of the window and the size of ships

    :param width: width of window
    :type width: int
    :param height: height of window
    :type height: int
    :param ship_size: size ships should be scaled to
    :type ship_size: int
    :param fps: frames per second
    :type fps: int
    :param weapon_chosen: Starting weapon for the player
    :type weapon_chosen: EntityID
    :param difficulty: Difficulty mode of the AI
    :type difficulty: EntityID
    :param game_mode: Game mode to play
    :type game_mode: EntityID
    """

    def __init__(self, width, height, ship_size, fps, weapon_chosen, difficulty, game_mode, player_id):
        # General parameters
        self.width = width
        self.height = height
        self.ship_size = ship_size
        self.fps = fps
        # Initializing the player and its bonuses from ship choice
        self._reload_bonus, self._damage_bonus, self._player_ship = self._init_player(player_id)
        self.friendly_ships.append(self._player_ship)
        # The current enemy AI module
        self._AI = self._init_enemy_ai(game_mode, difficulty)

        # Reload time for the player's weapon, measured in frames
        self._reload_time = 0
        # Current progress until weapon is reloaded
        self._reload = 0
        self.sounds = self._init_sounds()
        # This sets all the weapon stats
        self.switch_weapon(weapon_chosen)

    """Initializes the player's ship.

    :param player_id: The ID of the ship the player chose.
    :type player_id: PlayerID
    :returns: Tuple of reload bonus, damage bonus, and the player ship object
    :rtype: int, int, Player
    """

    def _init_player(self, player_id):
        player_stats = get_ship_stats(player_id)
        # Bonuses from ship choice
        reload = 1 - (player_stats["RELOAD MODIFIER"] - 1)
        damage = player_stats["DAMAGE MULTIPLIER"]
        player = Player(self.ship_size, self.width / 2 - self.ship_size / 2, self.height / 2, player_stats["HP"],
                        player_stats["SHIELD"], player_id, self.fps, player_stats["SPEED"])
        return reload, damage, player

    """Initializes all the sound effects in the game.

    :returns: dictionary of sound effects
    :rtype: {str: pygame.mixer.Sound}
    """

    def _init_sounds(self):
        sounds = {}
        current_path = os.path.dirname(__file__)  # where this file is located
        outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the Model folder
        resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
        sound_path = os.path.join(resource_path, 'sounds')  # the sounds folder path
        # Sound weapons make when they fire
        path = os.path.join(sound_path, 'bullet_sound.ogg')
        bullet_sound = pygame.mixer.Sound(file=path)
        bullet_sound.set_volume(.05)
        path = os.path.join(sound_path, 'missile_sound.ogg')
        missile_sound = pygame.mixer.Sound(file=path)
        missile_sound.set_volume(.1)
        path = os.path.join(sound_path, 'explosion_sound.ogg')
        explosion_sound = pygame.mixer.Sound(file=path)
        explosion_sound.set_volume(.2)
        path = os.path.join(sound_path, 'railgun_sound.ogg')
        railgun_sound = pygame.mixer.Sound(file=path)
        sounds["BULLET"] = bullet_sound
        sounds["MISSILE"] = missile_sound
        sounds["EXPLOSION"] = explosion_sound
        sounds["RAILGUN"] = railgun_sound
        return sounds

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
        # Using if-else instead of dictionary so each instance isn't
        # instantiated without being used
        if game_mode == GameID.SURVIVAL:
            AI = EnemyWaveAI(self, difficulty)
        elif game_mode == GameID.MANDIBLE_MADNESS:
            AI = EnemyMandibleMadnessAI(self, difficulty)
        elif game_mode == GameID.TITAN_SLAYER:
            AI = EnemyTitanSlayerAI(self, difficulty)
        elif game_mode == GameID.HEAVEN:
            AI = EnemyHeavenAI(self, difficulty)
        elif game_mode == GameID.TUTORIAL:
            AI = EnemyTutorialAI(self)
        else:
            raise ValueError("Given game mode is not supported:", game_mode)
        return AI

    """Represents a tick in the game. Handles reloads and moves all projectiles and updates the AI module to
    move enemies. Also rotates enemies to face the player.
    """

    def tick(self):
        # Moves all projectiles
        for projectile in self.friendly_projectiles + self.enemy_projectiles:
            projectile.move()
        # Reloads the player's weapon depending on its fire speed
        if self._reload < self._reload_time:
            self._reload += 1
        # Rotates enemies, recharges their shields, and checks if they're dead
        self.enemy_ships[:] = [enemy for enemy in self.enemy_ships if not self._is_dead(enemy)]
        self._player_ship.is_damaged = False
        # Removes off screen objects
        self._remove_off_screen_objects()
        if self._player_ship.hp > 0:
            self._AI.tick()
            # Checks collisions between projectiles and ships
            self._check_collisions()
            # Recharges shield for player
            self._player_ship.recharge_shield()

    """Removes effects that are over.
    """

    def remove_effects(self):
        # Filters the effects for objects to offload
        self.effects[:] = [effect for effect in self.effects if effect.animate()]

    """Determines if the given enemy ship is dead, and adds to the player score if true.

    :param ship: Ship to check if dead
    :type ship: Ship
    :returns: if ship is dead
    :rtype: bool
    """

    def _is_dead(self, ship):
        if ship.dead:
            # Adds to score
            self._player_ship.score += ship.score
            self.sounds["EXPLOSION"].play()
            offset = ((self.ship_size * 1.5) - ship.size) // 2
            self.effects.append(Explosion(ship.x - offset, ship.y - offset,
                                          EffectID.EXPLOSION, self.fps))
            # Clears all if a Titan is killed
            if ship.entity_id == EnemyID.TITAN:
                del self.enemy_ships[:]
                self.popup_text("TITAN SLAIN", -1, -1, 3)
                self.effects.append(Explosion(ship.x, ship.y, EffectID.TITAN_EXPLOSION, self.fps))
        else:
            ship.rotate(self._player_ship)
            ship.recharge_shield()
            ship.is_damaged = False
        return ship.is_dead

    """Moves the player ship and other actions depending on what directions are given.

    :param keys: list of directions to handle
    :type keys: list of Direction
    """

    def move_player(self, keys):
        # Player
        # Firing
        if Direction.FIRE in keys:
            if not self._player_ship.dead:
                if self._reload == self._reload_time:
                    self._projectile_generator()
                    self._reload = 0
        # Up and down
        if Direction.UP in keys and self._boundary_check(Direction.UP, self.ship_size):
            self._player_ship.move_player(Direction.UP)
        elif Direction.DOWN in keys and self._boundary_check(Direction.DOWN, self.ship_size):
            self._player_ship.move_player(Direction.DOWN)

        # Left and right
        if Direction.LEFT in keys and self._boundary_check(Direction.LEFT, self.ship_size):
            self._player_ship.move_player(Direction.LEFT)
        elif Direction.RIGHT in keys and self._boundary_check(Direction.RIGHT, self.ship_size):
            self._player_ship.move_player(Direction.RIGHT)

    """Removes all off screen objects such as projectiles or ships.
    """

    def _remove_off_screen_objects(self):
        self.friendly_projectiles[:] = [projectile for projectile in self.friendly_projectiles
                                        if not self._is_off_screen(projectile)]
        self.enemy_projectiles[:] = [projectile for projectile in self.enemy_projectiles
                                     if not self._is_off_screen(projectile)]

    """Checks if the given entity is off screen.

    :param entity: entity to check
    :type entity: Entity
    """

    def _is_off_screen(self, entity):
        size = entity.size / 2
        center = (entity.x + size, entity.y + size)
        # if off screen:
        x_off = center[0] > self.width + size or center[0] < -size
        y_off = center[1] > self.height + size or center[1] < -size
        return x_off or y_off

    """Checks for any projectile collisions between ships and ship collisions. If the ship is destroyed, adds an
    explosion effect to the effects list.
    """

    def _check_collisions(self):
        # TODO: Maybe slice the lists
        # Checks friendly projectiles vs. enemy ships
        self.friendly_projectiles = [projectile for projectile in self.friendly_projectiles
                                     if not self._check_if_hit(projectile, self.enemy_ships, EffectID.BLUE_EXPLOSION)]
        # Checks enemy projectiles vs. friendly ships
        self.enemy_projectiles = [projectile for projectile in self.enemy_projectiles
                                  if not self._check_if_hit(projectile, self.friendly_ships, EffectID.RED_EXPLOSION)]
        # If the player is damaged, then plays a screen effect
        if self._player_ship.isDamaged:
            self._play_screen_effect()

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
        if weapon_type == WeaponID.RAILGUN:
            self.effects.append(Explosion(projectile.x - self.ship_size / 4,
                                          projectile.y - self.ship_size / 4,
                                          splash_color, self.fps))
        elif weapon_type == WeaponID.FRIENDLY_MISSILE:
            # Projectile is missile and its target has been destroyed, gives it a new target
            if projectile.target_destroyed:
                projectile.acquire_target(self._find_closest_enemy(projectile))
        for ship in ships:
            # Hit box
            ship_bounding_box = ship.size / 4
            # Radius for air burst
            air_burst_box = int(self.ship_size * .7)
            air_burst_distance = projectile.air_burst and self._check_distance(projectile, ship, air_burst_box)
            # Checks if the projectile makes direct contact with the ship or is in air burst range
            if self._check_distance(projectile, ship, ship_bounding_box) or air_burst_distance:
                # Damages the ship
                ship.damage(projectile.damage)
                # Creates an explosion around the projectile
                if projectile.has_splash:
                    # Calculates what ships receive splash damage
                    self._check_splash_damage(projectile, ship, ships)
                    self.effects.append(Explosion(projectile.x - (projectile.size // 4),
                                                  projectile.y,
                                                  splash_color, self.fps))
                    self.sounds["EXPLOSION"].play()
                # Removes projectile if it is not a railgun shot
                if projectile.entity_id != ProjectileID.RAILGUN_BLAST:
                    return True
        return False

    """Plays a particular screen tint effect depending on what damage the player has taken.
    Blue for shield damage, red for health damage.
    """

    def _play_screen_effect(self):
        # PLays a blue or red tint depending on if the player has shield left
        tint = ScreenTint(0, 0, EffectID.SHIELD_TINT, self.fps) if self._player_ship.shield > 0 else \
            ScreenTint(0, 0, EffectID.HP_TINT, self.fps)
        # Checks if the current tint is already playing
        # Allows layer of tints for more intensity
        tint_number = 0
        for effect in self.effects:
            if effect.entity_id == tint.entity_id:
                tint_number += 1
        if tint_number <= 6:
            self.effects.append(tint)
        # If the player dies, then game over and returns to title screen (from controller)
        if self._player_ship.dead:
            self.game_over = True
            self.popup_text("Game Over", -1, -1, 4)

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
            if self._check_distance(projectile, ship, self.ship_size * .75):
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
        x1 = projectile.x + (projectile.size / 2)
        y1 = projectile.y + (projectile.size / 2)
        x2 = ship.x + (ship.size / 2)
        y2 = ship.y + (ship.size / 2)
        distance = int(abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)))
        return distance <= dist

    """Switches the player's weapon to the given type.

    :param weapon: weapon type
    :type weapon: EntityID
    """

    def switch_weapon(self, weapon):
        # Grabs the weapon stats and sets buffer for frame rate
        weapon_stats = get_weapon_stats(weapon)
        self._player_stats["SPEED"] = int(weapon_stats["PROJECTILE SPEED"] * (30 / self.fps))
        self._player_stats["SPREAD"] = weapon_stats["SPREAD"]
        self._player_stats["TYPE"] = weapon_stats["PROJECTILE TYPE"]
        self._player_stats["DAMAGE"] = int(weapon_stats["DAMAGE"] * self._player_stats["DMOD"] * self._damage_bonus)
        self._reload_time = int(weapon_stats["RELOAD"] * self._player_stats["RMOD"] *
                                (self.fps / 30) * self._reload_bonus)
        self._player_stats["COUNT"] = weapon_stats["PROJECTILE COUNT"]
        # Sets the reload times
        if self._reload_time <= 0:
            self._reload_time = 1
        if self._reload > self._reload_time:
            self._reload = self._reload_time

        self._player_stats["TYPE"] = weapon

    """Generates projectiles based on the current type and given angle.
    """

    def _projectile_generator(self):
        stats = self._player_stats
        # Offset and angle partitions based on number of projectiles
        partition = ((2 * stats["SPREAD"]) // stats["COUNT"]) + 5
        firing_position = self._player_ship.y - self.ship_size / 4
        # Generating the required number of projectiles:
        for _ in range(stats["COUNT"]):
            offset = random.randint(-stats["SPREAD"], stats["SPREAD"])
            projectile = self._generate_projectile(stats["SPEED"], self._player_ship.x, firing_position, offset + 90,
                                                   stats["DAMAGE"], self.ship_size, stats["TYPE"])
            offset += partition
            self.friendly_projectiles.append(projectile)

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
    :param size: size of the projectile
    :type size: int
    :param entity_id: ID of the projectile type
    :type entity_id: ProjectileID
    :raises: ValueError if current projectile type is not supported
    """

    def _generate_projectile(self, speed, x, y, angle, damage, size, entity_id):
        if entity_id == ProjectileID.FRIENDLY_BULLET or entity_id == ProjectileID.FRIENDLY_FLAK:
            self.sounds["BULLET"].play()
            return Bullet(speed, x, y, angle, damage, size, entity_id)
        elif entity_id == ProjectileID.FRIENDLY_MISSILE:
            self.sounds["MISSILE"].play()
            closest_enemy = self._find_closest_enemy(self._player_ship)
            return Missile(speed, x, y, angle, damage, size, entity_id, self.fps, closest_enemy)
        elif entity_id == ProjectileID.DIAMOND_DUST:
            self.sounds["BULLET"].play()
            closest_enemy = self._find_closest_enemy(self._player_ship)
            return DiamondDust(speed, x, y, angle, damage, size, ProjectileID.FRIENDLY_BULLET, closest_enemy)
        elif entity_id == ProjectileID.HOMING_BULLET:
            self.sounds["BULLET"].play()
            closest_enemy = self._find_closest_enemy(self._player_ship)
            return Missile(speed, x, y, angle, damage, size, ProjectileID.FRIENDLY_BULLET, self.fps, closest_enemy)
        elif entity_id == ProjectileID.RAILGUN_BLAST:
            self.sounds["RAILGUN"].play()
            return Bullet(speed, x, y, angle, damage, size, ProjectileID.RAILGUN_BLAST)
        else:
            raise ValueError("Invalid projectile type:", entity_id)

    """Finds the closest enemy to the given entity. Used primarily for missile tracking.

    :param source: Source ship or projectile to use as origin
    :type source: Ship or Projectile
    :returns: closest enemy to the source, or 0
    :rtype: Ship or int
    """

    def _find_closest_enemy(self, source):
        x = source.x
        y = source.y
        minimum = self.width * 3
        # Sets the first enemy as the closest ship
        if len(self.enemy_ships) > 0:
            closest_enemy = self.enemy_ships[0]
        else:
            return 0
        # Iterates through the list of enemy ships linearly and finds the closest one
        # using distance
        for enemy in self.enemy_ships:
            enemy_x = enemy.x
            enemy_y = enemy.y
            distance = int(abs(math.sqrt((x - enemy_x) ** 2 + (y - enemy_y) ** 2)))
            if distance <= minimum:
                minimum = distance
                closest_enemy = enemy
        return closest_enemy

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
        entity = self._player_ship
        if direction == Direction.UP:
            return entity.y - entity.speed > 0
        elif direction == Direction.DOWN:
            return entity.y + entity.speed < self.height - offset
        elif direction == Direction.RIGHT:
            return entity.x + entity.speed < self.width - offset
        elif direction == Direction.LEFT:
            return entity.x - entity.speed > 0
        else:
            raise ValueError("Given direction is not valid:", direction)

    """Levels the player up! Modifies the reload and damage modifiers, along with health and shield.
    """

    def level_up(self):
        player = self._player_ship
        # Increases max HP and restores it
        player.max_hp += (player.max_hp // 20)
        player.hp = player.max_hp
        # Increases max shield and restores it
        player.max_shield += (player.max_hp // 10)
        player.shield_recharge_rate = (player.max_shield // 20 / self.fps)
        player.shield = player.max_shield
        # Increases damage and fire rate
        self._player_stats["DMOD"] += .2
        self._player_stats["RMOD"] -= .05
        if self._player_stats["RMOD"] <= 0:
            self._player_stats["RMOD"] -= .1
        self.popup_text("Level Up", -1, self.height // 3, 3)
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

    def popup_text(self, text, x, y, seconds):
        if x == -1:
            x = self.width // 2
        if y == -1:
            y = self.height // 2
        # Moves the popup down if it is in the same space as another popup
        for effect in self.effects:
            if effect.entity_id == EffectID.POPUP:
                if effect.y == y and effect.text != text:
                    y += self.ship_size
        self.effects.append(PopUp(text, self.fps, seconds, x, y))

    """Returns all the projectiles in play.

    :returns: list of projectiles in game
    :rtype: list of Projectile
    """

    def get_projectiles(self):
        return self.enemy_projectiles + self.friendly_projectiles

    """Returns all enemy ships.
    :returns: list of enemy ships
    :rtype: list of Ship
    """

    def get_enemies(self):
        return self.enemy_ships

    """Returns all effects.
    :returns: list of effects
    :rtype: list of Explosion
    """

    def get_effects(self):
        return self.effects

    """Resets the model, emptying all lists of entities other than the player.
    """

    def clear(self):
        del self.enemy_ships[:]
        del self.enemy_projectiles[:]
        del self.friendly_projectiles[:]
        del self.effects[:]
        del self.friendly_ships[:]
        self.friendly_ships.append(self._player_ship)

    """Pauses the game by displaying a text field and prompt to exit to title screen.
    """

    def pause(self):
        self.clear_popups()
        self.popup_text("PAUSED", -1, self.height // 3, 1 / self.fps)
        self.popup_text("[BACKSPACE] TO RETURN TO TITLE", -1,
                        (self.height // 3) + (self.ship_size // 2), 1 / self.fps)

    """Clears all popup texts in the effects.
    """

    def clear_popups(self):
        self.effects[:] = [effect for effect in self.effects if not effect.entity_id == EffectID.POPUP]
