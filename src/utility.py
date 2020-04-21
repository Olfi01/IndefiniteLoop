"""Provides helper functions to the code, to avoid redundant code.
For example, takes care of centering text or images."""


def center_horizontally(image, dimensions):
    """Returns the horizontal coordinate needed to center the image horizontally."""
    return dimensions[0] // 2 - image.get_width() // 2
