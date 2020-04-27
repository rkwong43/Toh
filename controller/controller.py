import pygame
import os

from src.utils import config
from src.utils.direction import Direction

"""Controller that keeps track of time and key inputs to pass onto the _view and _model. Will also handle music
and different types of menus and screens
"""


class Controller:
    # Key bindings:
    _key_to_directions = {pygame.K_w: Direction.UP, pygame.K_a: Direction.LEFT, pygame.K_s: Direction.DOWN,
                          pygame.K_d: Direction.RIGHT, pygame.K_SPACE: Direction.FIRE, pygame.K_UP: Direction.UP,
                          pygame.K_DOWN: Direction.DOWN, pygame.K_RIGHT: Direction.RIGHT, pygame.K_LEFT: Direction.LEFT}
    # Music:
    # Music by Scott Buckley – www.scottbuckley.com.au
    current_path = os.path.dirname(__file__)  # where this file is located
    outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the _view folder
    resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
    music_path = os.path.join(resource_path, 'music')  # the music folder path

    """Constructor that takes in a _view and _model to run the game
    :param _model: the _model to pass the key inputs to and ticks
    :type _model: _model object
    :param _view: the _view to pass objects from the _model to render
    :type _view: _view object
    :param start_menu: the start menu _view
    :type start_menu: StartMenu_view
    :param _fps: frames per second to run the game at
    :type _fps: int
    """

    def __init__(self, _model, _view):
        self._model = _model
        self._view = _view
        self._fps = config.game_fps
        # Endurance by Scott Buckley is the music in the background
        self.game_music_path = os.path.join(self.music_path, 'endurance.mp3')

    """Runs the game, setting a clock and looping until game is quit or starts over.

    :returns: If the game has to restart
    :rtype: bool
    """

    def run_game(self):
        # In game clock for _fps and time
        clock = pygame.time.Clock()
        # Defines if the game is done
        done = False
        # Loads and plays the level music
        pygame.mixer.music.load(self.game_music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.5)
        paused = False
        ANIMATE = pygame.USEREVENT + 1
        game_over_countdown = self._fps * 5
        pygame.time.set_timer(ANIMATE, 300)
        while not done:
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    return False
                elif game_event.type == pygame.KEYUP:
                    # Pauses game
                    if game_event.key == pygame.K_ESCAPE:
                        paused = not paused
                    # Goes back to menu
                    elif game_event.key == pygame.K_BACKSPACE and paused:
                        return True
                # Animates sprites
                if game_event.type == ANIMATE:
                    self._view.animate()
            # Grabs the keys currently pressed down
            keys = pygame.key.get_pressed()
            # Moves the player and ticks
            if not paused:
                self._model.move_player(self._parse_keys(keys))
                self._model.tick()
            else:
                self._model.pause()
            # Renders the _view and removes lasting effects
            self._model.remove_effects()
            self._view.render(self._model.get_player(), self._model.get_projectiles(),
                              self._model.get_ships(), self._model.get_effects())
            if self._model.is_game_over():
                game_over_countdown -= 1
                if game_over_countdown == 0:
                    return True
            self._view.render_fps(int(clock.get_fps()))
            # Updates display
            pygame.display.update()
            clock.tick(self._fps)
        return False

    """Takes in a list of Pygame keys and returns a list of directions for the _model.

    :param keys: Keys to parse
    :type keys: List of Pygame Key constants
    :returns: list of directions
    :rtype: List of Direction
    """

    def _parse_keys(self, keys):
        result = []
        for key, direction in self._key_to_directions.items():
            if keys[key]:
                result.append(direction)
        return result
