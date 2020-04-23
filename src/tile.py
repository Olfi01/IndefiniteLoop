"""Contains the Tile class, which is used to display a single tile on the map"""
from pygame.sprite import Sprite
from enums import TileType
import pygame


TURN_SPEED = 10  # 90 NEEDS to be divisible by this, or else the animation will bug


class Tile(Sprite):
    """Represents one tile on the game map."""
    def __init__(self, tile_type, rotation, shape, pos, grid_pos):
        """Initializes a new Tile with the given type, rotation and size.
        Rotation can be either 0, 1, 2 or 3.
        Rotation is counted counterclockwise from the original image.
        Size is the number of pixels the image should be wide and high.
        :type tile_type: TileType
        :type rotation: int
        :type shape: tuple
        :type pos: tuple
        :type grid_pos: tuple"""
        Sprite.__init__(self)
        self.tile_type = tile_type
        self.rotation = rotation
        self.animated_rotation = self.rotation * 90
        self.shape = shape
        self.pos = pos
        self.grid_pos = grid_pos
        self.image = get_image_for(self.tile_type, self.animated_rotation, self.shape)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.animation_running = 0

    def update(self):
        if self.animation_running != 0:
            step = TURN_SPEED * (self.animation_running / abs(self.animation_running))
            self.animated_rotation += step
            self.animation_running -= step
            self.update_image()

    def rotate_cw(self):
        """Rotates the sprite clockwise by 90 degrees."""
        self.rotation -= 1
        if self.rotation < 0:
            self.rotation = 3
        self.animation_running -= 90
        self.update_image()

    def rotate_ccw(self):
        """Rotates the sprite counterclockwise by 90 degrees"""
        self.rotation += 1
        if self.rotation > 3:
            self.rotation = 0
        self.animation_running += 90
        self.update_image()

    def update_image(self):
        """Updates the image of the sprite."""
        self.image = get_image_for(self.tile_type, self.animated_rotation, self.shape)
        self.rect = self.image.get_rect()   # type: pygame.Rect
        self.rect.centerx = self.pos[0] + (self.shape[0] / 2)
        self.rect.centery = self.pos[1] + (self.shape[1] / 2)

    def is_pos_on_tile(self, pos):
        """Returns true if the given position is on this tile. Used for click recognition."""
        return self.pos[0] < pos[0] < self.pos[0] + self.shape[0] and self.pos[1] < pos[1] < self.pos[1] + self.shape[1]

    def get_tile_as_num(self):
        return get_tile_as_num(self.tile_type, self.rotation)


tile_info = {
    TileType.Four: [15, 15, 15, 15],
    TileType.Three: [14, 7, 11, 13],
    TileType.TwoStraight: [10, 5, 10, 5],
    TileType.TwoCorner: [12, 6, 3, 9],
    TileType.One: [8, 4, 2, 1]
}


def get_tile_as_num(tile_type, rotation):
    """Returns the tile encoded as a number, as described in level_generator.py
    :type tile_type: TileType
    :type rotation: int"""
    return tile_info[tile_type][rotation]


cached_images = {}


def get_image_for(tile_type, rotation, shape):
    """Returns the image for the given tile type, rotation and size.
    Rotation can be either 0, 1, 2 or 3.
    Rotation is counted counterclockwise from the original image.
    Size is the number of pixels the image should be wide and high.
    :type tile_type: TileType
    :type rotation: int
    :type shape: tuple"""
    key = (tile_type, rotation, shape)
    if key not in cached_images:
        key2 = (tile_type, 0, shape)
        if key2 not in cached_images:
            if tile_type not in cached_images:
                cached_images[tile_type] = load_image(tile_type)
            cached_images[key2] = pygame.transform.scale(cached_images[tile_type], shape)
        cached_images[key] = pygame.transform.rotate(cached_images[key2], rotation)
    return cached_images[key]


base_images = {
    TileType.One: "res/one.png",
    TileType.TwoCorner: "res/two_corner.png",
    TileType.TwoStraight: "res/two_straight.png",
    TileType.Three: "res/three.png",
    TileType.Four: "res/four.png"
}


def load_image(tile_type):
    """Loads the base image for the given tile type.
    :type tile_type: TileType"""
    return pygame.image.load(base_images[tile_type])
