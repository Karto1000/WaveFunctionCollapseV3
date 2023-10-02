import time

from Config import Config
import pygame

from Direction import Direction
from MazeBuilder import MazeBuilder
from TemplateTile import TemplateTileManager, TemplateTile, TileType
from WFC import WaveFunctionCollapse

pygame.init()
SCREEN = pygame.display.set_mode((Config.SW, Config.SH))
CLOCK = pygame.time.Clock()

template_tile_manager = TemplateTileManager()
maze_builder = MazeBuilder(template_tile_manager)

template_tile_manager.add_tile(
    TemplateTile(
        TileType.EMPTY,
        {
            Direction.UP: [*TileType],
            Direction.RIGHT: [*TileType],
            Direction.DOWN: [*TileType],
            Direction.LEFT: [*TileType]
        }
    ),
    is_special=False
)

SINGLE_ROOM_TILE = TemplateTile(
    TileType.SINGLE_ROOM,
    {
        Direction.UP: list(TileType.get_all_without_connection(Direction.DOWN)),
        Direction.RIGHT: list(TileType.get_all_without_connection(Direction.LEFT)),
        Direction.LEFT: list(TileType.get_all_with_connection(Direction.RIGHT)),
        Direction.DOWN: list(TileType.get_all_without_connection(Direction.UP))
    }
)

maze_builder.register_special_tile(SINGLE_ROOM_TILE)
maze_builder.construct()

template_tile_manager.add_tile(SINGLE_ROOM_TILE)
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

    try:
        wfc.update()
    except Exception as e:
        pygame.draw.rect(
            SCREEN,
            (122, 122, 122),
            (e.args[0] * Config.CW, e.args[1] * Config.CH, Config.CW, Config.CH)
        )

    wfc.draw(SCREEN)

    pygame.display.flip()
