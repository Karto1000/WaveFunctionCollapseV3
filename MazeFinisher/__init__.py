from __future__ import annotations

import collections
import random
import typing

import pygame

from Config import Config
from Direction import Direction
from TemplateTile import TileType

if typing.TYPE_CHECKING:
    from WFC import WaveFunctionCollapse
    from Tile import Tile


class MazeFinisher:
    def __init__(self, wfc: WaveFunctionCollapse):
        self.wfc: WaveFunctionCollapse = wfc
        self.current_tile: Tile = self.wfc.get_tile_at(0, 0)
        self.visited_tiles: list[Tile] = [self.current_tile]
        self.backtracking_tiles: list[Tile] = []

    def update(self):
        neighbors: dict[Direction, Tile] = {
            k: v for k, v in self.wfc.get_neighbors(self.current_tile).items() if
            v is not None and v not in self.visited_tiles and v not in self.backtracking_tiles
        }

        items = neighbors.items()
        random.shuffle(list(items))

        for direction, neighbor in items:
            not_rot_connections = TileType.get_connections(neighbor.template_tile.tile_type)

            # The neighbor is not a maze tile (CANNOT NAVIGATE TO IT)
            if not_rot_connections is None:
                continue

            rotated_connections = collections.deque(not_rot_connections)
            rotated_connections.rotate(neighbor.template_tile.rotation)

            # Check if the neighbor can connect to the current tile
            if rotated_connections[direction.get_opposite().value]:
                self.current_tile = neighbor
                self.visited_tiles.append(neighbor)
                break
        else:
            # If there is no neighbor to connect to
            maze_tiles = {k: t for k, t in neighbors.items() if
                          TileType.get_connections(t.template_tile.tile_type) is not None}

            if len(maze_tiles) == 0:
                self.backtrack()
                return

            random_tile = random.choice(list(maze_tiles.items()))

            # Connect the two tiles to the algorithm can continue
            self.wfc.connect_tiles(self.current_tile, random_tile[1], random_tile[0])
            self.current_tile = random_tile[1]
            self.visited_tiles.append(self.current_tile)

    def backtrack(self):
        if len(self.visited_tiles) == 0:
            return

        self.backtracking_tiles.append(self.current_tile)
        self.current_tile = self.visited_tiles.pop()

    def draw(self, screen: pygame.Surface):
        for visited_tile in self.visited_tiles:
            pygame.draw.rect(
                screen,
                (20, 20, 20),
                (visited_tile.x * Config.CW, visited_tile.y * Config.CH, Config.CW, Config.CH)
            )
