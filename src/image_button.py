"""Contains the image button class. Used to avoid redundant code."""
import pygame

from button import Button


class ImageButton(Button):
    """Represents a button based on an image. Used by the GUI class."""
    def __init__(self, position, image, image_hovered, on_click, enabled=True):
        """Initializes a new image button. Takes the position, the path of the image,
        the path of the image when hovered and an on-click method as parameters,
        as well as a boolean indicating whether the button is disabled.
        :type position: tuple
        :type on_click: function
        :type enabled: bool"""
        self.image = image
        self.image_hovered = image_hovered
        Button.__init__(self, position, on_click, enabled)

    def render_image(self):
        """Returns the image to render, depending on whether it's being hovered or not."""
        if self.hovered:
            return self.image_hovered
        else:
            return self.image
