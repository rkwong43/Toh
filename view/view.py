import os
import pygame

from src.utils.entity_id import EntityID
from src.view.image_containers.charge_up_images import ChargeUpImages
from src.view.image_containers.explosion_images import ExplosionImages
from src.view.image_containers.image_holder import ImageHolder
from src.view.image_containers.popup_image import PopUpImage
from src.view.image_containers.screen_tint_images import ScreenTintImages

"""View to render the game, uses pygame to render images. Add ships, projectiles, and effects images to render
inside their respective fields ships_to_init, projectiles_to_init, and effects_to_init inside init_images().
"""


class View:
    # Image paths
    current_path = os.path.dirname(__file__)  # where this file is located
    outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the View folder
    resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
    image_path = os.path.join(resource_path, 'images')  # the image folder path

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

    def __init__(self, display_width, display_height, game_title, ship_size, game_mode, fps):
        # Determines when to switch images for animation
        self.animation_switch = True
        # Sets up the game window surface
        self.game_display = pygame.display.set_mode((display_width, display_height))
        self.ship_size = ship_size
        # Title of the window
        pygame.display.set_caption(game_title)
        # Background image is 1920 x 1080
        background_path = os.path.join(self.image_path, 'background.png')
        if game_mode == EntityID.TITAN_SLAYER:
            background_path = os.path.join(self.image_path, 'titan_background.png')
        elif game_mode == EntityID.MANDIBLE_MADNESS:
            background_path = os.path.join(self.image_path, 'mandible_background.png')
        elif game_mode == EntityID.HEAVEN:
            background_path = os.path.join(self.image_path, 'heaven_background.png')
        elif game_mode == EntityID.SURVIVAL:
            background_path = os.path.join(self.image_path, 'survival_background.png')
        self.background = pygame.image.load(background_path).convert_alpha()
        self.background = pygame.transform.scale(self.background, (display_width, display_height))
        self.background_y = 0
        # How much the background scrolls
        self.background_change = 2 * (30 / fps)
        # Display parameters
        self.width = display_width
        self.height = display_height
        self.font_size = display_height / 24
        font_path = os.path.join(self.resource_path, 'fonts')
        font_path = os.path.join(font_path, 'insane_hours_2.ttf')
        self.text_font = pygame.font.Font(font_path, int(self.font_size))
        self.hp_text = self.text_font.render("HP", 1, (255, 255, 255)).convert_alpha()
        hp_width, hp_height = pygame.font.Font.size(self.text_font, "HP")
        self.red_bar = pygame.rect.Rect(hp_width, display_height - self.font_size + self.font_size / 3,
                                        display_width / 3, self.font_size / 3)
        self.hp_bar = self.red_bar.copy()
        # Shield bar for player
        self.shield_bar = pygame.rect.Rect(hp_width, display_height - self.font_size + self.font_size / 5,
                                           display_width / 3, self.font_size / 4)
        # Score
        self.score_text = self.text_font.render("Score:", 1, (255, 255, 255)).convert_alpha()
        self.score_x = hp_width + (display_width / 3) + self.font_size
        self.score_width = pygame.font.Font.size(self.text_font, "Score:")[0]
        # FPS ticker
        self.fps_text = self.text_font.render("FPS:", 1, (255, 255, 255)).convert_alpha()

        # Grabs the image dictionary
        self.image_dict = self.init_images(fps)

    """Initializes all the images used in the game.
    
    :param fps: frames per second to pass to image holders
    :type fps: int
    :returns: dictionary of entity ID to images
    :rtype: {EntityID : ImageHolder}
    """

    def init_images(self, fps):
        # Result to return:
        result = {}
        # Standard sized player ships to render:
        players_to_init = [EntityID.CITADEL, EntityID.AEGIS, EntityID.GHOST, EntityID.ARCHANGEL, EntityID.STORM,
                           EntityID.ORIGIN]
        # Standard sized ships to render
        ships_to_init = [EntityID.MANDIBLE, EntityID.MANTIS, EntityID.CRUCIBLE, EntityID.MOSQUITO,
                         EntityID.SUBJUGATOR, EntityID.SEER]
        # Larger ships to render (1.5 * ship_size)
        large_ships_to_init = [EntityID.ARBITRATOR, EntityID.TERMINUS, EntityID.JUDICATOR]
        # Larger ships to render (2 * ship_size)
        larger_ships_to_init = [EntityID.MOTHERSHIP, EntityID.DESPOILER]
        # Largest ships to render
        largest_ships_to_init = [EntityID.TITAN]
        # Projectiles to render
        projectiles_to_init = [EntityID.FRIENDLY_FLAK, EntityID.FRIENDLY_BULLET, EntityID.FRIENDLY_MISSILE,
                               EntityID.ENEMY_MISSILE, EntityID.ENEMY_BULLET, EntityID.ENEMY_FLAK]
        # Effects to render
        effects_to_init = [EntityID.EXPLOSION, EntityID.RED_EXPLOSION, EntityID.BLUE_EXPLOSION]

        # Renders each ship (standard sized)
        for id_name in ships_to_init + players_to_init:
            ship_name = id_name.name
            image_paths = [os.path.join(self.image_path, ship_name + '_base.png'),
                           os.path.join(self.image_path, ship_name + '_animation.png'),
                           os.path.join(self.image_path, ship_name + '_damaged.png'),
                           os.path.join(self.image_path, ship_name + '_shield.png')]
            container = ImageHolder(image_paths, self.ship_size)
            result[id_name] = container
        # Larger ships to render
        for id_name in large_ships_to_init:
            ship_name = id_name.name
            image_paths = [os.path.join(self.image_path, ship_name + '_base.png'),
                           os.path.join(self.image_path, ship_name + '_animation.png'),
                           os.path.join(self.image_path, ship_name + '_damaged.png'),
                           os.path.join(self.image_path, ship_name + '_shield.png')]
            container = ImageHolder(image_paths, int(self.ship_size * 1.5))
            result[id_name] = container
        # Even larger ships to render:
        for id_name in larger_ships_to_init:
            ship_name = id_name.name
            image_paths = [os.path.join(self.image_path, ship_name + '_base.png'),
                           os.path.join(self.image_path, ship_name + '_animation.png'),
                           os.path.join(self.image_path, ship_name + '_damaged.png'),
                           os.path.join(self.image_path, ship_name + '_shield.png')]
            container = ImageHolder(image_paths, int(self.ship_size * 2))
            result[id_name] = container
        # Largest ships to render:
        for id_name in largest_ships_to_init:
            ship_name = id_name.name
            image_paths = [os.path.join(self.image_path, ship_name + '_base.png'),
                           os.path.join(self.image_path, ship_name + '_animation.png'),
                           os.path.join(self.image_path, ship_name + '_damaged.png'),
                           os.path.join(self.image_path, ship_name + '_shield.png')]
            container = ImageHolder(image_paths, int(self.ship_size * 8))
            result[id_name] = container
        # Renders each projectile
        projectile_size = self.ship_size // 2
        for id_name in projectiles_to_init:
            projectile_name = id_name.name
            image_path = os.path.join(self.image_path, projectile_name + '.png')
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (projectile_size, projectile_size))
            result[id_name] = image
        # Renders each effect (explosions)
        for id_name in effects_to_init:
            effect_name = id_name.name
            image_paths = [os.path.join(self.image_path, effect_name + '_frame1.png'),
                           os.path.join(self.image_path, effect_name + '_frame2.png'),
                           os.path.join(self.image_path, effect_name + '_frame3.png'),
                           os.path.join(self.image_path, effect_name + '_frame4.png'),
                           os.path.join(self.image_path, effect_name + '_frame5.png')]
            container = ExplosionImages(image_paths, int(self.ship_size * 1.5), fps)
            if effect_name == "EXPLOSION":
                big_container = ExplosionImages(image_paths, int(self.ship_size * 8), fps)
                result[EntityID.TITAN_EXPLOSION] = big_container
            elif effect_name == "RED_EXPLOSION":
                charge_effect_container = ChargeUpImages(image_paths, int(self.ship_size * 1.5), fps)
                result[EntityID.RED_CHARGE] = charge_effect_container
            result[id_name] = container
        # Screen tints
        blue_tint = os.path.join(self.image_path, 'shield_damage_screen_effect.png')
        red_tint = os.path.join(self.image_path, 'damage_screen_effect.png')
        shield_damage_tint = ScreenTintImages(blue_tint, self.width, self.height)
        damage_tint = ScreenTintImages(red_tint, self.width, self.height)
        result[EntityID.SHIELD_TINT] = shield_damage_tint
        result[EntityID.HP_TINT] = damage_tint
        # Popup text
        result[EntityID.POPUP] = PopUpImage(self.text_font, self.width, self.height)
        return result

    """Switches a field to determine when to animate images.
    """

    def animate(self):
        self.animation_switch = not self.animation_switch

    """Renders the game, including background, ships, and projectiles.

    :param items: ships and projectiles to render
    :type items: list of Ship or Projectile
    """

    def render(self, player, projectiles, enemies, effects):
        # Scrolling background
        self.draw_background()
        # If the player isn't dead, it is rendered
        if not player.dead:
            self.render_ship(player, 0)
        # Renders enemies to face the player
        for enemy in enemies:
            self.render_ship(enemy, enemy.angle)
        # Renders projectiles
        for projectile in projectiles:
            self.render_projectile(projectile)
        # Renders effects
        for effect in effects:
            self.render_effect(effect)
        # Renders HUD
        self.draw_hud(player)

    """Draws the scrolling background.
    """

    def draw_background(self):
        self.game_display.blit(self.background, (0, self.background_y))
        self.game_display.blit(self.background, (0, self.background_y - self.height))
        self.background_y += self.background_change
        if self.background_y == self.height:
            self.background_y = 0

    """Draws the HUD on the bottom of the screen.
    
    :param player: Player to grab score, health, and shielding from
    :type player: Ship
    """

    def draw_hud(self, player):
        # Red bar underneath
        pygame.draw.rect(self.game_display, (255, 0, 0), self.red_bar)
        # Green HP bar above the red bar
        if player.hp > 0:
            self.hp_bar.width = (self.width / 3) / (player.max_hp / player.hp)
            pygame.draw.rect(self.game_display, (0, 148, 43), self.hp_bar)
        # Shield health bar
        if player.shield > 0:
            self.shield_bar.width = (self.width / 3) / (player.max_shield / player.shield)
            pygame.draw.rect(self.game_display, (0, 159, 225), self.shield_bar)
        # HP Text
        self.game_display.blit(self.hp_text, (0, self.height - self.font_size))
        # Score
        self.game_display.blit(self.score_text, (self.score_x, self.height - self.font_size))
        score = self.text_font.render(str(player.score), 1, (255, 255, 255)).convert_alpha()
        self.game_display.blit(score, (self.score_x + self.score_width,
                                       self.height - self.font_size))

    """Renders an individual ship depending on if it's damaged etc.
    
    :param ship: ship to render
    :type ship: Ship
    :param angle: angle to rotate image to
    :type angle: int
    """

    def render_ship(self, ship, angle):
        image_holder = self.image_dict.get(ship.entity_id)

        image = image_holder.base_image
        # Decides which image to use:
        # damaged image, base image, or second base image for animation for engines
        if ship.isDamaged:
            if ship.shield > 0:
                image = image_holder.shield_damage_image
            else:
                image = image_holder.damaged_image
        elif self.animation_switch:
            image = image_holder.animated_image
        # Rotates enemy to face the given angle
        enemy_image = pygame.transform.rotate(image, angle)
        new_rect = enemy_image.get_rect(center=(ship.x + ship.size / 2, ship.y + ship.size / 2))
        self.game_display.blit(enemy_image, new_rect.topleft)

    """Renders an individual projectile depending on its orientation.
    
    :param projectile: projectile to render
    :type projectile: Projectile
    """

    def render_projectile(self, projectile):
        if projectile.entity_id != EntityID.RAILGUN:
            image = self.image_dict.get(projectile.entity_id)
            # Rotates the projectile depending on its angle
            projectile_image = pygame.transform.rotate(image, projectile.direction - 90)
            center_height = projectile.y + self.ship_size / 2
            center_width = projectile.x + self.ship_size / 2
            new_rect = projectile_image.get_rect(
                center=(center_width, center_height))
            self.game_display.blit(projectile_image, new_rect.topleft)

    """Renders the given effect. Returns the effect.
    
    :param effect: effect to render
    :type effect: Effect
    :returns: the effect
    :rtype: Effect
    """

    def render_effect(self, effect):
        image = self.image_dict.get(effect.entity_id).get_frame(effect)
        self.game_display.blit(image, (effect.x, effect.y))
        return effect

    """Renders the FPS counter for the game.
    
    :param fps: frames per second
    :type fps: int
    """

    def render_fps(self, fps):
        self.game_display.blit(self.fps_text, (self.width - (5 * self.font_size), self.height - self.font_size))
        fps_number = self.text_font.render(str(fps), 1, (255, 255, 255)).convert_alpha()
        self.game_display.blit(fps_number, (self.width - (2 * self.font_size), self.height - self.font_size))
