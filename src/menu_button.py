"""Contains the menu button class. This class is used for abstraction and avoidance of redundant code."""
import text_helper
from utility import center_horizontally


class MenuButton:
    """The menu button class. Represents a button in a menu. Used by the GUI class."""
    def __init__(self, position, text, fonts, text_size, text_color, text_color_hover, on_click):
        """Initializes a new menu button.
        Takes the position, the text, the list of font preferences, the text size and the text color as parameters.
        :type position: tuple
        :type text: str
        :type fonts: list
        :type text_size: int
        :type text_color: tuple
        :type text_color_hover: tuple
        :type on_click: function"""
        self.position = position
        self.text = text
        self.fonts = fonts
        self.text_size = text_size
        self.text_color = text_color
        self.text_color_hover = text_color_hover
        self.on_click = on_click
        self.hovered = False

        self.renderedText = self.render_text()

    def render_text(self):
        """Renders the text differently dependent on whether the button is being hovered over or not.
        Returns the rendered text."""
        if self.hovered:
            text_color = self.text_color_hover
        else:
            text_color = self.text_color
        return text_helper.create_text(self.text, self.fonts, self.text_size, text_color)

    def hover(self):
        """Notifies the button that it's currently being hovered over."""
        if not self.hovered:
            self.hovered = True
            self.update()

    def un_hover(self):
        """Notifies the button that it's not being hovered over any more."""
        if self.hovered:
            self.hovered = False
            self.update()

    def update(self):
        """Updates the button (rendering)."""
        self.renderedText = self.render_text()

    def click(self):
        """Called when the button is clicked."""
        self.on_click()

    def get_rendered_button(self):
        """Returns the rendered image of the button."""
        return self.renderedText

    def get_position(self):
        """Returns the position of the button where it should be rendered."""
        return self.position

    def get_width(self):
        """Returns the width of the button."""
        return self.renderedText.get_width()

    def get_height(self):
        """Returns the height of the button."""
        return self.renderedText.get_height()

    def center_horizontally(self, screen_dimensions):
        self.position = (center_horizontally(self.renderedText, screen_dimensions), self.position[1])   # type: tuple

    def is_position_on_button(self, mouse_pos):
        return self.get_position()[0] < mouse_pos[0] < self.get_position()[0] + self.get_width() \
               and self.get_position()[1] < mouse_pos[1] < self.get_position()[1] + self.get_height()
