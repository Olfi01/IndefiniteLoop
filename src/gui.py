# coding=utf-8
"""Contains the GUI class used for rendering menus. Calls the text helper for text rendering."""
import pygame
import text_helper
import events
from image_button import ImageButton
from src.button import Button
from src.game_data import GameData
from utility import center_horizontally, left_of, right_of
from text_button import TextButton
from colors import black, white, red


menu_fonts = ["Comic Sans MS", "Segoe Print"]
arrow_right = pygame.transform.scale(pygame.image.load("res/arrow_right.png"), (30, 30))
arrow_right_hover = pygame.transform.scale(pygame.image.load("res/arrow_right_hover.png"), (30, 30))
arrow_left = pygame.transform.flip(arrow_right, True, False)
arrow_left_hover = pygame.transform.flip(arrow_right_hover, True, False)


class GUI:
    """The GUI class. Used for rendering menus (main menu, level selection etc.)
    Called from the control unit."""
    def __init__(self, screen, game_data):
        """Initializes the GUI class and the connected surface. Takes the PyGame screen to be used as a parameter.
        :type screen: pygame.Surface
        :type game_data: game_data.GameData"""
        self.buttons = []
        self.level = 1
        self.max_level = 1
        self.screen = screen    # type: pygame.Surface
        self.game_data = game_data  # type: GameData
        self.screen_dimensions = screen.get_size()
        self.main_menu_surface = None
        # 0: Level button, 1: Level down button, 2: Level up button
        self.level_buttons = []

    def draw_main_menu(self):
        """Draws the main menu onto the screen each frame."""
        if self.main_menu_surface is None:
            self.init_main_menu_surface()
        self.main_menu_surface.fill(black)
        self.draw_title()
        for button in self.enabled_buttons():
            self.main_menu_surface.blit(button.get_rendered_button(), button.get_position())
        self.screen.blit(self.main_menu_surface, (0, 0))

    def init_main_menu_surface(self):
        """Initializes the surface for the main menu, drawing the title and creating the buttons."""
        self.level = self.max_level = self.game_data.get_max_level()
        self.main_menu_surface = pygame.Surface(self.screen_dimensions)
        self.main_menu_surface.fill(black)
        self.buttons = []
        level_button = TextButton((0, 450), "Level " + str(self.level), menu_fonts, 30, white, white, lambda: None)
        level_button.center_horizontally(self.screen_dimensions)
        self.level_buttons.append(level_button)
        self.buttons.append(level_button)
        level_down_button = ImageButton(left_of(arrow_left, level_button, 20),
                                        arrow_left, arrow_left_hover, self.level_down, False)
        self.level_buttons.append(level_down_button)
        self.buttons.append(level_down_button)
        level_up_button = ImageButton(right_of(arrow_right, level_button, 20),
                                      arrow_right, arrow_right_hover, self.level_up, False)
        self.level_buttons.append(level_up_button)
        self.update_level_buttons()
        self.buttons.append(level_up_button)
        # the line of code below creates a MenuButton that contains white text that gets red when hovered,
        # and sends an event to start game mode 0 for the control unit if clicked.
        start_button = TextButton((0, 500), "Start game", menu_fonts, 30, white, red,
                                  self.start_game_mode_0)
        start_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(start_button)
        quit_button = TextButton((0, 550), "Quit", menu_fonts, 30, white, red,
                                 lambda: pygame.event.post(pygame.event.Event(pygame.QUIT, {})))
        quit_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(quit_button)

    def draw_title(self):
        title = text_helper.create_text("Indefinite Loop", menu_fonts, 50, white)
        self.main_menu_surface.blit(title, (center_horizontally(title, self.screen_dimensions), 50))

    def check_button_hover(self, mouse_pos):
        """Notifies the GUI that the mouse has been moved and re-checks
        whether a button is currently being hovered over"""
        for button in self.buttons:  # type: Button
            if button.is_position_on_button(mouse_pos):
                button.hover()
            else:
                button.un_hover()

    def click(self, mouse_pos):
        """Notifies the GUI that the mouse has clicked at a certain position."""
        for button in self.enabled_buttons():  # type: Button
            if button.is_position_on_button(mouse_pos):
                button.click()

    def level_down(self):
        if self.level > 1:
            self.level = self.level - 1
            self.update_level_buttons()

    def level_up(self):
        if self.level < self.max_level:
            self.level = self.level + 1
            self.update_level_buttons()

    def update_level_buttons(self):
        self.level_buttons[0].set_text("Level " + str(self.level))
        if self.level <= 1:
            self.level_buttons[1].disable()
        else:
            self.level_buttons[1].enable()
        if self.level >= self.max_level:
            self.level_buttons[2].disable()
        else:
            self.level_buttons[2].enable()

    def enabled_buttons(self):
        return filter(lambda x: x.is_enabled(), self.buttons)

    def start_game_mode_0(self):
        pygame.event.post(pygame.event.Event(events.START_GAME_MODE_0, {"level": self.level}))
