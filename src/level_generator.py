"""The level generator used for the level layouts. The level number is taken as a seed
to ensure that the levels are the same for everyone.
Every tile is represented by a number in the following fashion:
5 = 0b0101, with each bit representing whether or not there is a collection in the respective direction.
The first bit (starting from the right!) is for left, the second for up, the third for right and the fourth for down."""
from src.utility import is_kth_bit_set
import random
import numpy as np


def generate_level(level):
    """Generates the level with the given number.
    Returns it as a 2d numpy array containing the tiles represented as explained above.
    This method could be tested by giving it a random number and checking whether the returned array is a valid level
    with a valid solution.
    :type level: int"""
    seed = level * 69420   # multiply by 69420 to not have the seeds too close to each other
    random.seed(seed)
    dimensions = get_map_size(level)
    level_map = np.full(dimensions, -1)
    while -1 in level_map:
        choice = random.choice(np.argwhere(level_map == -1))
        next_index = (choice[0], choice[1])
        # get indices of the tiles next to the current index
        left_index, up_index, right_index, down_index = get_direction_indices(next_index)
        left = tile_needs_connection(left_index, level_map, has_connection_right)
        up = tile_needs_connection(up_index, level_map, has_connection_down)
        right = tile_needs_connection(right_index, level_map, has_connection_left)
        down = tile_needs_connection(down_index, level_map, has_connection_up)
        level_map[next_index] = get_tile(left, up, right, down)
    return un_solve(level_map)


def un_solve(level_map):
    """Randomly spins all the tiles to make the level unsolved.
    This method could be tested by giving it a level that is solved,
    and checking whether the level returned is not solved."""
    for x in range(level_map.shape[0]):
        for y in range(level_map.shape[1]):
            i = (x, y)
            if level_map[i] == 0 or level_map[i] == 0b1111:
                continue    # no need to spin empty tiles or tiles with connections to all sides
            level_map[i] = rotate_random(level_map[i])
    if not is_solved(level_map):
        return level_map
    # For this method to be infinitely recursive (which would be bad) there would have to be a level without any tiles,
    # which has a probability of 1/16 to the power of the number of possible tiles in the level, in other words:
    # Near impossible. Near enough to not go the additional length of handling that case.
    return un_solve(level_map)


def is_solved(level_map):
    """Returns true if the given level map is solved (meaning there is no more dangling connection)"""
    shape = level_map.shape
    for x in range(shape[0]):
        for y in range(shape[1]):
            i = (x, y)
            tile = level_map[i]
            if tile == 0:
                continue
            left_index, up_index, right_index, down_index = get_direction_indices(i)
            if has_connection_left(tile) and \
                    (tile_is_out_of_borders(left_index, shape) or not has_connection_right(level_map[left_index])):
                return False
            if has_connection_up(tile) and \
                    (tile_is_out_of_borders(up_index, shape) or not has_connection_down(level_map[up_index])):
                return False
            if has_connection_right(tile) and \
                    (tile_is_out_of_borders(right_index, shape) or not has_connection_left(level_map[right_index])):
                return False
            if has_connection_down(tile) and \
                    (tile_is_out_of_borders(down_index, shape) or not has_connection_up(level_map[down_index])):
                return False
    return True


def rotate_random(tile):
    """Rotates a tile either by 0, 90, 180 or 270 degrees. Returns the rotated tile.
    :type tile: int"""
    return rotate(tile, random.choice([0, 1, 2, 3]))


def rotate(tile, n):
    """Rotates a tile by n steps clockwise. Returns the rotated tile.
    :type tile: int
    :type n: int"""
    return 0b1111 & (tile << n | tile >> (4 - n))


def get_tile(left, up, right, down):
    """Returns the numeric value for the tile, determined by whether or not it has connections in given directions.
    :type left: int
    :type up: int
    :type right: int
    :type down: int"""
    tile = 0
    if left:
        tile += 1
    if up:
        tile += 2
    if right:
        tile += 4
    if down:
        tile += 8
    return tile


def tile_needs_connection(index, level_map, adjacent_has_connection):
    """Returns True if the tile needs a connection to the given index, False if it must not have one.
    If neither is the case, returns a random value of either True or False.
    Takes the index, the map, and the function in which direction to check for an existing connection.
    :type index: tuple
    :type level_map: ndarray
    :type adjacent_has_connection: function"""
    if tile_is_out_of_borders(index, level_map.shape):
        return False
    if tile_is_set(index, level_map):
        return adjacent_has_connection(level_map[index])
    return random.choice([True, False])


def tile_is_out_of_borders(index, shape):
    """Returns True if the index is out of the borders defined by shape, False if not.
    :type index: tuple
    :type shape: tuple"""
    return index[0] < 0 or index[1] < 0 or index[0] >= shape[0] or index[1] >= shape[1]


def tile_is_set(index, level_map):
    """Returns True if the tile at the given index of the map is set, False if not."""
    return level_map[index] != -1


def get_direction_indices(next_index):
    """Returns the indices next to the current one, in the following order: left, up, right, down
    :type next_index: tuple"""
    left = (next_index[0] - 1, next_index[1])
    up = (next_index[0], next_index[1] - 1)
    right = (next_index[0] + 1, next_index[1])
    down = (next_index[0], next_index[1] + 1)
    return left, up, right, down


def get_map_size(level):
    """Returns the dimensions of the map to be used for the given level.
    :type level: int"""
    if level < 5:
        return 5, 5
    if level < 70:
        return 10, 10
    if level < 150:
        return 25, 25
    return 50, 50


def has_connection_left(tile):
    """Returns true if the given tile has a connection to the left side.
    :type tile: int"""
    return is_kth_bit_set(tile, 1)


def has_connection_up(tile):
    """Returns true if the given tile has a connection to the upper side.
    :type tile: int"""
    return is_kth_bit_set(tile, 2)


def has_connection_right(tile):
    """Returns true if the given tile has a connection to the right side.
    :type tile: int"""
    return is_kth_bit_set(tile, 3)


def has_connection_down(tile):
    """Returns true if the given tile has a connection to the lower side.
    :type tile: int"""
    return is_kth_bit_set(tile, 4)
