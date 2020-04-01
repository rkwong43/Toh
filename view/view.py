import os
import pygame

from src.utils import config
from src.utils.ids.effect_id import EffectID
from src.utils.ids.enemy_id import EnemyID
from src.utils.ids.game_id import GameID
from src.utils.ids.gamemode_id import GameModeID
from src.utils.ids.player_id import PlayerID
from src.utils.ids.projectile_id import ProjectileID
from src.view.image_containers.charge_up_images import ChargeUpImages
from src.view.image_containers.explosion_images import ExplosionImages
from src.view.image_containers.image_holder import ImageHolder
from src.view.image_containers.popup_image import PopUpImage
from src.view.image_containers.screen_tint_images import ScreenTintImages

"""View to render the game, uses pygame to render images. Add ships, projectiles, and effects images to render
inside their respective fields ships_to_init, projectiles_to_init, and effects_to_init inside init_images().
"""


class View:
    WHITE = (255, 255, 255)
    # Image paths
    _current_path = os.path.dirname(__file__)  # where this file is located
    _outer_path = os.path.abspath(os.path.join(_current_path, os.pardir))  # the View folder
    _resource_path = os.path.join(_outer_path, 'resources')  # the resource folder path
    _image_path = os.path.join(_resource_path, 'images')  # the image folder path
    # Font size
    _font_path = os.path.join(_resource_path, 'fonts')
    _font_path = os.path.join(_font_path, 'insane_hours_2.ttf')
    # Backgrounds
    _backgrounds = {GameModeID.TITAN_SLAYER: os.path.join(_image_path, 'titan_background.png'),
                    GameModeID.MANDIBLE_MADNESS: os.path.join(_image_path, 'mandible_background.png'),
                    GameModeID.CLASSIC: os.path.join(_image_path, 'survival_background.png'),
                    GameModeID.HEAVEN: os.path.join(_image_path, 'heaven_background.png'),
                    GameID.MENU: os.path.join(_image_path, 'background.png'),
                    GameID.TUTORIAL: os.path.join(_image_path, 'background.png')
                    }

    # Ship scaling (what the default ship size should be multiplied by in their rendering)
    _ship_scaling = {
        EnemyID.MANDIBLE: 1, EnemyID.MANTIS: 1, EnemyID.CRUCIBLE: 1, EnemyID.MOSQUITO: 1,
        EnemyID.SUBJUGATOR: 1, EnemyID.SEER: 1,
        EnemyID.ARBITRATOR: 1.5, EnemyID.TERMINUS: 1.5, EnemyID.JUDICATOR: 1.5,
        EnemyID.MOTHERSHIP: 2, EnemyID.DESPOILER: 2,
        EnemyID.TITAN: 8
    }
    # All player ships are by default x1 size
    for player_ship in PlayerID:
        _ship_scaling[player_ship] = 1

    """Constructor to initialize the game display.

    :param display_width: width of the window
    :type display_width: int
    :param display_height: height of the window
    :type display_height: int
    :param game_title: caption to put as the window title
    :type game_title: str
    :param ship_size: size to render base ships to
    :type ship_size: int
    :param game_mode: Game mode to determine background
    :type game_mode: EntityID
    :param fps: Frames per second to set effect length
    :type fps: int
    """

    def __init__(self, game_mode):
        self._width = config.display_width
        self._height = config.display_height
        #######################################################
        # Determines when to switch images for animation
        self._animation_switch = True
        # Sets up the game window surface
        self._game_display = pygame.display.set_mode((self._width, self._height))
        self._ship_size = config.ship_size
        # Title of the window
        pygame.display.set_caption(config.game_title)
        #######################################################
        background_path = self._backgrounds[game_mode]
        self._background = pygame.image.load(background_path).convert_alpha()
        self._background = pygame.transform.scale(self._background, (self._width, self._height))
        self._background_y = 0
        # How much the background scrolls
        self._background_change = 2 * (30 / config.game_fps)
        #######################################################
        # Display parameters
        self._font_size = self._height / 24
        self._text_font = pygame.font.Font(self._font_path, int(self._font_size))
        self._hp_text = self._text_font.render("HP", 1, self.WHITE).convert_alpha()
        hp_width, hp_height = pygame.font.Font.size(self._text_font, "HP")
        #######################################################
        self._red_bar = pygame.rect.Rect(hp_width, self._height - self._font_size + self._font_size / 3,
                                         self._width / 3, self._font_size / 3)
        self._hp_bar = self._red_bar.copy()
        # Shield bar for player
        # TODO: Change to just copying then adjusting height
        self._shield_bar = pygame.rect.Rect(hp_width, self._height - self._font_size + self._font_size / 5,
                                            self._width / 3, self._font_size / 4)
        #######################################################
        # Score
        self._score_text = self._text_font.render("Score:", 1, self.WHITE).convert_alpha()
        self._score_x = hp_width + (self._width / 3) + self._font_size
        self._score_width = pygame.font.Font.size(self._text_font, "Score:")[0]
        #######################################################
        # FPS ticker
        self._fps_text = self._text_font.render("FPS:", 1, self.WHITE).convert_alpha()

        #######################################################
        # Grabs the image dictionary
        self._image_dict = self._init_images()

    """Initializes all the images used in the game.

    :returns: dictionary of entity ID to images
    :rtype: {EntityID : ImageHolder}
    """

    def _init_images(self):
        # Result to return:
        result = {}
        # Projectiles to render
        projectiles_to_init = [e for e in ProjectileID if e not in
                               [ProjectileID.RAILGUN_BLAST, ProjectileID.DIAMOND_DUST, ProjectileID.HOMING_BULLET]]
        # Effects to render
        effects_to_init = [EffectID.EXPLOSION, EffectID.RED_EXPLOSION, EffectID.BLUE_EXPLOSION]
        # Renders each ship
        for id_name, size in self._ship_scaling.items():
            ship_name = id_name.name
            image_paths = self._get_image_paths(ship_name)
            container = ImageHolder(image_paths, int(self._ship_size * size))
            result[id_name] = container
        # Renders each projectile
        projectile_size = self._ship_size // 2
        for id_name in projectiles_to_init:
            projectile_name = id_name.name
            image_path = os.path.join(self._image_path, projectile_name + '.png')
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (projectile_size, projectile_size))
            result[id_name] = image
        # Renders each effect (explosions)
        for id_name in effects_to_init:
            effect_name = id_name.name
            image_paths = [os.path.join(self._image_path, effect_name + '_frame1.png'),
                           os.path.join(self._image_path, effect_name + '_frame2.png'),
                           os.path.join(self._image_path, effect_name + '_frame3.png'),
                           os.path.join(self._image_path, effect_name + '_frame4.png'),
                           os.path.join(self._image_path, effect_name + '_frame5.png')]
            container = ExplosionImages(image_paths, int(self._ship_size * 1.5))
            # Two additional effects that do not have different sprites
            if effect_name == "EXPLOSION":
                big_container = ExplosionImages(image_paths, int(self._ship_size * 8))
                result[EffectID.TITAN_EXPLOSION] = big_container
            elif effect_name == "RED_EXPLOSION":
                charge_effect_container = ChargeUpImages(image_paths, int(self._ship_size * 1.5))
                result[EffectID.RED_CHARGE] = charge_effect_container
            result[id_name] = container
        # Screen tints
        blue_tint = os.path.join(self._image_path, 'shield_damage_screen_effect.png')
        red_tint = os.path.join(self._image_path, 'damage_screen_effect.png')
        shield_damage_tint = ScreenTintImages(blue_tint)
        damage_tint = ScreenTintImages(red_tint)
        result[EffectID.SHIELD_TINT] = shield_damage_tint
        result[EffectID.HP_TINT] = damage_tint
        # Popup text
        result[EffectID.POPUP] = PopUpImage(self._text_font)
        return result

    """Returns a list of the image paths for a ship.

    :param ship_name: Name of the ship and the image file
    :type ship_name: str
    :returns: list of image paths
    :rtype: str
    """

    def _get_image_paths(self, ship_name):
        return [os.path.join(self._image_path, ship_name + '_base.png'),
                os.path.join(self._image_path, ship_name + '_animation.png'),
                os.path.join(self._image_path, ship_name + '_damaged.png'),
                os.path.join(self._image_path, ship_name + '_shield.png')]

    """Switches a field to determine when to animate images.
    """

    def animate(self):
        self._animation_switch = not self._animation_switch

    """Renders the game, including background, ships, and projectiles.

    :param items: ships and projectiles to render
    :type items: list of Ship or Projectile
    """

    def render(self, player, projectiles, enemies, effects):
        # Scrolling background
        self._draw_background()
        # If the player isn't dead, it is rendered
        if not player.is_dead:
            self._render_ship(player, 0)
        # Renders enemies to face the player
        for enemy in enemies:
            self._render_ship(enemy, enemy.angle)
        # Renders projectiles
        for projectile in projectiles:
            self._render_projectile(projectile)
        # Renders effects
        for effect in effects:
            self._render_effect(effect)
        # Renders HUD
        self._draw_hud(player)

    """Draws the scrolling background.
    """

    def _draw_background(self):
        self._game_display.blit(self._background, (0, self._background_y))
        self._game_display.blit(self._background, (0, self._background_y - self._height))
        self._background_y += self._background_change
        if self._background_y == self._height:
            self._background_y = 0

    """Draws the HUD on the bottom of the screen.

    :param player: Player to grab score, health, and shielding from
    :type player: Ship
    """

    def _draw_hud(self, player):
        # Red bar underneath
        pygame.draw.rect(self._game_display, (255, 0, 0), self._red_bar)
        # Green HP bar above the red bar
        if player.hp > 0:
            self._hp_bar.width = (self._width / 3) / (player.max_hp / player.hp)
            pygame.draw.rect(self._game_display, (0, 148, 43), self._hp_bar)
        # Shield health bar
        if player.shield > 0:
            self._shield_bar.width = (self._width / 3) / (player.max_shield / player.shield)
            pygame.draw.rect(self._game_display, (0, 159, 225), self._shield_bar)
        # HP Text
        self._game_display.blit(self._hp_text, (0, self._height - self._font_size))
        # Score
        self._game_display.blit(self._score_text, (self._score_x, self._height - self._font_size))
        score = self._text_font.render(str(player.score), 1, self.WHITE).convert_alpha()
        self._game_display.blit(score, (self._score_x + self._score_width,
                                        self._height - self._font_size))

    """Renders an individual ship depending on if it's damaged etc.

    :param ship: ship to render
    :type ship: Ship
    :param angle: angle to rotate image to
    :type angle: int
    """

    def _render_ship(self, ship, angle):
        image_holder = self._image_dict.get(ship.entity_id)
        image = image_holder.base_image
        # Decides which image to use:
        # damaged image, base image, or second base image for animation for engines
        if ship.is_damaged:
            if ship.shield > 0:
                image = image_holder.shield_damage_image
            else:
                image = image_holder.damaged_image
        elif self._animation_switch:
            image = image_holder.animated_image
        # Rotates enemy to face the given angle
        enemy_image = pygame.transform.rotate(image, angle)

        self._game_display.blit(enemy_image,
                                self._find_posn(enemy_image, ship.x + ship.size / 2, ship.y + ship.size / 2))

    """Renders an individual projectile depending on its orientation.

    :param projectile: projectile to render
    :type projectile: Projectile
    """

    def _render_projectile(self, projectile):
        if projectile.entity_id != ProjectileID.RAILGUN_BLAST:
            image = self._image_dict.get(projectile.entity_id)
            # Rotates the projectile depending on its angle
            projectile_image = pygame.transform.rotate(image, projectile.direction - 90)
            center_height = projectile.y + self._ship_size / 2
            center_width = projectile.x + self._ship_size / 2
            self._game_display.blit(projectile_image, self._find_posn(projectile_image, center_width, center_height))

    """Renders the given effect. Returns the effect.

    :param effect: effect to render
    :type effect: Effect
    :returns: the effect
    :rtype: Effect
    """

    def _render_effect(self, effect):
        image = self._image_dict.get(effect.entity_id).get_frame(effect)
        self._game_display.blit(image, (effect.x, effect.y))
        return effect

    """Renders the FPS counter for the game.

    :param fps: frames per second
    :type fps: int
    """

    def render_fps(self, fps):
        self._game_display.blit(self._fps_text, (self._width - (5 * self._font_size), self._height - self._font_size))
        fps_number = self._text_font.render(str(fps), 1, self.WHITE).convert_alpha()
        self._game_display.blit(fps_number, (self._width - (2 * self._font_size), self._height - self._font_size))

    """Finds position given a Surface and coordinates for the center. Returns the coordinates that
    correspond to the correct top left position to place the surface to achieve the given center.
    
    :param image: Surface to find coordinates to
    :type image: Surface
    :param x: x position
    :type x: int
    :param y: y position
    :param y: int
    :returns: tuple of the coordinates to place it
    :rtype: (int, int)
    """

    def _find_posn(self, image, x, y):
        rect = image.get_rect(center=(x, y))
        return rect.topleft
