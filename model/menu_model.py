from src.entities.effects.explosion import Explosion
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
from src.entity_id import EntityID
from src.model.model import Model

"""Represents the model that handles displaying weapons or enemies in a gallery type menu.
"""


class MenuModel(Model):
    # If a weapon or enemy is being showcased
    showcase_weapon = False
    showcase_enemy = False
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

    def __init__(self, width, height, ship_size, fps):
        super().__init__(width, height, ship_size, fps, EntityID.GUN, EntityID.SURVIVAL, EntityID.EASY)
        self.player_ship.x = self.width
        self.play = False

    """Represents a tick in the game. Handles reloads and moves all projectiles and updates the AI module to
    move enemies. Also rotates enemies to face the player.
    """

    def tick(self):
        if self.play:
            # Moves all projectiles
            for projectile in self.friendly_projectiles + self.enemy_projectiles:
                projectile.move()
            # Has enemies immediately fire when ready
            if self.showcase_enemy:
                for ship in self.enemy_ships:
                    ship.move()
                    ship.ticks += 1
                    if ship.ticks == ship.fire_rate:
                        ship.ticks = 0
                        if ship.ready_to_fire:
                            if ship.projectile_type == EntityID.ENEMY_BULLET or \
                                    ship.projectile_type == EntityID.ENEMY_FLAK:
                                self.bullet_sound.play()
                            elif ship.projectile_type == EntityID.RAILGUN or \
                                    ship.projectile_type == EntityID.BAD_MISSILE:
                                self.railgun_sound.play()
                            else:
                                self.missile_sound.play()
                            ship.fire(self.player_ship, self.enemy_projectiles)
            # Reloads the player's weapon depending on its fire speed
            if self.showcase_weapon:
                if self.reload < self.max_fire_speed:
                    self.reload += 1
                elif self.reload == self.max_fire_speed:
                    self.projectile_generator()
                    self.reload = 0
            # Checks collisions between projectiles and ships
            self.remove_off_screen_objects()
            for ship in self.enemy_ships:
                ship.isDamaged = False
            self.player_ship.isDamaged = False
            self.check_collisions()

    """Checks for any projectile collisions between ships and ship collisions. If the ship is destroyed, adds an
    explosion effect to the effects list.
    """

    def check_collisions(self):
        # Checks friendly projectiles vs. enemy ships
        self.check_collisions_helper(self.enemy_ships, self.friendly_projectiles, EntityID.BLUE_EXPLOSION)
        # Checks enemy projectiles vs. friendly ships
        self.check_collisions_helper(self.friendly_ships, self.enemy_projectiles, EntityID.RED_EXPLOSION)

    """Checks collisions between the given list of ships and projectiles. Bare-bones version for modeling weapons.

    :param ships: ships to check
    :type ships: List of Ship
    :param projectiles: projectiles to check
    :type projectiles: List of Projectile
    :param splash_color: color explosion for projectiles to use, also adjusts score of player if blue
    :type splash_color: EntityID
    """

    def check_collisions_helper(self, ships, projectiles, splash_color):
        for projectile in projectiles:
            # If it is a railgun, uses explosions as indication of where they are
            weapon_type = projectile.entity_id
            if weapon_type == EntityID.RAILGUN:
                self.effects.append(Explosion(projectile.x - self.ship_size / 4,
                                              projectile.y - self.ship_size / 4,
                                              splash_color, self.fps))
            for ship in ships:
                # Hit box
                ship_bounding_box = ship.size / 4
                # Radius for air burst
                air_burst_box = int(self.ship_size * .7)
                air_burst_distance = projectile.air_burst and self.check_distance(projectile, ship, air_burst_box)
                # Checks if the projectile makes direct contact with the ship or is in air burst range
                if self.check_distance(projectile, ship, ship_bounding_box) or air_burst_distance:
                    # Creates an explosion around the projectile
                    ship.isDamaged = True
                    if projectile.has_splash:
                        # Calculates what ships receive splash damage
                        self.check_splash_damage(projectile, ship, ships)
                        self.effects.append(Explosion(projectile.x - (projectile.size // 4),
                                                      projectile.y,
                                                      splash_color, self.fps))
                        self.explosion_sound.play()
                    if projectile.entity_id != EntityID.RAILGUN:
                        projectiles.remove(projectile)
                    break

    """Switches the player's weapon to the given type.

    :param weapon: weapon type
    :type weapon: EntityID
    """

    def switch_weapon(self, weapon):
        super().switch_weapon(weapon)
        if not self.showcase_weapon:
            self.showcase_weapon = True
            self.showcase_enemy = False
        if len(self.enemy_ships) == 0:
            self.clear()
            self.player_bullet_damage = 0
            self.player_ship.x = self.width / 4
            self.player_ship.y = self.height * .75
            mandible = Mandible(self.ship_size, self.width / 4, self.height / 3, 1000, 1, 1, 1, 1, 1, False, self.fps)
            mandible3 = Mandible(self.ship_size, (self.width / 4) + self.ship_size, self.height / 3,
                                 1000, 1, 1, 1, 1, 1, False, self.fps)
            mandible4 = Mandible(self.ship_size, (self.width / 4) - self.ship_size, self.height / 3,
                                 1000, 1, 1, 1, 1, 1, False, self.fps)
            self.enemy_ships.extend([mandible, mandible3, mandible4])

    """Spawns a ship and places it in a predetermined position.

    :param entity_id: ID of ship to spawn
    :type entity_id: EntityID
    """

    def spawn_ship(self, entity_id):
        if not self.showcase_enemy:
            self.showcase_enemy = True
            self.showcase_weapon = False
        if len(self.enemy_ships) == 0:
            self.clear()
            self.player_ship.x = self.width / 4
            self.player_ship.y = self.height * .75
            ship = None
            x_pos = self.width / 4
            if entity_id == EntityID.MANDIBLE:
                ship = Mandible(self.ship_size, x_pos, self.height / 3, 1000, 0, 1,
                                0, self.fps, 1000,
                                False, self.fps)
            elif entity_id == EntityID.MANTIS:
                ship = Mantis(self.ship_size, x_pos, self.height / 3, 1000, x_pos, 1,
                              0, self.fps, 1000, False,
                              self.fps)
            elif entity_id == EntityID.CRUCIBLE:
                ship = Crucible(self.ship_size, x_pos, self.height / 3, 1000, 0, 1,
                                0, self.fps, 1000, self.fps)
            elif entity_id == EntityID.MOSQUITO:
                ship = Mosquito(self.ship_size, x_pos, self.height / 3, 1000, 0, 1,
                                0, self.fps, 1000, self.fps)
            elif entity_id == EntityID.SUBJUGATOR:
                ship = Subjugator(self.ship_size, x_pos, self.height / 3, 1000, 0, 1,
                                  0, self.fps, 1000, self.fps)
            elif entity_id == EntityID.ARBITRATOR:
                ship = Arbitrator(self.ship_size * 1.5, x_pos - (self.ship_size // 4), self.height / 3, 1000,
                                  0, 1,
                                  0, self.fps, 1000, self.fps)
            elif entity_id == EntityID.TERMINUS:
                ship = Terminus(self.ship_size * 1.5, x_pos - (self.ship_size // 4), self.height / 3, 1000,
                                0, 1,
                                0, self.fps, 1000, self.fps,
                                self.effects)
            elif entity_id == EntityID.SEER:
                ship = Seer(self.ship_size, x_pos, self.height / 3, 1000, x_pos, 1,
                            0, self.fps, 1000, self.fps)
            elif entity_id == EntityID.JUDICATOR:
                ship = Judicator(self.ship_size * 1.5, x_pos - (self.ship_size // 4), self.height / 3, 1000,
                                 0, 1,
                                 0, self.fps, 1000, self.fps,
                                 self.effects)
            elif entity_id == EntityID.MOTHERSHIP:
                ship = Mothership(self.ship_size * 2, x_pos - (self.ship_size // 2), self.height / 3, 1000,
                                  0, 1,
                                  0, self.fps, 1000, self.fps, None)
            elif entity_id == EntityID.DESPOILER:
                ship = Despoiler(self.ship_size * 2, x_pos - (self.ship_size // 2), self.height / 3, 1000, 0,
                                 1,
                                 0, self.fps, 1000, self.fps)
            ship.projectile_damage = 0
            self.enemy_ships.append(ship)
