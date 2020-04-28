"""Contains the Map class that represents the in-game screen. Keeps track of the tiles and their rotation.
Takes care of rendering the in-game screen."""
import math
from pygame import Surface
from game_data import GameData
from level_generator import generate_level, is_solved
import pygame
from enums import TileType, GameStyle
import tile as tile_module
from tile import Tile
from colors import black, green
import resource_locations as res
from music import SoundManager


DONE_ANIM_SPEED = 30


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
        self.sound = SoundManager(self.game_data)
        self.map = pygame.Surface(self.screen.get_size())
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(black)
        self.click_sound = pygame.mixer.Sound(res.SOUND_SNAP)
        self.done = False
        self.done_c_rad = - ((90 // tile_module.TURN_SPEED) * DONE_ANIM_SPEED)
        self.diag = math.sqrt(pow(self.map.get_width(), 2) + pow(self.map.get_height(), 2))
        self.center = (self.map.get_width() // 2, self.map.get_height() // 2)

    def draw_map(self):
        """Draws the map on the screen each tick"""
        self.tiles.clear(self.map, self.background)
        self.tiles.update()
        if self.done:
            if self.done_c_rad < self.diag:
                self.done_c_rad += DONE_ANIM_SPEED
            if self.done_c_rad >= 0:
                pygame.draw.circle(self.map, green, self.center, self.done_c_rad)
        self.tiles.draw(self.map)
        self.screen.blit(self.map, (0, 0))

    def handle_click(self, mouse_pos, button):
        """Handles the click event sent by pygame. Used to rotate the tiles and to advance a level if done."""
        if button != 1 and button != 3:
            return
        if self.done:
            self.set_level(self.level + 1)
            self.reset_done()
            return
        for tile in self.tiles:
            if tile.is_pos_on_tile(mouse_pos):
                self.sound.play_sound(self.click_sound)
                if button == 1:
                    tile.rotate_cw()
                else:
                    tile.rotate_ccw()
                self.level_map[tile.grid_pos] = tile.get_tile_as_num()
                self.check_level_solved()

    def check_level_solved(self):
        """Checks whether the current level is solved and sets the map to done if it is."""
        if is_solved(self.level_map):
            self.game_data.update_max_level_if_higher(self.level + 1)
            self.set_done()

    def set_done(self):
        """Notifies the map class that the level was completed, but the player didn't advance to the next level yet."""
        self.done = True
        self.sound.play_sound(pygame.mixer.Sound(res.SOUND_SUCCESS))

    def reset_done(self):
        """Notifies the map class that the player did advance to the next level."""
        self.done = False
        self.done_c_rad = - ((90 // tile_module.TURN_SPEED) * DONE_ANIM_SPEED)  # The delay for the success animation
        # is calculated in a way that it starts when the turn animation of the tile ends

    def update_level_map(self):
        """Updates the level map after the level number has been set."""
        self.tiles.empty()
        self.map.blit(self.background, (0, 0))
        for x in range(self.level_map.shape[0]):
            for y in range(self.level_map.shape[1]):
                i = (x, y)
                if self.level_map[i] == 0:
                    continue
                tile = create_tile(self.level_map[i], self.tile_shape,
                                   (x * self.tile_shape[0], y * self.tile_shape[1]), i, self.game_data.get_style())
                self.tiles.add(tile)

    def set_level(self, level):
        """Sets the level of the map and generates the map accordingly."""
        self.level = level
        self.level_map = generate_level(self.level)
        self.tile_shape = (self.screen.get_width() // self.level_map.shape[0],
                           self.screen.get_height() // self.level_map.shape[1])
        self.update_level_map()


tile_infos = {
    0b0001: {"type": TileType.One, "rot": 3},
    0b0010: {"type": TileType.One, "rot": 2},
    0b0011: {"type": TileType.TwoCorner, "rot": 2},
    0b0100: {"type": TileType.One, "rot": 1},
    0b0101: {"type": TileType.TwoStraight, "rot": 1},
    0b0110: {"type": TileType.TwoCorner, "rot": 1},
    0b0111: {"type": TileType.Three, "rot": 1},
    0b1000: {"type": TileType.One, "rot": 0},
    0b1001: {"type": TileType.TwoCorner, "rot": 3},
    0b1010: {"type": TileType.TwoStraight, "rot": 0},
    0b1011: {"type": TileType.Three, "rot": 2},
    0b1100: {"type": TileType.TwoCorner, "rot": 0},
    0b1101: {"type": TileType.Three, "rot": 3},
    0b1110: {"type": TileType.Three, "rot": 0},
    0b1111: {"type": TileType.Four, "rot": 0},
}


def create_tile(tile, shape, pos, grid_pos, style):
    """Creates a tile corresponding to the given number (which represents a tile as explained in level_generator.py)
    Also takes the shape of the tile declaring width and height.
    :type tile: int
    :type shape: tuple
    :type pos: tuple
    :type grid_pos: tuple
    :type style: GameStyle"""
    return Tile(tile_infos[tile]["type"], tile_infos[tile]["rot"], shape, pos, grid_pos, style)
