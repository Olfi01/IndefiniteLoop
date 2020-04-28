# coding=utf-8
"""Contains the GUI class used for rendering menus. Calls the text helper for text rendering."""
import pygame
import text_helper
import events
from image_button import ImageButton
from button import Button
from game_data import GameData
from utility import center_horizontally, left_of, right_of
from text_button import TextButton
from colors import black, white, red
import resource_locations as res
from pygame import Surface
from enums import GameStyle
from music import SoundManager
import music


def scale_image_button(src):
    """Loads the image from the given file path and scales it to the size of an image button"""
    return pygame.transform.scale(pygame.image.load(src), (30, 30))


menu_fonts = ["Comic Sans MS", "Segoe Print"]
img_arrow_right = scale_image_button(res.IMG_ARROW_RIGHT)
img_arrow_right_hover = scale_image_button(res.IMG_ARROW_RIGHT_HOVER)
img_arrow_left = pygame.transform.flip(img_arrow_right, True, False)
img_arrow_left_hover = pygame.transform.flip(img_arrow_right_hover, True, False)
img_music_on = scale_image_button(res.IMG_MUSIC_ON)
img_music_on_hover = scale_image_button(res.IMG_MUSIC_ON_HOVER)
img_music_off = scale_image_button(res.IMG_MUSIC_OFF)
img_music_off_hover = scale_image_button(res.IMG_MUSIC_OFF_HOVER)
img_sound_on = scale_image_button(res.IMG_SOUND_ON)
img_sound_on_hover = scale_image_button(res.IMG_SOUND_ON_HOVER)
img_sound_off = scale_image_button(res.IMG_SOUND_OFF)
img_sound_off_hover = scale_image_button(res.IMG_SOUND_OFF_HOVER)


# Use like this: music_button_images[is_on][is_hover]
music_button_images = {
    True: {
        False: img_music_on,
        True: img_music_on_hover
    },
    False: {
        False: img_music_off,
        True: img_music_off_hover
    }
}


# Use like this: sound_button_images[is_on][is_hover]
sound_button_images = {
    True: {
        False: img_sound_on,
        True: img_sound_on_hover
    },
    False: {
        False: img_sound_off,
        True: img_sound_off_hover
    }
}


class GUI:
    """The GUI class. Used for rendering menus (main menu, level selection etc.)
    Called from the control unit."""
    def __init__(self, screen, game_data):
        """Initializes the GUI class and the connected surface. Takes the PyGame screen to be used as a parameter.
        :type screen: Surface
        :type game_data: GameData"""
        self.buttons = []
        self.level = 0
        self.max_level = 1
        self.screen = screen
        self.game_data = game_data
        self.sound = SoundManager(self.game_data)
        self.screen_dimensions = screen.get_size()
        self.main_menu_surface = None
        self.pause_menu_surface = None
        self.settings_menu_surface = None
        # 0: Level button, 1: Level down button, 2: Level up button
        self.level_buttons = []
        self.click_sound = pygame.mixer.Sound(res.SOUND_CLICK)
        # 0: Style button, 1: Music button, 2: Sound button
        self.settings_buttons = []

    def draw_main_menu(self):
        """Draws the main menu onto the screen each frame."""
        if self.main_menu_surface is None:
            self.init_main_menu_surface()
        self.main_menu_surface.fill(black)
        self.draw_title()
        for button in self.enabled_buttons():
            self.main_menu_surface.blit(button.get_rendered_button(), button.get_position())
        self.screen.blit(self.main_menu_surface, (0, 0))

    def draw_pause_menu(self):
        """Draws the pause menu over the game screen."""
        if self.pause_menu_surface is None:
            self.init_pause_menu()
        self.screen.blit(self.pause_menu_surface, (0, 0))
        title = text_helper.create_text("Pause", menu_fonts, 50, white)
        self.screen.blit(title, (center_horizontally(title, self.screen_dimensions), 50))
        for button in self.buttons:
            self.screen.blit(button.get_rendered_button(), button.get_position())

    def draw_settings_menu(self):
        """Draws the settings menu."""
        if self.settings_menu_surface is None:
            self.init_settings_menu()
        self.settings_menu_surface.fill(black)
        title = text_helper.create_text("Settings", menu_fonts, 50, white)
        self.settings_menu_surface.blit(title, (center_horizontally(title, self.screen_dimensions), 50))
        for button in self.buttons:
            self.settings_menu_surface.blit(button.get_rendered_button(), button.get_position())
        self.screen.blit(self.settings_menu_surface, (0, 0))

    def init_main_menu_surface(self):
        """Initializes the surface for the main menu, drawing the title and creating the buttons."""
        if self.level == 0:
            self.level = self.max_level = self.game_data.get_max_level()
        self.main_menu_surface = pygame.Surface(self.screen_dimensions)
        self.pause_menu_surface = None
        self.settings_menu_surface = None
        self.main_menu_surface.fill(black)
        self.buttons = []
        self.level_buttons = []
        level_button = TextButton((0, 450), "Level " + str(self.level), menu_fonts, 30, white, white, lambda: None)
        level_button.center_horizontally(self.screen_dimensions)
        self.level_buttons.append(level_button)
        self.buttons.append(level_button)
        level_down_button = ImageButton(left_of(img_arrow_left, level_button, 20),
                                        img_arrow_left, img_arrow_left_hover, self.level_down, False)
        self.level_buttons.append(level_down_button)
        self.buttons.append(level_down_button)
        level_up_button = ImageButton(right_of(img_arrow_right, level_button, 20),
                                      img_arrow_right, img_arrow_right_hover, self.level_up, False)
        self.level_buttons.append(level_up_button)
        self.update_level_buttons()
        self.buttons.append(level_up_button)
        # the line of code below creates a MenuButton that contains white text that gets red when hovered,
        # and sends an event to start game mode 0 for the control unit if clicked.
        start_button = TextButton((0, 500), "Start game", menu_fonts, 30, white, red,
                                  self.start_game_mode_0)
        start_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(start_button)
        settings_button = TextButton((0, 550), "Settings", menu_fonts, 30, white, red,
                                     lambda: pygame.event.post(pygame.event.Event(events.OPEN_SETTINGS, {})))
        settings_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(settings_button)
        quit_button = self.create_quit_button(600)
        self.buttons.append(quit_button)

    def init_pause_menu(self):
        """Initializes the pause menu."""
        self.pause_menu_surface = pygame.Surface(self.screen_dimensions)
        self.pause_menu_surface.set_alpha(240)
        self.pause_menu_surface.fill(black)
        self.main_menu_surface = None
        self.settings_menu_surface = None
        self.buttons = []
        continue_button = TextButton((0, 450), "Continue", menu_fonts, 30, white, red,
                                     lambda: pygame.event.post(pygame.event.Event(events.EXIT_PAUSE, {})))
        continue_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(continue_button)
        main_menu_button = TextButton((0, 500), "Back to main menu", menu_fonts, 30, white, red,
                                      lambda: pygame.event.post(pygame.event.Event(events.BACK_TO_MAIN_MENU, {})))
        main_menu_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(main_menu_button)
        quit_button = self.create_quit_button(550)
        self.buttons.append(quit_button)

    def init_settings_menu(self):
        """Initializes the settings menu."""
        self.settings_menu_surface = pygame.Surface(self.screen_dimensions)
        self.main_menu_surface = None
        self.pause_menu_surface = None
        self.buttons = []
        style_button = TextButton((0, 450), get_style_name(self.game_data.get_style()), menu_fonts, 30, white, red,
                                  self.switch_style)
        style_button.center_horizontally(self.screen_dimensions)
        self.settings_buttons.append(style_button)
        self.buttons.append(style_button)
        x_center = center_horizontally(pygame.Surface((0, 0)), self.screen_dimensions)
        music_button = ImageButton((x_center - 50, 510), self.get_music_button_img(), self.get_music_button_img_h(),
                                   self.toggle_music)
        self.settings_buttons.append(music_button)
        self.buttons.append(music_button)
        sound_button = ImageButton((x_center + 20, 510), self.get_sound_button_img(), self.get_sound_button_img_h(),
                                   self.toggle_sound)
        self.settings_buttons.append(sound_button)
        self.buttons.append(sound_button)
        main_menu_button = TextButton((0, 550), "Back to main menu", menu_fonts, 30, white, red,
                                      lambda: pygame.event.post(pygame.event.Event(events.BACK_TO_MAIN_MENU, {})))
        main_menu_button.center_horizontally(self.screen_dimensions)
        self.buttons.append(main_menu_button)

    def create_quit_button(self, y_pos):
        """Creates the quit button at the given y_pos. Used by both the init_main_menu and init_pause_menu methods."""
        quit_button = TextButton((0, y_pos), "Quit", menu_fonts, 30, white, red,
                                 lambda: pygame.event.post(pygame.event.Event(pygame.QUIT, {})))
        quit_button.center_horizontally(self.screen_dimensions)
        return quit_button

    def draw_title(self):
        """Draws the title onto the screen"""
        title = text_helper.create_text("Indefinite Loop", menu_fonts, 50, white)
        self.main_menu_surface.blit(title, (center_horizontally(title, self.screen_dimensions), 50))

    def check_button_hover(self, mouse_pos):
        """Notifies the GUI that the mouse has been moved and re-checks
        whether a button is currently being hovered over.
        :type mouse_pos: tuple"""
        for button in self.buttons:  # type: Button
            if button.is_position_on_button(mouse_pos):
                button.hover()
            else:
                button.un_hover()

    def click(self, mouse_pos):
        """Notifies the GUI that the mouse has clicked at a certain position.
        :type mouse_pos: tuple"""
        for button in self.enabled_buttons():  # type: Button
            if button.is_position_on_button(mouse_pos):
                self.sound.play_sound(self.click_sound)
                button.click()

    def level_down(self):
        """Sets the currently selected level one level down if possible."""
        if self.level > 1:
            self.level = self.level - 1
            self.update_level_buttons()

    def level_up(self):
        """Sets the currently selected level one level up if possible."""
        if self.level < self.max_level:
            self.level = self.level + 1
            self.update_level_buttons()

    def update_level_buttons(self):
        """Updates the text of the level button to match the level set and disables/enables the arrows if needed."""
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
        """Filters the buttons to only return the enabled ones. Used to make sure no disabled buttons can be clicked."""
        return filter(lambda x: x.is_enabled(), self.buttons)

    def start_game_mode_0(self):
        """Posts the start game event to the control unit."""
        pygame.event.post(pygame.event.Event(events.START_GAME_MODE_0, {"level": self.level}))

    def switch_style(self):
        """Switches through the styles by choosing the next one."""
        self.game_data.set_style(next_style[self.game_data.get_style()])
        self.settings_buttons[0].set_text(get_style_name(self.game_data.get_style()))

    def get_music_button_img(self):
        """Gets the music button image that corresponds to the current setting"""
        return music_button_images[self.game_data.is_music_on()][False]

    def get_music_button_img_h(self):
        """Gets the hovered music button image that corresponds to the current setting."""
        return music_button_images[self.game_data.is_music_on()][True]

    def get_sound_button_img(self):
        """Gets the sound button image that corresponds to the current setting"""
        return sound_button_images[self.game_data.is_sound_on()][False]

    def get_sound_button_img_h(self):
        """Gets the hovered sound button image that corresponds to the current setting."""
        return sound_button_images[self.game_data.is_sound_on()][True]

    def toggle_music(self):
        """Toggles the music setting (sets it to off if it's on, sets it to on if it's off)"""
        self.game_data.set_music_on(not self.game_data.is_music_on())
        self.settings_buttons[1].set_images(self.get_music_button_img(), self.get_music_button_img_h())
        if not self.game_data.is_music_on():
            music.stop_music()
        else:
            self.sound.play_music()

    def toggle_sound(self):
        """Toggles the sound setting (sets it to off if it's on, sets it to on if it's off)"""
        self.game_data.set_sound_on(not self.game_data.is_sound_on())
        self.settings_buttons[2].set_images(self.get_sound_button_img(), self.get_sound_button_img_h())


next_style = {
    GameStyle.Fancy: GameStyle.Simplistic,
    GameStyle.Simplistic: GameStyle.Fancy
}


style_names = {
    GameStyle.Fancy: "Fancy Style",
    GameStyle.Simplistic: "Simplistic Style"
}


def get_style_name(style):
    """Returns the name of the given style.
    :type style: GameStyle"""
    return style_names[style]
