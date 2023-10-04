import collections
import copy
from enum import Enum
from typing import Generator

from Direction import Direction


class TileType(Enum):
    # INDEX 0 -> Identifier, INDEX 1 -> AMOUNT OF ROTATIONS
    # INDEX 2 -> WEIGHT

    # ...
    # ---
    # ...
    LINE = 0, 2, 55

    # ...
    # .--
    # .-.
    CORNER = 2, 4, 50

    # .-.
    # .--
    # .-.
    FORK = 3, 4, 50

    # .-.
    # ---
    # .-.
    CROSS = 4, 1, 50

    # .-.
    # ...
    # ...
    DEAD_END = 5, 4, 51

    # --< SPECIAL >--

    # ...
    # --.
    # ...
    SPECIAL_SINGLE_ROOM = 6, 4, 10

    # ...
    # --x
    # ...
    SPECIAL_BIG_ROOM_ENTRANCE = 7, 4, 0

    # ---
    # ---
    # ---
    SPECIAL_BIG_ROOM_MAIN = 8, 1, 0

    # -..
    # -..
    # -..
    SPECIAL_BIG_ROOM_WALL = 9, 4, 0

    # ---
    # -..
    # -..
    SPECIAL_BIG_ROOM_CORNER = 10, 4, 0

    # ...
    # ...
    # ...
    SPECIAL_EMPTY = -1, 1, 0

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
    def get_rotated_maze_tiles(cls) -> dict[str, dict[str, list[bool, bool, bool, bool]]]:
        base_maze_tiles = cls.get_maze_tiles()
        tiles = {}

        for base_maze_tile in base_maze_tiles:
            connections_deque = collections.deque(cls.get_connections(base_maze_tile))
            allowed_corners_deque = collections.deque(cls.get_allowed_corners(base_maze_tile))

            for rotation in range(0, base_maze_tile.value[1]):
                tiles[TileType.get_identifier(base_maze_tile, rotation)] = {
                    "connections": list(connections_deque),
                    "allowed_corners": list(allowed_corners_deque)
                }
                connections_deque.rotate(1)
                allowed_corners_deque.rotate(1)

        return tiles

    @classmethod
    def get_all_with_connection(cls, direction: Direction) -> Generator[tuple['TileType', int], None, None]:
        maze_tiles = cls.get_rotated_maze_tiles()

        for tile, obj in maze_tiles.items():
            if obj["connections"][direction.value]:
                yield [TileType.get_from_identifier(tile.split("_ROT_")[0]), int(tile.split("_")[-1])]

    @classmethod
    def get_all_without_connection(cls, direction: Direction) -> Generator[list['TileType', int], None, None]:
        maze_tiles = cls.get_rotated_maze_tiles()

        for tile, obj in maze_tiles.items():
            if not obj["connections"][direction.value]:
                yield [TileType.get_from_identifier(tile.split("_ROT_")[0]), int(tile.split("_")[-1])]

    @classmethod
    def get_all_rotations(cls, tile_type: 'TileType') -> list[list['TileType', int]]:
        rotated_tiles = []

        for rotation in range(tile_type.value[1]):
            rotated_tiles.append([tile_type, rotation])

        return rotated_tiles

    @staticmethod
    def get_identifier(tile_type: 'TileType', rotation: int) -> str:
        return f"{tile_type.name}_ROT_{rotation}"

    @classmethod
    def get_from_identifier(cls, identifier: str) -> 'TileType':
        return cls[identifier.split("_ROT_")[0]]

    @classmethod
    def get_connections(cls, tile_type: 'TileType', rotation: int = 0) -> list[bool, bool, bool, bool]:
        connections = collections.deque()

        match tile_type:
            case cls.LINE:
                connections.extend([False, True, False, True])
            case cls.CORNER:
                connections.extend([False, True, True, False])
            case cls.FORK:
                connections.extend([True, True, True, False])
            case cls.CROSS:
                connections.extend([True, True, True, True])
            case cls.DEAD_END:
                connections.extend([False, False, True, False])
            case _:
                return None

        connections.rotate(rotation)
        return list(connections)

    @classmethod
    def get_allowed_corners(cls, tile_type: 'TileType') -> list[bool, bool, bool, bool]:
        match tile_type:
            case cls.LINE:
                return [True, False, True, False]
            case cls.CORNER:
                return [True, False, False, True]
            case cls.FORK:
                return [False, False, False, True]
            case cls.DEAD_END:
                return [True, True, False, True]
            case cls.CROSS:
                return [False, False, False, False]
            case _:
                raise Exception(f"Tile Type {tile_type.name} does not have corners defined")

    @classmethod
    def get_type_from_connections(cls, connections: list[bool, bool, bool, bool]) -> tuple['TileType', int]:
        connections = collections.deque(connections)

        for i in range(4):
            match list(connections):
                case [False, True, False, True]:
                    return cls.LINE, i
                case [False, True, True, False]:
                    return cls.CORNER, i
                case [True, True, True, False]:
                    return cls.FORK, i
                case [True, True, True, True]:
                    return cls.CROSS, i
                case [False, False, True, False]:
                    return cls.DEAD_END, i
            connections.rotate(-1)

    @classmethod
    def get_all_tiles(cls) -> list[list['TileType', int]]:
        tile_types = []

        for tile_type in TileType:
            for rotation in range(0, tile_type.value[1]):
                tile_types.append([tile_type, rotation])

        return tile_types


class TemplateTile:
    def __init__(self, tile_type: TileType, connectable_tiles: dict[Direction, list[list[TileType, int]]],
                 rotation: int, allowed_corners: list[bool]):
        self.tile_type = tile_type
        self.connectable_tiles = connectable_tiles
        self.rotation = rotation
        self.allowed_corners = allowed_corners

    def __repr__(self):
        return f"TemplateTile<type: {self.tile_type} rotation: {self.rotation}>"


class TemplateTileManager:
    def __init__(self):
        self.tiles: list[TemplateTile] = []

    def add_tile(self, template_tile: TemplateTile):
        self.tiles.append(template_tile)

    def add_special_tile(self, tile_type: TileType, connections: dict[Direction, list[list[TileType, int]]],
                         allowed_corners: list[bool]) -> list[
        TemplateTile]:
        tiles = []

        rotated_connections = copy.copy(connections)
        switched_connections = copy.copy(connections)
        rotated_allowed_corners = collections.deque(allowed_corners)

        original_keys = connections.keys()
        rotated_keys = collections.deque(connections.keys())

        for rotation in range(0, tile_type.value[1]):
            tile = TemplateTile(
                tile_type,
                copy.deepcopy(switched_connections),
                rotation=rotation,
                allowed_corners=list(rotated_allowed_corners)
            )

            self.add_tile(tile)
            tiles.append(tile)

            rotated_keys.rotate(-1)
            rotated_allowed_corners.rotate(1)

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
        tile = list(filter(lambda t: t.tile_type == tile_type and t.rotation == rotation, self.tiles))
        return tile[0]
