import random
from typing import Optional

import pygame

from Config import Config
from TemplateTile import TileType, TemplateTile
from Tile import Tile, TileRepresenterBuilder


class WaveFunctionCollapse:
    def __init__(self, template_tile_manager):
        self.tiles: list[Tile] = []
        self.template_tile_manager = template_tile_manager

        for y in range(0, Config.SH // Config.CH):
            for x in range(0, Config.SW // Config.CW):
                self.tiles.append(Tile(x, y, template_tile_manager=template_tile_manager, wfc=self))

    def get_tile_at(self, x: int, y: int) -> Optional[Tile]:
        if x < 0 or x >= Config.SW // Config.CW:
            return None
        if y < 0 or y >= Config.SH // Config.CH:
            return None

        return self.tiles[x + y * (Config.SW // Config.CW)]

    def set_tile_at(self, x: int, y: int, template: TemplateTile):
        if x < 0 or x >= Config.SW // Config.CW:
            raise Exception("Set out of bounds")
        if y < 0 or y >= Config.SH // Config.CH:
            raise Exception("Set out of bounds")

        self.tiles[x + y * (Config.SW // Config.CW)].template_tile = template
        self.tiles[x + y * (Config.SW // Config.CW)].representer = TileRepresenterBuilder.from_tile(
            self.tiles[x + y * (Config.SW // Config.CW)])

    def get_lowest_entropy_tiles(self) -> list[Tile]:
        min_entropy = 100
        tiles = []

        for tile in self.tiles:
            if tile.template_tile.tile_type != TileType.EMPTY:
                continue

            if tile.entropy < min_entropy:
                tiles.clear()
                tiles.append(tile)
                min_entropy = tile.entropy
            elif tile.entropy == min_entropy:
                tiles.append(tile)

        return tiles

    def update(self):
        available_tiles = self.get_lowest_entropy_tiles()

        if len(available_tiles) == 0:
            return

        tile: Tile = random.choice(available_tiles)
        tile.collapse()

    def draw(self, screen: pygame.Surface):
        for tile in self.tiles:
            if tile.representer:
                tile.representer.draw(screen)
