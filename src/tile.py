"""Contains the Tile class, which is used to display a single tile on the map"""
from pygame.sprite import Sprite
from enums import TileType, GameStyle
import pygame
import resource_locations as res


TURN_SPEED = 10  # 90 NEEDS to be divisible by this, or else the animation will bug


class Tile(Sprite):
    """Represents one tile on the game map."""
    def __init__(self, tile_type, rotation, shape, pos, grid_pos, style):
        """Initializes a new Tile with the given type, rotation and size.
        Rotation can be either 0, 1, 2 or 3.
        Rotation is counted counterclockwise from the original image.
        Size is the number of pixels the image should be wide and high.
        :type tile_type: TileType
        :type rotation: int
        :type shape: tuple
        :type pos: tuple
        :type grid_pos: tuple
        :type style: GameStyle"""
        Sprite.__init__(self)
        self.tile_type = tile_type
        self.rotation = rotation
        self.animated_rotation = self.rotation * 90
        self.shape = shape
        self.pos = pos
        self.grid_pos = grid_pos
        self.style = style
        self.image = get_image_for(self.tile_type, self.animated_rotation, self.shape, self.style)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.animation_running = 0

    def update(self):
        """Updates the tile. Used for the rotation animation."""
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
        self.image = get_image_for(self.tile_type, self.animated_rotation, self.shape, self.style)
        self.rect = self.image.get_rect()   # type: pygame.Rect
        self.rect.centerx = self.pos[0] + (self.shape[0] / 2)
        self.rect.centery = self.pos[1] + (self.shape[1] / 2)

    def is_pos_on_tile(self, pos):
        """Returns true if the given position is on this tile. Used for click recognition."""
        return self.pos[0] < pos[0] < self.pos[0] + self.shape[0] and self.pos[1] < pos[1] < self.pos[1] + self.shape[1]

    def get_tile_as_num(self):
        """Returns this tile encoded as a number, as explained in level_generator.py"""
        return get_tile_as_num(self.tile_type, self.rotation)


tile_info = {
    TileType.Four: [0b1111, 0b1111, 0b1111, 0b1111],
    TileType.Three: [0b1110, 0b0111, 0b1011, 0b1101],
    TileType.TwoStraight: [0b1010, 0b0101, 0b1010, 0b0101],
    TileType.TwoCorner: [0b1100, 0b0110, 0b0011, 0b1001],
    TileType.One: [0b1000, 0b0100, 0b0010, 0b0001]
}


def get_tile_as_num(tile_type, rotation):
    """Returns the tile encoded as a number, as described in level_generator.py
    :type tile_type: TileType
    :type rotation: int"""
    return tile_info[tile_type][rotation]


cached_images = {}


def get_image_for(tile_type, rotation, shape, style):
    """Returns the image for the given tile type, rotation and size.
    Rotation can be either 0, 1, 2 or 3.
    Rotation is counted counterclockwise from the original image.
    Size is the number of pixels the image should be wide and high.
    :type tile_type: TileType
    :type rotation: int
    :type shape: tuple
    :type style: GameStyle"""
    key = (tile_type, rotation, shape, style)
    if key not in cached_images:
        key2 = (tile_type, 0, shape, style)
        if key2 not in cached_images:
            if (tile_type, style) not in cached_images:
                cached_images[(tile_type, style)] = load_image(tile_type, style)
            cached_images[key2] = pygame.transform.scale(cached_images[(tile_type, style)], shape)
        cached_images[key] = pygame.transform.rotate(cached_images[key2], rotation)
    return cached_images[key]


base_images = {
    GameStyle.Fancy: {
        TileType.One: res.IMG_ONE,
        TileType.TwoCorner: res.IMG_TWO_CORNER,
        TileType.TwoStraight: res.IMG_TWO_STRAIGHT,
        TileType.Three: res.IMG_THREE,
        TileType.Four: res.IMG_FOUR
    },
    GameStyle.Simplistic: {
        TileType.One: res.IMG_ONE,
        TileType.TwoCorner: res.IMG_TWO_CORNER_S,
        TileType.TwoStraight: res.IMG_TWO_STRAIGHT_S,
        TileType.Three: res.IMG_THREE_S,
        TileType.Four: res.IMG_FOUR_S
    }
}


def load_image(tile_type, style):
    """Loads the base image for the given tile type.
    :type tile_type: TileType
    :type style: GameStyle"""
    return pygame.image.load(base_images[style][tile_type])
