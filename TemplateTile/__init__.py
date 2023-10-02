from enum import Enum
from typing import Generator

from Direction import Direction


class TileType(Enum):
    EMPTY = -1, 50

    # MAZE
    UP_DOWN = 0, 50
    RIGHT_LEFT = 1, 50
    UP_RIGHT = 2, 50
    UP_LEFT = 3, 50
    DOWN_RIGHT = 4, 50
    DOWN_LEFT = 5, 50
    FORK_UP_RIGHT = 6, 50
    FORK_UP_LEFT = 7, 50
    FORK_RIGHT_DOWN = 8, 50
    FORK_RIGHT_UP = 9, 50
    CROSS = 10, 50
    UP_DEAD_END = 11, 50
    RIGHT_DEAD_END = 12, 50
    DOWN_DEAD_END = 13, 50
    LEFT_DEAD_END = 14, 50

    # SPECIAL
    SINGLE_ROOM = 15, 35

    @classmethod
    def get_maze_tiles(cls) -> dict['TileType', list[bool]]:
        return {
            cls.UP_DOWN: [True, False, True, False],
            cls.RIGHT_LEFT: [False, True, False, True],
            cls.UP_RIGHT: [False, True, True, False],
            cls.UP_LEFT: [False, False, True, True],
            cls.DOWN_RIGHT: [True, True, False, False],
            cls.DOWN_LEFT: [True, False, False, True],
            cls.FORK_UP_RIGHT: [True, True, True, False],
            cls.FORK_UP_LEFT: [True, False, True, True],
            cls.FORK_RIGHT_DOWN: [False, True, True, True],
            cls.FORK_RIGHT_UP: [True, True, False, True],
            cls.CROSS: [True, True, True, True],
            cls.UP_DEAD_END: [False, False, True, False],
            cls.RIGHT_DEAD_END: [False, False, False, True],
            cls.DOWN_DEAD_END: [True, False, False, False],
            cls.LEFT_DEAD_END: [False, True, False, False],
        }

    @classmethod
    def get_all_with_connection(cls, direction: Direction) -> Generator['TileType', None, None]:
        maze_tiles = cls.get_maze_tiles()

        for tile, connection in maze_tiles.items():
            if connection[direction.value]:
                yield tile

    @classmethod
    def get_all_without_connection(cls, *directions: Direction) -> Generator['TileType', None, None]:
        maze_tiles = cls.get_maze_tiles()

        for tile, connection in maze_tiles.items():
            for direction in directions:
                if not connection[direction.value]:
                    yield tile
                    break


class TemplateTile:
    def __init__(self, tile_type: TileType, connectable_tiles: dict[Direction, list[TileType]]):
        self.tile_type = tile_type
        self.connectable_tiles = connectable_tiles


class TemplateTileManager:
    def __init__(self):
        self.tiles: list[TemplateTile] = []
        self.special_tiles: list[TemplateTile] = []

    def add_tile(self, template_tile: TemplateTile, *, is_special: bool = True):
        if is_special:
            self.special_tiles.append(template_tile)
        else:
            self.tiles.append(template_tile)

    def check_all_tiles_defined(self):
        added_tile_types = list(map(lambda t: t.tile_type, self.tiles))
        added_special_tile_types = list(map(lambda t: t.tile_type, self.special_tiles))

        for tile_type in TileType:
            if tile_type not in added_tile_types and tile_type not in added_special_tile_types:
                raise Exception(f"Tile Type {tile_type} was not defined")

    def get_template_tile(self, tile_type: TileType) -> TemplateTile:
        tile = list(filter(lambda t: t.tile_type == tile_type, self.tiles))

        if len(tile) == 0:
            tile = list(filter(lambda t: t.tile_type == tile_type, self.special_tiles))

        return tile[0]
