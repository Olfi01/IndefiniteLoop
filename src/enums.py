"""A package that contains all the enums used by the game."""
from enum import Enum


class GameState(Enum):
    """Represents the state of the game. At first, only MainMenu and InGameMode0 will ever be used."""
    MainMenu = 0,
    InGameMode0 = 1,
    InLevelEditor = 2,
    InGameMode1 = 3
