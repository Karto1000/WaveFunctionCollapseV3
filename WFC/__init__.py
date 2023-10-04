import collections
import random
import time
from typing import Optional

import pygame

from Config import Config
from Direction import Direction
from TemplateTile import TileType, TemplateTile, TemplateTileManager
from Tile import Tile, TileRepresenterBuilder


class WaveFunctionCollapse:
    def __init__(self, template_tile_manager):
        self.tiles: list[Tile] = []
        self.template_tile_manager: TemplateTileManager = template_tile_manager
        self.is_finished = False

        for y in range(0, Config.SH // Config.CH):
            for x in range(0, Config.SW // Config.CW):
                new_tile = Tile(x, y, template_tile_manager=template_tile_manager, wfc=self)
                self.tiles.append(new_tile)

                new_available_tiles = new_tile.available_tiles.copy()

                if x == 0:
                    for tile in new_tile.available_tiles:
                        # IF IT CANT CONNECT TO LEFT WALL
                        if not tile.allowed_corners[3] and tile in new_available_tiles:
                            new_available_tiles.remove(tile)

                if x == Config.SW // Config.CW - 1:
                    for tile in new_tile.available_tiles:
                        # IF IT CANT CONNECT TO RIGHT WALL
                        if not tile.allowed_corners[1] and tile in new_available_tiles:
                            new_available_tiles.remove(tile)

                if y == 0:
                    for tile in new_tile.available_tiles:
                        # IF IT CANT CONNECT TO TOP WALL
                        if not tile.allowed_corners[0] and tile in new_available_tiles:
                            new_available_tiles.remove(tile)
                if y == Config.SH // Config.CH - 1:
                    for tile in new_tile.available_tiles:
                        # IF IT CANT CONNECT TO Bottom WALL
                        if not tile.allowed_corners[2] and tile in new_available_tiles:
                            new_available_tiles.remove(tile)

                new_tile.available_tiles = new_available_tiles

    def get_tile_at(self, x: int, y: int) -> Optional[Tile]:
        if x < 0 or x >= Config.SW // Config.CW:
            return None
        if y < 0 or y >= Config.SH // Config.CH:
            return None

        return self.tiles[x + y * (Config.SW // Config.CW)]

    def get_neighbors(self, tile: Tile) -> dict[Direction, Optional[Tile]]:
        return {
            Direction.UP: self.get_tile_at(tile.x, tile.y - 1),
            Direction.RIGHT: self.get_tile_at(tile.x + 1, tile.y),
            Direction.DOWN: self.get_tile_at(tile.x, tile.y + 1),
            Direction.LEFT: self.get_tile_at(tile.x - 1, tile.y)
        }

    def set_tile_at(self, x: int, y: int, template: TemplateTile):
        if x < 0 or x >= Config.SW // Config.CW:
            raise Exception("Set out of bounds")
        if y < 0 or y >= Config.SH // Config.CH:
            raise Exception("Set out of bounds")

        self.tiles[x + y * (Config.SW // Config.CW)].template_tile = template
        self.tiles[x + y * (Config.SW // Config.CW)].representer = TileRepresenterBuilder.from_tile(
            self.tiles[x + y * (Config.SW // Config.CW)])

    def connect_tiles(self, connect_from: Tile, connect_to: Tile, direction: Direction):
        """
        Connect two maze tiles **IMPORTANT** The tiles MUST be maze tiles and have a valid connection

        :param connect_from: The first tile to connect
        :param connect_to: The second tile to connect
        """

        connect_from_type = connect_from.template_tile.tile_type
        connect_to_type = connect_to.template_tile.tile_type

        connect_from_connections = TileType.get_connections(
            connect_from_type,
            rotation=connect_from.template_tile.rotation
        )
        connect_to_connections = TileType.get_connections(
            connect_to_type,
            rotation=connect_to.template_tile.rotation
        )

        if not connect_from_connections or not connect_to_connections:
            raise ValueError(
                f"First or Second tile type is not a maze tile first_tile_type: "
                f"{connect_from_type} "
                f"second_tile_type: {connect_to_type}")

        connect_from_connections[direction.value] = True
        connect_to_connections[direction.get_opposite().value] = True

        new_from = TileType.get_type_from_connections(connect_from_connections)
        new_to = TileType.get_type_from_connections(connect_to_connections)

        self.set_tile_at(
            connect_from.x,
            connect_from.y,
            self.template_tile_manager.get_template_tile(new_from[0], new_from[1])
        )

        self.set_tile_at(
            connect_to.x,
            connect_to.y,
            self.template_tile_manager.get_template_tile(new_to[0], new_to[1])
        )

    def get_lowest_entropy_tiles(self) -> list[Tile]:
        min_entropy = 100
        tiles = []

        for tile in self.tiles:
            if tile.template_tile.tile_type != TileType.SPECIAL_EMPTY:
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
            self.is_finished = True
            return

        tile: Tile = random.choice(available_tiles)
        tile.collapse()

    def draw(self, screen: pygame.Surface):
        for tile in self.tiles:
            if tile.representer:
                tile.representer.draw(screen)
