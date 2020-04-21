"""A helper class for rendering text.
Caches fonts and rendered text images to reduce load on the system when rendering stuff like menus."""
import pygame


def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x: x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


__font_cache = {}


def get_font(font_preferences, size):
    key = str(font_preferences) + '|' + str(size)
    font = __font_cache.get(key, None)
    if font is None:
        font = make_font(font_preferences, size)
        __font_cache[key] = font
    return font


__text_cache = {}


def create_text(text, fonts, size, color):
    """creates a text image from input text, uses caching"""
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = __text_cache.get(key, None)
    if image is None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        __text_cache[key] = image
    return image
