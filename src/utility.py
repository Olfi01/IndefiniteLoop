"""Provides helper functions to the code, to avoid redundant code.
For example, takes care of centering text or images."""


def center_horizontally(image, dimensions):
    """Returns the horizontal coordinate needed to center the image horizontally."""
    return dimensions[0] // 2 - image.get_width() // 2


def left_of(image, button, distance):
    """Returns the coordinates needed to have the image next to the given button with the given distance.
    :type image: pygame.Surface
    :type button: button.Button
    :type distance: int"""
    return button.get_position()[0] - image.get_width() - distance, \
        button.get_position()[1] + (button.get_height() // 2) - (image.get_height() // 2)


def right_of(image, button, distance):
    """Returns the coordinates needed to have the image next to the given button with the given distance.
    :type image: pygame.Surface
    :type button: button.Button
    :type distance: int"""
    return button.get_position()[0] + button.get_width() + distance, \
        button.get_position()[1] + (button.get_height() // 2) - (image.get_height() // 2)
