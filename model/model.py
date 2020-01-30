import math
import os
import random

import pygame

from src.utils.direction import Direction
from src.entities.effects.popup import PopUp
from src.entities.effects.screen_tint import ScreenTint
from src.entities.projectiles.bad_missile import BadMissile
from src.entities.projectiles.bullet import Bullet
from src.entities.projectiles.missile import Missile
from src.entities.effects.explosion import Explosion
from src.entities.ships.player import Player
from src.utils.entity_id import EntityID
from src.model.ai.enemy_ai_heaven import EnemyHeavenAI
from src.model.ai.enemy_ai_mandible_madness import EnemyMandibleMadnessAI
from src.model.ai.enemy_ai_titan_slayer import EnemyTitanSlayerAI
from src.model.ai.enemy_ai_tutorial import EnemyTutorialAI
from src.model.ai.enemy_ai_waves import EnemyWaveAI
from src.model.stats.weapon_stats import get_weapon_stats

"""Represents the model that handles controlling the player, firing, enemies, and other game mechanics such as
health, leveling experience, and game events such as spawning more enemies
"""


# Steps to add new enemy:
# 1: Create damaged, base, animation, and shield sprites
# 2: Create glow effects for animation and base, overlay (opacity .4)
# 3: Create glow effect for shielding (opacity .4)


# Current
# TODO: different player ship types
# TODO: UNIT TESTING
# TODO: EXCEPTION CHECKING
# TODO: REFACTOR EVERYTHING
# TODO: Write player ship choice and high scores to a JSON file?
# TODO: Have a builder for enemy ships?
# TODO: ADD MENU CLICK SOUND
# TODO: ADD MORE GAME MODES AND OPTIONS
# TODO: Maybe a reversal game mode with switched sides?


# Future:
# TODO: Spatial partitioning?
# TODO: Story mode (dialogue etc)
# Story: Arms race, first level enemies do nothing. They steadily arm themselves and develop weapons to fight back
# TODO: Resolution support
# TODO: More enemy types?
# TODO: make your own ship?


# TODO: Maybe if performance suffers, remove shields for enemies

class Model:
    # Friendly ships and player
    friendly_ships = []
    # Enemy ships
    enemy_ships = []
    # Enemy projectiles
    enemy_projectiles = []
    # Friendly projectiles
    friendly_projectiles = []

    # Default weapon values
    # Bullet speed (base)
    bullet_speed = 10
    # Player's bullet damage
    player_bullet_damage = 10
    # Player's number of projectiles fired
    player_projectile_count = 1
    player_bullet_spread = 0
    player_projectile_type = EntityID.FRIENDLY_BULLET
    player_weapon_type = EntityID.GUN
    # Current damage modifier
    damage_modifier = 1
    # Current reload modifier
    reload_modifier = 1
    # Effects
    effects = []
    # Game over?
    game_over = False
    # Game is paused:
    paused = False

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

    def __init__(self, width, height, ship_size, fps, weapon_chosen, difficulty, game_mode):
        self.width = width
        self.height = height
        self.ship_size = ship_size
        self.ships = []
        self.fps = fps
        self.tick_counter = 0
        # Starts near the bottom center of the screen
        # TODO: Change for new ships
        self.player_ship = Player(ship_size, width / 2 - ship_size / 2, height / 2, 100, 100, EntityID.CITADEL, fps)
        self.friendly_ships.append(self.player_ship)
        # The current enemy AI module
        if game_mode == EntityID.SURVIVAL:
            self.AI = EnemyWaveAI(self, difficulty)
        elif game_mode == EntityID.MANDIBLE_MADNESS:
            self.AI = EnemyMandibleMadnessAI(self, difficulty)
        elif game_mode == EntityID.TITAN_SLAYER:
            self.AI = EnemyTitanSlayerAI(self, difficulty)
        elif game_mode == EntityID.HEAVEN:
            self.AI = EnemyHeavenAI(self, difficulty)
        elif game_mode == EntityID.TUTORIAL:
            self.AI = EnemyTutorialAI(self)
        else:
            raise ValueError("Given game mode is not supported:", game_mode)
        # TODO: ADOPT OTHER GAME MODES

        # Reload time for the player's weapon, measured in frames
        self.max_fire_speed = fps // 5
        # Current progress until weapon is reloaded
        self.reload = self.max_fire_speed

        # Sounds and music
        self.sound = pygame.mixer.init()
        current_path = os.path.dirname(__file__)  # where this file is located
        outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the View folder
        resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
        sound_path = os.path.join(resource_path, 'sounds')  # the sounds folder path
        # Sound weapons make when they fire
        path = os.path.join(sound_path, 'bullet_sound.wav')
        self.bullet_sound = pygame.mixer.Sound(file=path)
        self.bullet_sound.set_volume(.1)
        path = os.path.join(sound_path, 'missile_sound.wav')
        self.missile_sound = pygame.mixer.Sound(file=path)
        self.missile_sound.set_volume(.1)
        path = os.path.join(sound_path, 'explosion_sound.wav')
        self.explosion_sound = pygame.mixer.Sound(file=path)
        path = os.path.join(sound_path, 'railgun_sound.wav')
        self.railgun_sound = pygame.mixer.Sound(file=path)
        self.switch_weapon(weapon_chosen)

    """Represents a tick in the game. Handles reloads and moves all projectiles and updates the AI module to
    move enemies. Also rotates enemies to face the player.
    """

    def tick(self):
        # Moves all projectiles
        for projectile in self.friendly_projectiles + self.enemy_projectiles:
            projectile.move()
        # Reloads the player's weapon depending on its fire speed
        if self.reload < self.max_fire_speed:
            self.reload += 1
        # Rotates enemies, recharges their shields, and checks if they're dead
        self.enemy_ships[:] = [enemy for enemy in self.enemy_ships if not self.is_dead(enemy)]
        self.player_ship.isDamaged = False
        # Checks collisions between projectiles and ships
        # Removes off screen objects
        self.remove_off_screen_objects()
        if not self.player_ship.dead:
            self.AI.tick()
            self.check_collisions()
            # Recharges shield for player
            self.player_ship.recharge_shield()

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

    def is_dead(self, ship):
        if ship.dead:
            # Adds to score
            self.player_ship.score += ship.score
            self.explosion_sound.play()
            offset = ((self.ship_size * 1.5) - ship.size) // 2
            self.effects.append(Explosion(ship.x - offset, ship.y - offset,
                                          EntityID.EXPLOSION, self.fps))
            # Clears all if a Titan is killed
            if ship.entity_id == EntityID.TITAN:
                del self.enemy_ships[:]
                self.popup_text("TITAN SLAIN", -1, -1, 3)
                self.effects.append(Explosion(ship.x, ship.y, EntityID.TITAN_EXPLOSION, self.fps))
        else:
            ship.rotate(self.player_ship)
            ship.recharge_shield()
            ship.isDamaged = False
        return ship.dead

    """Moves the player ship and other actions depending on what directions are given.

    :param keys: list of directions to handle
    :type keys: list of Direction
    """

    def move_player(self, keys):
        # Player
        # Firing
        if Direction.FIRE in keys:
            if not self.player_ship.dead:
                if self.reload == self.max_fire_speed:
                    self.projectile_generator()
                    self.reload = 0
        # Up and down
        if Direction.UP in keys and self.boundary_check(self.player_ship, Direction.UP, self.ship_size):
            self.player_ship.move_player(Direction.UP)
        elif Direction.DOWN in keys and self.boundary_check(self.player_ship, Direction.DOWN, self.ship_size):
            self.player_ship.move_player(Direction.DOWN)

        # Left and right
        if Direction.LEFT in keys and self.boundary_check(self.player_ship, Direction.LEFT, self.ship_size):
            self.player_ship.move_player(Direction.LEFT)
        elif Direction.RIGHT in keys and self.boundary_check(self.player_ship, Direction.RIGHT, self.ship_size):
            self.player_ship.move_player(Direction.RIGHT)

    """Removes all off screen objects such as projectiles or ships.
    """

    def remove_off_screen_objects(self):
        self.friendly_projectiles[:] = [projectile for projectile in self.friendly_projectiles
                                        if not self.is_off_screen(projectile)]
        self.enemy_projectiles[:] = [projectile for projectile in self.enemy_projectiles
                                     if not self.is_off_screen(projectile)]

    """Removes off screen objects in the given list.
    
    :param entity: entity to check
    :type entity: Entity
    """

    def is_off_screen(self, entity):
        size = entity.size / 2
        center = (entity.x + size, entity.y + size)
        # if off screen:
        x_off = center[0] > self.width + size or center[0] < -size
        y_off = center[1] > self.height + size or center[1] < -size
        return x_off or y_off

    """Checks for any projectile collisions between ships and ship collisions. If the ship is destroyed, adds an
    explosion effect to the effects list.
    """

    def check_collisions(self):
        # TODO: Spatial partitioning?
        # Checks friendly projectiles vs. enemy ships
        self.friendly_projectiles[:] = [projectile for projectile in self.friendly_projectiles
                                        if not self.check_if_hit(projectile, self.enemy_ships, EntityID.BLUE_EXPLOSION)]
        # Checks enemy projectiles vs. friendly ships
        self.enemy_projectiles[:] = [projectile for projectile in self.enemy_projectiles
                                     if not self.check_if_hit(projectile, self.friendly_ships, EntityID.RED_EXPLOSION)]
        # If the player is damaged, then plays a screen effect
        if self.player_ship.isDamaged:
            self.play_screen_effect()

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

    def check_if_hit(self, projectile, ships, splash_color):
        weapon_type = projectile.entity_id
        if weapon_type == EntityID.RAILGUN:
            self.effects.append(Explosion(projectile.x - self.ship_size / 4,
                                          projectile.y - self.ship_size / 4,
                                          splash_color, self.fps))
        elif weapon_type == EntityID.FRIENDLY_MISSILE:
            # Projectile is missile and its target has been destroyed, gives it a new target
            if projectile.target_destroyed:
                projectile.acquire_target(self.find_closest_enemy(projectile))
        for ship in ships:
            # Hit box
            ship_bounding_box = ship.size / 4
            # Radius for air burst
            air_burst_box = int(self.ship_size * .7)
            air_burst_distance = projectile.air_burst and self.check_distance(projectile, ship, air_burst_box)
            # Checks if the projectile makes direct contact with the ship or is in air burst range
            if self.check_distance(projectile, ship, ship_bounding_box) or air_burst_distance:
                # Damages the ship
                ship.damage(projectile.damage)
                # Creates an explosion around the projectile
                if projectile.has_splash:
                    # Calculates what ships receive splash damage
                    self.check_splash_damage(projectile, ship, ships)
                    self.effects.append(Explosion(projectile.x - (projectile.size // 4),
                                                  projectile.y,
                                                  splash_color, self.fps))
                    self.explosion_sound.play()
                # Removes projectile if it is not a railgun shot
                if projectile.entity_id != EntityID.RAILGUN:
                    return True
        return False

    """Plays a particular screen tint effect depending on what damage the player has taken.
    Blue for shield damage, red for health damage.
    """

    def play_screen_effect(self):
        # PLays a blue tint
        if self.player_ship.shield > 0:
            tint = ScreenTint(0, 0, EntityID.SHIELD_TINT, self.fps)
        else:
            # Plays a red tint
            tint = ScreenTint(0, 0, EntityID.HP_TINT, self.fps)
        # Checks if the current tint is already playing
        tint_number = 0
        for effect in self.effects:
            if effect.entity_id == tint.entity_id:
                tint_number += 1
        if tint_number <= 8:
            self.effects.append(tint)
        # If the player dies, then game over and returns to title screen (from controller)
        if self.player_ship.dead:
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

    def check_splash_damage(self, projectile, ship_to_remove, ships):
        for ship in ships:
            if ship == ship_to_remove:
                continue
            if self.check_distance(projectile, ship, self.ship_size * .75):
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

    def check_distance(self, projectile, ship, dist):
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
        self.bullet_speed = int(weapon_stats["PROJECTILE SPEED"] * (30 / self.fps))
        self.player_bullet_spread = weapon_stats["SPREAD"]
        self.player_projectile_type = weapon_stats["PROJECTILE TYPE"]
        self.player_bullet_damage = int(weapon_stats["DAMAGE"] * self.damage_modifier)
        self.max_fire_speed = int(weapon_stats["RELOAD"] * self.reload_modifier * (self.fps / 30))
        self.player_projectile_count = weapon_stats["PROJECTILE COUNT"]
        # Sets the reload times
        if self.max_fire_speed <= 0:
            self.max_fire_speed = 1
        if self.reload > self.max_fire_speed:
            self.reload = self.max_fire_speed

        self.player_weapon_type = weapon

    """Generates a projectile based on the current type and given angle.
    
    :raises: ValueError if current projectile type is not supported
    """

    def projectile_generator(self):
        # Offset and angle partitions based on number of projectiles
        partition = ((2 * self.player_bullet_spread) // self.player_projectile_count) + 5
        offset = -self.player_bullet_spread
        firing_position = self.player_ship.y - self.ship_size / 4
        # Standard bullet
        if self.player_projectile_type == EntityID.FRIENDLY_BULLET:
            # Bullet starts at 3/4 of the ship sprite
            for x in range(self.player_projectile_count):
                offset = random.randint(-self.player_bullet_spread, self.player_bullet_spread)
                bullet = Bullet(self.bullet_speed, self.player_ship.x, firing_position,
                                offset + 90, self.player_bullet_damage, self.ship_size,
                                EntityID.FRIENDLY_BULLET)
                self.friendly_projectiles.append(bullet)
            # PLays the bullet sound
            self.bullet_sound.play()
        # Flak shells
        elif self.player_projectile_type == EntityID.FRIENDLY_FLAK:
            # Bullet starts at 3/4 of the ship sprite
            for x in range(self.player_projectile_count):
                offset = random.randint(-self.player_bullet_spread, self.player_bullet_spread)
                bullet = Bullet(self.bullet_speed, self.player_ship.x, firing_position,
                                offset + 90, self.player_bullet_damage, self.ship_size,
                                EntityID.FRIENDLY_FLAK)
                self.friendly_projectiles.append(bullet)
                # PLays the bullet sound
            self.bullet_sound.play()
        # Homing missiles
        elif self.player_projectile_type == EntityID.FRIENDLY_MISSILE:
            closest_enemy = self.find_closest_enemy(self.player_ship)
            for x in range(self.player_projectile_count):
                missile = Missile(self.bullet_speed, self.player_ship.x, firing_position,
                                  offset + 90, self.player_bullet_damage, self.ship_size,
                                  EntityID.FRIENDLY_MISSILE, self.fps, closest_enemy)
                offset += partition
                self.friendly_projectiles.append(missile)
            # Missile sound effect
            self.missile_sound.play()
        # Really bad missile
        elif self.player_projectile_type == EntityID.BAD_MISSILE:
            closest_enemy = self.find_closest_enemy(self.player_ship)
            for x in range(self.player_projectile_count):
                missile = BadMissile(self.bullet_speed, self.player_ship.x, firing_position,
                                     offset + 90, self.player_bullet_damage, self.ship_size,
                                     EntityID.FRIENDLY_BULLET, closest_enemy)
                offset += partition
                self.friendly_projectiles.append(missile)
            self.bullet_sound.play()
        elif self.player_projectile_type == EntityID.RAILGUN:
            for x in range(self.player_projectile_count):
                bullet = Bullet(self.bullet_speed, self.player_ship.x, firing_position,
                                90, int(self.player_bullet_damage * (30 / self.fps)), self.ship_size,
                                EntityID.RAILGUN)
                self.friendly_projectiles.append(bullet)
            self.railgun_sound.play()
        else:
            raise ValueError("Invalid projectile type:", str(self.player_projectile_type))

    """Finds the closest enemy to the given entity. Used primarily for missile tracking.

    :param source: Source ship or projectile to use as origin
    :type source: Ship or Projectile
    :returns: closest enemy to the source, or 0
    :rtype: Ship or int
    """

    def find_closest_enemy(self, source):
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

    """Checks if the entity is off screen, primarily used for the player so they cannot move off screen.

    :param entity: entity to check if off screen
    :type entity: Player
    :param direction: what direction the entity is going to move
    :type direction: Direction
    :param offset: offset of the size to check
    :type offset: int
    :returns: boolean of whether the ship is at the boundary of the screen or not
    :rtype: boolean
    :raises: ValueError if given direction is not valid
    """

    def boundary_check(self, entity, direction, offset):
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
        player = self.player_ship
        # Increases max HP and restores it
        player.max_hp += 5
        player.hp = player.max_hp
        # Increases max shield and restores it
        player.max_shield += 10
        player.shield_recharge_rate = (player.max_shield // 20 / self.fps)
        player.shield = player.max_shield
        # Increases damage and fire rate
        self.damage_modifier += .2
        self.reload_modifier -= .05
        if self.reload_modifier <= 0:
            self.reload_modifier = .1
        self.popup_text("Level Up", -1, self.height // 3, 3)
        # Refreshes the weapon stats for the player
        self.switch_weapon(self.player_weapon_type)

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
            if effect.entity_id == EntityID.POPUP:
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
        self.friendly_ships.append(self.player_ship)

    """Pauses the game by displaying a text field and prompt to exit to title screen.
    """

    def pause(self):
        self.popup_text("PAUSED", -1, self.height // 3, 1 / self.fps)
        self.popup_text("[BACKSPACE] TO RETURN TO TITLE", -1,
                        (self.height // 3) + (self.ship_size // 2), 1 / self.fps)
