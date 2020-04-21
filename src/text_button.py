"""Contains the text button class. This class is used for abstraction and avoidance of redundant code."""
import text_helper
from button import Button


class TextButton(Button):
    """The text button class. Represents a text button in a menu. Used by the GUI class."""
    def __init__(self, position, text, fonts, text_size, text_color, text_color_hover, on_click):
        """Initializes a new text button.
        Takes the position, the text, the list of font preferences, the text size, the text color,
        and an on-click method as parameters.
        :type position: tuple
        :type text: str
        :type fonts: list
        :type text_size: int
        :type text_color: tuple
        :type text_color_hover: tuple
        :type on_click: function"""
        self.text = text
        self.fonts = fonts
        self.text_size = text_size
        self.text_color = text_color
        self.text_color_hover = text_color_hover
        Button.__init__(self, position, on_click)

    def set_text(self, text):
        """Sets the text of this button to the new text.
        :type text: str"""
        self.text = text
        self.update()

    def render_image(self):
        """Renders the text differently dependent on whether the button is being hovered over or not.
        Returns the rendered text."""
        if self.hovered:
            text_color = self.text_color_hover
        else:
            text_color = self.text_color
        return text_helper.create_text(self.text, self.fonts, self.text_size, text_color)
