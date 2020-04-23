"""Contains the Map class that represents the in-game screen. Keeps track of the tiles and their rotation.
Takes care of rendering the in-game screen."""
from pygame import Surface
from game_data import GameData
from level_generator import generate_level, is_solved
import pygame
from enums import TileType
from tile import Tile
from colors import black


class Map:
    """Represents the map on which the game will be played.
    Takes care of rendering the in-game screen and the gameplay."""
    def __init__(self, screen, game_data):
        """Initializes a new instance of the map class.
        Takes the screen to draw on and the game data class as parameters.
        :type screen: Surface
        :type game_data: GameData"""
        self.screen = screen
        self.game_data = game_data
        self.level = 1
        self.level_map = generate_level(self.level)
        self.tile_shape = (self.screen.get_width() // self.level_map.shape[0],
                           self.screen.get_height() // self.level_map.shape[1])
        self.tiles = pygame.sprite.Group()
        self.map = pygame.Surface(self.screen.get_size())
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(black)
        self.click_sound = pygame.mixer.Sound("res/snap.wav")

    def draw_map(self):
        self.tiles.clear(self.map, self.background)
        self.tiles.update()
        self.tiles.draw(self.map)
        self.screen.blit(self.map, (0, 0))

    def handle_click(self, mouse_pos, button):
        if button != 1 and button != 3:
            return
        for tile in self.tiles:
            if tile.is_pos_on_tile(mouse_pos):
                self.click_sound.play()
                if button == 1:
                    tile.rotate_cw()
                else:
                    tile.rotate_ccw()
                self.level_map[tile.grid_pos] = tile.get_tile_as_num()
                self.check_level_solved()

    def check_level_solved(self):
        if is_solved(self.level_map):
            self.game_data.update_max_level_if_higher(self.level + 1)
            self.set_level(self.level + 1)

    def update_level_map(self):
        """Updates the level map after the level number has been set."""
        self.tiles.empty()
        for x in range(self.level_map.shape[0]):
            for y in range(self.level_map.shape[1]):
                i = (x, y)
                if self.level_map[i] == 0:
                    continue
                tile = create_tile(self.level_map[i], self.tile_shape,
                                   (x * self.tile_shape[0], y * self.tile_shape[1]), i)
                self.tiles.add(tile)

    def set_level(self, level):
        """Sets the level of the map and generates the map accordingly."""
        self.level = level
        self.level_map = generate_level(self.level)
        self.tile_shape = (self.screen.get_width() // self.level_map.shape[0],
                           self.screen.get_height() // self.level_map.shape[1])
        self.update_level_map()


tile_infos = {
    1: {"type": TileType.One, "rot": 3},
    2: {"type": TileType.One, "rot": 2},
    3: {"type": TileType.TwoCorner, "rot": 2},
    4: {"type": TileType.One, "rot": 1},
    5: {"type": TileType.TwoStraight, "rot": 1},
    6: {"type": TileType.TwoCorner, "rot": 1},
    7: {"type": TileType.Three, "rot": 1},
    8: {"type": TileType.One, "rot": 0},
    9: {"type": TileType.TwoCorner, "rot": 3},
    10: {"type": TileType.TwoStraight, "rot": 0},
    11: {"type": TileType.Three, "rot": 2},
    12: {"type": TileType.TwoCorner, "rot": 0},
    13: {"type": TileType.Three, "rot": 3},
    14: {"type": TileType.Three, "rot": 0},
    15: {"type": TileType.Four, "rot": 0},
}


def create_tile(tile, shape, pos, grid_pos):
    """Creates a tile corresponding to the given number (which represents a tile as explained in level_generator.py)
    Also takes the shape of the tile declaring width and height.
    :type tile: int
    :type shape: tuple
    :type pos: tuple
    :type grid_pos: tuple"""
    return Tile(tile_infos[tile]["type"], tile_infos[tile]["rot"], shape, pos, grid_pos)
