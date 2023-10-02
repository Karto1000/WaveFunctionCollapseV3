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
        maze_tile_types = TileType.get_maze_tiles()

        for maze_tile, connections in maze_tile_types.items():
            connectable_tiles = {Direction.UP: [], Direction.RIGHT: [], Direction.DOWN: [], Direction.LEFT: []}

            for direction in Direction:
                opposite_direction = direction.get_opposite()

                for _maze_tile, _connections in maze_tile_types.items():
                    if _maze_tile == maze_tile:
                        continue

                    if connections[direction.value] and _connections[opposite_direction.value]:
                        connectable_tiles[direction].append(_maze_tile)
                    elif not connections[direction.value] and not _connections[opposite_direction.value]:
                        connectable_tiles[direction].append(_maze_tile)

            for special_tile in self.registered_tiles:
                for direction in Direction:
                    if maze_tile in special_tile.connectable_tiles[direction]:
                        connectable_tiles[direction.get_opposite()].append(special_tile.tile_type)

            self.template_tile_manager.add_tile(TemplateTile(maze_tile, connectable_tiles), is_special=False)

    def register_special_tile(self, tile: TemplateTile):
        self.registered_tiles.append(tile)
