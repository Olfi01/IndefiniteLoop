"""A package that contains all the enums used by the game."""
from enum import Enum, IntEnum


class GameState(Enum):
    """Represents the state of the game. At first, only MainMenu and InGameMode0 will ever be used."""
    MainMenu = 0,
    InGameMode0 = 1,
    InLevelEditor = 2,
    InGameMode1 = 3,
    PausedGameMode0 = 4,
    SettingsScreen = 5


class TileType(Enum):
    """Represents the type of a tile. Named after the number of connections it has."""
    One = 0,
    TwoStraight = 1,
    TwoCorner = 2,
    Three = 3,
    Four = 4


class GameStyle(IntEnum):
    """Represents the style that the game currently uses."""
    Fancy = 0,
    Simplistic = 1
