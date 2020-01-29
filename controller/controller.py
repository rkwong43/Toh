import pygame
import os
import threading

from src.direction import Direction

"""Controller that keeps track of time and key inputs to pass onto the view and model. Will also handle music
and different types of menus and screens
"""


class Controller:
    # Key bindings:
    key_to_directions = {pygame.K_w: Direction.UP, pygame.K_a: Direction.LEFT, pygame.K_s: Direction.DOWN,
                         pygame.K_d: Direction.RIGHT, pygame.K_SPACE: Direction.FIRE}
    # If the player dies in the game
    game_over = False
    """Constructor that takes in a view and model to run the game
    :param model: the model to pass the key inputs to and ticks
    :type model: Model object
    :param view: the view to pass objects from the model to render
    :type view: View object
    :param start_menu: the start menu view
    :type start_menu: StartMenuView
    :param fps: frames per second to run the game at
    :type fps: int
    """

    def __init__(self, model, view, fps):
        self.model = model
        self.view = view
        self.fps = fps
        # Ticks for animation
        self.ticks = 0
        self.tick_limit = fps // 5
        # Music by Scott Buckley – www.scottbuckley.com.au
        current_path = os.path.dirname(__file__)  # where this file is located
        outer_path = os.path.abspath(os.path.join(current_path, os.pardir))  # the View folder
        resource_path = os.path.join(outer_path, 'resources')  # the resource folder path
        music_path = os.path.join(resource_path, 'music')  # the music folder path
        # Endurance by Scott Buckley is the music in the background
        self.game_music_path = os.path.join(music_path, 'endurance.mp3')

    """Runs the game, setting a clock and looping until game is quit or starts over.
    
    :returns: If the game has to restart
    :rtype: bool
    """

    def run_game(self):
        # In game clock for FPS and time
        clock = pygame.time.Clock()
        # Defines if the game is done
        done = False
        # Loads and plays the level music
        pygame.mixer.music.load(self.game_music_path)
        pygame.mixer.music.play(-1)
        paused = False
        while not done:
            # Creating two threads
            t1 = threading.Thread(target=self.model.tick)
            t2 = threading.Thread(target=self.view.render, args=(self.model.player_ship, self.model.get_projectiles(),
                                                                 self.model.get_enemies(), self.model.get_effects()))
            for game_event in pygame.event.get():
                # Checks if quit
                if game_event.type == pygame.QUIT:
                    done = True
                elif game_event.type == pygame.KEYUP:
                    # Pauses game
                    if game_event.key == pygame.K_ESCAPE:
                        paused = not paused
                    # Goes back to menu
                    elif game_event.key == pygame.K_BACKSPACE and paused:
                        return True
            # Grabs the keys currently pressed down
            keys = pygame.key.get_pressed()
            # Moves the player and ticks
            if not paused:
                self.model.move_player(self.parse_keys(keys))
                t1.start()
            else:
                self.model.pause()
            self.ticks += 1
            t2.start()
            # Every few frames the animation will be changed
            if self.ticks == self.tick_limit:
                self.view.animate()
                self.ticks = 0
                if self.model.game_over:
                    self.tick_limit = self.fps * 4
                    # Starts the game over
                    if self.game_over:
                        t1.join()
                        t2.join()
                        return True
                    self.game_over = True
            if not paused:
                t1.join()
            t2.join()

            # Updates display
            pygame.display.update()
            clock.tick(self.fps)
        return False

    """Takes in a list of Pygame keys and returns a list of directions for the model.
    
    :param keys: Keys to parse
    :type keys: List of Pygame Key constants
    :returns: list of directions
    :rtype: List of Direction
    """

    def parse_keys(self, keys):
        result = []
        for key, direction in self.key_to_directions.items():
            if keys[key]:
                result.append(direction)
        return result
