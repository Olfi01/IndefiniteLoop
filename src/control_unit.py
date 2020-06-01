"""Contains the control unit class. This is where the magic happens. It controls game state
and almost all in-game logic. It might outsource some in-game logic for better readability.
Uses the Map class to keep track of the tiles and their rotation, as well as rendering them.
Calls the GUI class for menu rendering and the Map class for in-game rendering."""
import pygame
import os
import events
from enums import GameState
from gui import GUI
from game_data import GameData
from map import Map
import resource_locations as res
import music
from music import SoundManager


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
        program_icon = pygame.image.load(res.ICON_LOOP)
        pygame.display.set_icon(program_icon)
        pygame.display.set_caption("Indefinite Loop")
        self.game_data = GameData("game_data.json")
        self.gui = GUI(self.screen, self.game_data)
        self.map = Map(self.screen, self.game_data)
        self.sound = SoundManager(self.game_data)

    def game_loop(self):
        """Starts the game loop."""
        self.running = True
        music.load_music(res.MUSIC_BACKGROUND)
        self.sound.play_music()
        while self.running:
            self.clock.tick(self.FPS)
            self.render()
            self.run_events()

    def render(self):
        """Renders what's on the screen, depending on the game state. Calls either the GUI or the Map class."""
        if self.state == GameState.MainMenu:
            self.gui.draw_main_menu()
        if self.state == GameState.InGameMode0:
            self.map.draw_map()
        if self.state == GameState.PausedGameMode0:
            self.map.draw_map()
            self.gui.draw_pause_menu()
        if self.state == GameState.SettingsScreen:
            self.gui.draw_settings_menu()
        if self.state == GameState.HowToScreen:
            self.gui.draw_how_to()
        pygame.display.flip()

    def run_events(self):
        """Checks for all the events pygame might have fired."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == GameState.MainMenu:
                self.handle_event_main_menu(event)
            if self.state == GameState.InGameMode0:
                self.handle_event_in_game(event)
            if self.state == GameState.PausedGameMode0:
                self.handle_event_paused(event)
            if self.state == GameState.SettingsScreen:
                self.handle_event_settings_screen(event)
            if self.state == GameState.HowToScreen:
                self.handle_event_how_to(event)

    def handle_menu_events(self, event, mouse):
        """Handles all events that occur in any GUI menu (mouse events mostly)
        :type event: Event
        :type mouse: tuple"""
        if event.type == pygame.MOUSEMOTION:
            self.gui.check_button_hover(mouse)
        if event.type == pygame.MOUSEBUTTONUP:
            self.gui.click(mouse)

    def handle_event_main_menu(self, event):
        """Handles all events that need to be handled in the main menu."""
        mouse = pygame.mouse.get_pos()
        self.handle_menu_events(event, mouse)
        if event.type == events.START_GAME_MODE_0:
            self.state = GameState.InGameMode0
            self.map.set_level(event.level)
        if event.type == events.OPEN_SETTINGS:
            self.state = GameState.SettingsScreen
        if event.type == events.OPEN_HOW_TO:
            self.state = GameState.HowToScreen

    def handle_event_in_game(self, event):
        """Handles all events that need to be handled in game."""
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            self.map.handle_click(mouse, event.button)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.state = GameState.PausedGameMode0

    def handle_event_paused(self, event):
        """Handles all events that need to be handled while paused."""
        mouse = pygame.mouse.get_pos()
        self.handle_menu_events(event, mouse)
        if event.type == events.EXIT_PAUSE:
            self.state = GameState.InGameMode0
        if event.type == events.BACK_TO_MAIN_MENU:
            self.gui.level = self.map.level
            self.gui.update_level_buttons()
            self.state = GameState.MainMenu

    def handle_event_settings_screen(self, event):
        """Handles all events that need to be handled in the settings screen."""
        mouse = pygame.mouse.get_pos()
        self.handle_menu_events(event, mouse)
        if event.type == events.BACK_TO_MAIN_MENU:
            self.state = GameState.MainMenu

    def handle_event_how_to(self, event):
        """Handles all events in the how-to screen."""
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
            self.state = GameState.MainMenu
