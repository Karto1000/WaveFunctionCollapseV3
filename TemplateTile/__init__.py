import collections
import copy
from enum import Enum
from typing import Generator

from Direction import Direction


class TileType(Enum):
    # INDEX 0 -> Identifier, INDEX 1 -> AMOUNT OF ROTATIONS

    # ...
    # ---
    # ...
    LINE = 0, 2

    # ...
    # .--
    # .-.
    CORNER = 2, 4

    # .-.
    # .--
    # .-.
    FORK = 3, 4

    # .-.
    # ---
    # .-.
    CROSS = 4, 1

    # .-.
    # ...
    # ...
    DEAD_END = 5, 4

    # --< SPECIAL >--
    SPECIAL_SINGLE_ROOM = 6, 4
    SPECIAL_EMPTY = -1, 1

    @classmethod
    def get_maze_tiles(cls) -> dict['TileType', list[bool, bool, bool, bool]]:
        tiles = {}

        for tile_type in TileType:
            if tile_type.name.startswith("SPECIAL"):
                continue

            tiles[tile_type] = cls.get_connections(tile_type)

        return tiles

    @classmethod
    def get_rotated_maze_tiles(cls) -> dict[str, list[bool, bool, bool, bool]]:
        base_maze_tiles = cls.get_maze_tiles()
        tiles = {}

        for base_maze_tile in base_maze_tiles:
            if base_maze_tile.name.startswith("SPECIAL"):
                continue

            deque = collections.deque(cls.get_connections(base_maze_tile))
            for rotation in range(0, base_maze_tile.value[1]):
                tiles[TileType.get_identifier(base_maze_tile, rotation)] = list(deque)
                deque.rotate(1)

        return tiles

    @classmethod
    def get_all_with_connection(cls, direction: Direction) -> Generator['TileType', None, None]:
        maze_tiles = cls.get_maze_tiles()

        for tile, connection in maze_tiles.items():
            if connection is None:
                continue

            if connection[direction.value]:
                yield tile

    @classmethod
    def get_all_without_connection(cls, *directions: Direction) -> Generator['TileType', None, None]:
        maze_tiles = cls.get_maze_tiles()

        for tile, connection in maze_tiles.items():
            if connection is None:
                continue

            for direction in directions:
                if not connection[direction.value]:
                    yield tile
                    break

    @staticmethod
    def get_identifier(tile_type: 'TileType', rotation: int) -> str:
        return f"{tile_type.name}_ROT_{rotation}"

    @classmethod
    def get_from_identifier(cls, identifier: str) -> 'TileType':
        return cls[identifier.split("_ROT_")[0]]

    @classmethod
    def get_connections(cls, tile_type: 'TileType') -> list[bool, bool, bool, bool]:
        match tile_type:
            case cls.LINE:
                return [False, True, False, True]
            case cls.CORNER:
                return [False, True, True, False]
            case cls.FORK:
                return [True, True, True, False]
            case cls.CROSS:
                return [True, True, True, True]
            case cls.DEAD_END:
                return [False, False, True, False]

    @classmethod
    def get_all_tiles(cls) -> list[tuple['TileType', int]]:
        tile_types = []

        for tile_type in TileType:
            for rotation in range(0, tile_type.value[1]):
                tile_types.append((tile_type, rotation))

        return tile_types


class TemplateTile:
    def __init__(self, tile_type: TileType, connectable_tiles: dict[Direction, list[tuple[TileType, int]]],
                 rotation: int):
        self.tile_type = tile_type
        self.connectable_tiles = connectable_tiles
        self.rotation = rotation


class TemplateTileManager:
    def __init__(self):
        self.tiles: list[TemplateTile] = []

    def add_tile(self, template_tile: TemplateTile):
        self.tiles.append(template_tile)

    def add_special_tile(self, tile_type: TileType, connection: dict[Direction, list[tuple[TileType, int]]]):
        for rotation in range(0, tile_type.value[1]):
            new_keys = collections.deque(connection.keys())
            new_keys.rotate(rotation)

            new_connections = {}
            for key in new_keys:
                new_connections[key] = connection[key]

            self.add_tile(
                TemplateTile(
                    tile_type,
                    new_connections,
                    rotation=rotation
                )
            )

    def check_all_tiles_defined(self):
        added_tile_types = list(map(lambda t: t.tile_type, self.tiles))

        for tile_type in TileType.get_maze_tiles():
            if tile_type not in added_tile_types:
                raise Exception(f"Tile Type {tile_type} was not defined")

    def get_template_tile(self, tile_type: TileType, rotation: int = 0) -> TemplateTile:
        tile = list(filter(lambda t: t.tile_type == tile_type, self.tiles))
        tile[0].rotation = rotation
        return tile[0]
