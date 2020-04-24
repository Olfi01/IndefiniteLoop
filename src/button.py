"""Contains the button class. This class is used for abstraction and avoidance of redundant code."""
from utility import center_horizontally


class Button:
    """The button class. Represents a text button in a menu. Used by the GUI class."""

    def __init__(self, position, on_click, enabled=True):
        """Initializes a new button.
        Takes the position and an on-click method as parameters.
        :type position: tuple
        :type on_click: function
        :type enabled: bool"""
        self.position = position
        self.on_click = on_click
        self.enabled = enabled
        self.hovered = False
        self.centered_h_dims = None

        self.rendered_image = self.render_image()

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
        self.rendered_image = self.render_image()
        if self.centered_h_dims is not None:
            self.center_horizontally(self.centered_h_dims)

    def render_image(self):
        """Renders the image of the button. Must be overridden in a derived class."""
        raise TypeError("render_image(self) needs to be overridden by the derived class.")

    def click(self):
        """Called when the button is clicked."""
        self.on_click()

    def get_rendered_button(self):
        """Returns the rendered image of the button."""
        return self.rendered_image

    def get_position(self):
        """Returns the position of the button where it should be rendered."""
        return self.position

    def get_width(self):
        """Returns the width of the button."""
        return self.rendered_image.get_width()

    def get_height(self):
        """Returns the height of the button."""
        return self.rendered_image.get_height()

    def center_horizontally(self, screen_dimensions):
        """Centers the button position horizontally relative to the given screen dimensions
        and sets the auto center flag to True.
        :type screen_dimensions: tuple"""
        self.centered_h_dims = screen_dimensions
        self.position = (center_horizontally(self.rendered_image, self.centered_h_dims),
                         self.position[1])  # type: tuple

    def un_center_horizontally(self):
        """Sets the auto center flag back to False."""
        self.centered_h_dims = None

    def is_position_on_button(self, mouse_pos):
        """Returns true if the given position is on the button itself.
        :type mouse_pos: tuple"""
        return self.get_position()[0] < mouse_pos[0] < self.get_position()[0] + self.get_width() \
            and self.get_position()[1] < mouse_pos[1] < self.get_position()[1] + self.get_height()

    def disable(self):
        """Disables the button."""
        self.enabled = False

    def enable(self):
        """Enables the button."""
        self.enabled = True

    def is_enabled(self):
        """Whether the button is enabled."""
        return self.enabled
