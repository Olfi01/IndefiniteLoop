"""Contains the GUI class used for rendering menus. Calls the text helper for text rendering."""
import pygame
import text_helper
import events
from utility import center_horizontally
from menu_button import MenuButton


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 40, 40)
menu_fonts = ["Comic Sans MS", "Segoe Print"]


class GUI:
    """The GUI class. Used for rendering menus (main menu, level selection etc.)
    Called from the control unit."""
    def __init__(self, screen):
        """Initializes the GUI class and the connected surface. Takes the PyGame screen to be used as a parameter."""
        self.buttons = []
        self.screen = screen    # type: pygame.Surface
        self.screen_dimensions = screen.get_size()
        self.main_menu_surface = None

    def draw_main_menu(self):
        """Draws the main menu onto the screen each frame."""
        if self.main_menu_surface is None:
            self.init_main_menu_surface()
        for button in self.buttons:
            self.main_menu_surface.blit(button.get_rendered_button(), button.get_position())
        self.screen.blit(self.main_menu_surface, (0, 0))

    def init_main_menu_surface(self):
        """Initializes the surface for the main menu, drawing the title and creating the buttons."""
        self.main_menu_surface = pygame.Surface(self.screen_dimensions)
        self.main_menu_surface.fill(black)
        self.buttons = []
        title = text_helper.create_text("Indefinite Loop", menu_fonts, 50, white)
        self.main_menu_surface.blit(title, (center_horizontally(title, self.screen_dimensions), 50))
        # the line of code below creates a MenuButton that contains white text that gets red when hovered,
        # and sends an event to start game mode 0 for the control unit if clicked.
        start_button = MenuButton((0, 500), "Start game", menu_fonts, 30, white, red,
                                  lambda: pygame.event.post(pygame.event.Event(events.START_GAME_MODE_0, {})))
        start_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(start_button)
        quit_button = MenuButton((0, 550), "Quit", menu_fonts, 30, white, red,
                                 lambda: pygame.event.post(pygame.event.Event(pygame.QUIT, {})))
        quit_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(quit_button)

    def check_button_hover(self, mouse_pos):
        """Notifies the GUI that the mouse has been moved and re-checks
        whether a button is currently being hovered over"""
        for button in self.buttons:  # type: MenuButton
            if button.is_position_on_button(mouse_pos):
                button.hover()
            else:
                button.un_hover()

    def click(self, mouse_pos):
        """Notifies the GUI that the mouse has clicked at a certain position."""
        for button in self.buttons:  # type: MenuButton
            if button.is_position_on_button(mouse_pos):
                button.click()
