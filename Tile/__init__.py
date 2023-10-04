import copy
import random

from Direction import Direction
from TemplateTile import TemplateTile, TileType
from Tile.TileRepresenter import TileRepresenterBuilder


class Tile:
    def __init__(self, x: int, y: int, *, template_tile_manager, wfc):
        self.x, self.y = x, y
        self.available_tiles: list[TemplateTile] = copy.copy(template_tile_manager.tiles)
        self.template_tile_manager = template_tile_manager
        self.wfc = wfc
        self.template_tile: TemplateTile = copy.copy(template_tile_manager.get_template_tile(TileType.SPECIAL_EMPTY))
        self.representer: TileRepresenter = None

    @property
    def entropy(self):
        return len(self.available_tiles)

    def set_template_tile(self, template_tile: TemplateTile):
        self.template_tile = template_tile
        self.representer = TileRepresenterBuilder.from_tile(self)

    def collapse(self, override_type: TemplateTile = None):
        if self.entropy == 0:
            raise Exception(self.x, self.y)

        if override_type is not None:
            self.set_template_tile(override_type)
        else:
            sorted_tiles = sorted(self.available_tiles, key=lambda t: t.tile_type.value[2], reverse=True)
            for available_tile in sorted_tiles:
                if random.randrange(0, 100) <= available_tile.tile_type.value[2]:
                    self.set_template_tile(available_tile)
                    break
            else:
                self.set_template_tile(random.choice(sorted_tiles))

        neighbors = {
            Direction.UP: self.wfc.get_tile_at(self.x, self.y - 1),
            Direction.RIGHT: self.wfc.get_tile_at(self.x + 1, self.y),
            Direction.DOWN: self.wfc.get_tile_at(self.x, self.y + 1),
            Direction.LEFT: self.wfc.get_tile_at(self.x - 1, self.y)
        }

        for direction, neighbor in neighbors.items():
            if not neighbor:
                continue

            valid_tiles = self.template_tile.connectable_tiles[direction]

            new_tiles = []

            for available_tile in neighbor.available_tiles:
                if [available_tile.tile_type, available_tile.rotation] in valid_tiles:
                    new_tiles.append(available_tile)

            neighbor.available_tiles = new_tiles

    def __repr__(self):
        return f"Tile<x: {self.x}, y: {self.y}>"
