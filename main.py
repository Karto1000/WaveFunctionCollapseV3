from Config import Config
import pygame

from Direction import Direction
from MazeBuilder import MazeBuilder
from TemplateTile import TemplateTileManager, TileType
from WFC import WaveFunctionCollapse

pygame.init()
SCREEN = pygame.display.set_mode((Config.SW, Config.SH))
CLOCK = pygame.time.Clock()

template_tile_manager = TemplateTileManager()
maze_builder = MazeBuilder(template_tile_manager)

template_tile_manager.add_special_tile(
    TileType.SPECIAL_EMPTY,
    {
        Direction.UP: TileType.get_all_tiles(),
        Direction.RIGHT: TileType.get_all_tiles(),
        Direction.DOWN: TileType.get_all_tiles(),
        Direction.LEFT: TileType.get_all_tiles()
    }
)

tiles = template_tile_manager.add_special_tile(
    TileType.SPECIAL_SINGLE_ROOM,
    {
        Direction.UP: list(TileType.get_all_without_connection(Direction.DOWN)),
        Direction.RIGHT: list(TileType.get_all_without_connection(Direction.LEFT)),
        Direction.DOWN: list(TileType.get_all_without_connection(Direction.UP)),
        Direction.LEFT: list(TileType.get_all_with_connection(Direction.RIGHT))
    }
)

for tile in tiles:
    maze_builder.register_special_tile(tile)

maze_builder.construct()

template_tile_manager.check_all_tiles_defined()
wfc = WaveFunctionCollapse(template_tile_manager)

while True:
    CLOCK.tick(Config.FPS)
    SCREEN.fill((255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    wfc.update()
    wfc.draw(SCREEN)

    pygame.display.flip()
