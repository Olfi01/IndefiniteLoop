"""Contains the custom events used to signal things back to the control unit by the GUI or similar classes."""
import pygame


# an event that signals the control unit to start the game in mode 0
START_GAME_MODE_0 = pygame.USEREVENT + 1
EXIT_PAUSE = pygame.USEREVENT + 2
BACK_TO_MAIN_MENU = pygame.USEREVENT + 3
OPEN_SETTINGS = pygame.USEREVENT + 4
OPEN_HOW_TO = pygame.USEREVENT + 5
