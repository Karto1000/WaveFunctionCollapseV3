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

    def add_rotation(self, old_rotation: int, amount: int) -> int:
        max_rotation = self.value[1]
        possible_out_of_bounds_rotation = old_rotation + amount
        return abs(possible_out_of_bounds_rotation % max_rotation)

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
    def get_all_with_connection(cls, direction: Direction) -> Generator[tuple['TileType', int], None, None]:
        maze_tiles = cls.get_rotated_maze_tiles()

        for tile, connection in maze_tiles.items():
            if connection is None:
                continue

            if connection[direction.value]:
                yield [TileType.get_from_identifier(tile.split("_ROT_")[0]), int(tile.split("_")[-1])]

    @classmethod
    def get_all_without_connection(cls, direction: Direction) -> Generator[list['TileType', int], None, None]:
        maze_tiles = cls.get_rotated_maze_tiles()

        for tile, connection in maze_tiles.items():
            if connection is None:
                continue

            if not connection[direction.value]:
                yield [TileType.get_from_identifier(tile.split("_ROT_")[0]), int(tile.split("_")[-1])]

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
    def get_all_tiles(cls) -> list[list['TileType', int]]:
        tile_types = []

        for tile_type in TileType:
            for rotation in range(0, tile_type.value[1]):
                tile_types.append([tile_type, rotation])

        return tile_types


class TemplateTile:
    def __init__(self, tile_type: TileType, connectable_tiles: dict[Direction, list[list[TileType, int]]],
                 rotation: int):
        self.tile_type = tile_type
        self.connectable_tiles = connectable_tiles
        self.rotation = rotation


class TemplateTileManager:
    def __init__(self):
        self.tiles: list[TemplateTile] = []

    def add_tile(self, template_tile: TemplateTile):
        self.tiles.append(template_tile)

    def add_special_tile(self, tile_type: TileType, connections: dict[Direction, list[list[TileType, int]]]) \
            -> list[TemplateTile]:
        tiles = []

        rotated_connections = copy.copy(connections)
        switched_connections = copy.copy(connections)

        original_keys = connections.keys()
        rotated_keys = collections.deque(connections.keys())

        for rotation in range(0, tile_type.value[1]):
            tile = TemplateTile(
                tile_type,
                copy.deepcopy(switched_connections),
                rotation=rotation
            )

            self.add_tile(tile)
            tiles.append(tile)

            rotated_keys.rotate(-1)

            for rotated_key, original_key in zip(rotated_keys, original_keys):
                switched_connections[rotated_key] = rotated_connections[original_key]

            # Shift the rotation of each TileType by 1
            for direction in Direction:
                for connection in rotated_connections[direction]:
                    connection[1] = connection[0].add_rotation(connection[1], 1)

        return tiles

    def check_all_tiles_defined(self):
        added_tile_types = list(map(lambda t: t.tile_type, self.tiles))

        for tile_type in TileType.get_maze_tiles():
            if tile_type not in added_tile_types:
                raise Exception(f"Tile Type {tile_type} was not defined")

    def get_template_tile(self, tile_type: TileType, rotation: int = 0) -> TemplateTile:
        tile = list(filter(lambda t: t.tile_type == tile_type, self.tiles))
        tile[0].rotation = rotation
        return tile[0]
