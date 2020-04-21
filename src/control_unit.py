"""Contains the control unit class. This is where the magic happens. It controls game state
and almost all in-game logic. It might outsource some in-game logic for better readability.
Uses the Map class to keep track of the tiles and their rotation, as well as rendering them.
Calls the GUI class for menu rendering and the Map class for in-game rendering."""
import pygame
import os
import events
from enums import GameState
from gui import GUI
from src.game_data import GameData


class ControlUnit:
    """The control unit of the game. Keeps track of the game state, executes the game loop
    and calls GUI and Map classes where needed."""
    def __init__(self):
        """Initializes the control unit and the game itself. Sets variables like window position, size,
        and initializes the GUI class"""
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.state = GameState.MainMenu
        self.running = False
        self.screen_dimensions = (1000, 1000)
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        program_icon = pygame.image.load('res/icon_loop.png')
        pygame.display.set_icon(program_icon)
        pygame.display.set_caption("Indefinite Loop")
        self.game_data = GameData("game_data.json")
        self.gui = GUI(self.screen, self.game_data)
        # self.map = Map(self.screen)

    def game_loop(self):
        """Starts the game loop."""
        self.running = True
        while self.running:
            self.clock.tick(self.FPS)
            self.render()
            self.run_events()

    def render(self):
        """Renders what's on the screen, depending on the game state. Calls either the GUI or the Map class."""
        if self.state == GameState.MainMenu:
            self.gui.draw_main_menu()
        pygame.display.flip()

    def run_events(self):
        """Checks for all the events pygame might have fired."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == GameState.MainMenu:
                self.handle_event_main_menu(event)

    def handle_event_main_menu(self, event):
        """Handles all events that need to be handled in the main menu."""
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            self.gui.check_button_hover(mouse)
        if event.type == pygame.MOUSEBUTTONUP:
            self.gui.click(mouse)
        if event.type == events.START_GAME_MODE_0:
            print("Start level " + str(event.level))
