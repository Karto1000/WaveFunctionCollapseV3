import numpy as numpy

from Direction import Direction
from TemplateTile import TemplateTileManager, TileType, TemplateTile


class MazeTile:
    def __init__(self, tile_type: TileType):
        self.tile_type = tile_type


class MazeBuilder:
    def __init__(self, template_tile_manager: TemplateTileManager):
        self.template_tile_manager = template_tile_manager
        self.registered_tiles: list[TemplateTile] = []

    def construct(self):
        maze_tile_types = TileType.get_rotated_maze_tiles()

        for maze_tile_type, obj in maze_tile_types.items():
            connectable_tiles = {Direction.UP: [], Direction.RIGHT: [], Direction.DOWN: [], Direction.LEFT: []}
            rotation = int(maze_tile_type.split("_")[-1])
            connections = obj["connections"]
            allowed_corners = obj["allowed_corners"]

            for direction in Direction:
                opposite_direction = direction.get_opposite()

                for neighbor_tile_type, neighbor_obj in maze_tile_types.items():
                    neighbor_rotation = int(neighbor_tile_type.split("_")[-1])
                    neighbor_connections = neighbor_obj["connections"]

                    if connections[direction.value] and neighbor_connections[opposite_direction.value]:
                        connectable_tiles[direction].append(
                            [TileType.get_from_identifier(neighbor_tile_type), neighbor_rotation])
                    elif not connections[direction.value] and not neighbor_connections[opposite_direction.value]:
                        connectable_tiles[direction].append(
                            [TileType.get_from_identifier(neighbor_tile_type), neighbor_rotation])

            for special_tile in self.registered_tiles:
                for direction in Direction:
                    if [TileType.get_from_identifier(maze_tile_type), rotation] in special_tile.connectable_tiles[
                        direction.get_opposite()]:
                        connectable_tiles[direction].append([special_tile.tile_type, special_tile.rotation])

            self.template_tile_manager.add_tile(
                TemplateTile(
                    TileType.get_from_identifier(maze_tile_type),
                    connectable_tiles,
                    rotation=rotation,
                    allowed_corners=allowed_corners
                )
            )

    def register_special_tile(self, tile: TemplateTile):
        self.registered_tiles.append(tile)
