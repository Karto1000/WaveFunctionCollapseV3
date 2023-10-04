import random

from Config import Config
import pygame

from Direction import Direction
from MazeBuilder import MazeBuilder
from MazeFinisher import MazeFinisher
from TemplateTile import TemplateTileManager, TileType
from WFC import WaveFunctionCollapse

pygame.init()
SCREEN = pygame.display.set_mode((Config.SW, Config.SH))
CLOCK = pygame.time.Clock()

template_tile_manager = TemplateTileManager()
maze_builder = MazeBuilder(template_tile_manager)

random.seed(Config.SEED)


def define_special_tiles():
    template_tile_manager.add_special_tile(
        TileType.SPECIAL_EMPTY,
        {
            Direction.UP: TileType.get_all_tiles(),
            Direction.RIGHT: TileType.get_all_tiles(),
            Direction.DOWN: TileType.get_all_tiles(),
            Direction.LEFT: TileType.get_all_tiles()
        },
        allowed_corners=[True, True, True, True]
    )

    for tile in template_tile_manager.add_special_tile(
            TileType.SPECIAL_SINGLE_ROOM,
            {
                Direction.UP: list(TileType.get_all_without_connection(Direction.DOWN)),
                Direction.RIGHT: list(TileType.get_all_without_connection(Direction.LEFT)),
                Direction.DOWN: list(TileType.get_all_without_connection(Direction.UP)),
                Direction.LEFT: list(TileType.get_all_with_connection(Direction.RIGHT))
            },
            allowed_corners=[True, True, True, False]
    ):
        maze_builder.register_special_tile(tile)

    for tile in template_tile_manager.add_special_tile(
            TileType.SPECIAL_BIG_ROOM_ENTRANCE,
            {
                Direction.UP: [[TileType.SPECIAL_BIG_ROOM_CORNER, 0], [TileType.SPECIAL_BIG_ROOM_WALL, 0]],
                Direction.RIGHT: [[TileType.SPECIAL_BIG_ROOM_MAIN, 0]],
                Direction.DOWN: [[TileType.SPECIAL_BIG_ROOM_CORNER, 3], [TileType.SPECIAL_BIG_ROOM_WALL, 0]],
                Direction.LEFT: list(TileType.get_all_with_connection(Direction.RIGHT))
            },
            allowed_corners=[False, False, False, False]
    ):
        maze_builder.register_special_tile(tile)

    template_tile_manager.add_special_tile(
        TileType.SPECIAL_BIG_ROOM_MAIN,
        {
            Direction.UP: [[TileType.SPECIAL_BIG_ROOM_MAIN, 0], [TileType.SPECIAL_BIG_ROOM_ENTRANCE, 1],
                           [TileType.SPECIAL_BIG_ROOM_WALL, 1]],
            Direction.RIGHT: [[TileType.SPECIAL_BIG_ROOM_MAIN, 0], [TileType.SPECIAL_BIG_ROOM_ENTRANCE, 2],
                              [TileType.SPECIAL_BIG_ROOM_WALL, 2]],
            Direction.DOWN: [[TileType.SPECIAL_BIG_ROOM_MAIN, 0], [TileType.SPECIAL_BIG_ROOM_ENTRANCE, 3],
                             [TileType.SPECIAL_BIG_ROOM_WALL, 3]],
            Direction.LEFT: [[TileType.SPECIAL_BIG_ROOM_MAIN, 0], [TileType.SPECIAL_BIG_ROOM_ENTRANCE, 0],
                             [TileType.SPECIAL_BIG_ROOM_WALL, 0]]

        },
        allowed_corners=[False, False, False, False]
    )

    template_tile_manager.add_special_tile(
        TileType.SPECIAL_BIG_ROOM_WALL,
        {
            Direction.UP: [[TileType.SPECIAL_BIG_ROOM_CORNER, 0], [TileType.SPECIAL_BIG_ROOM_WALL, 0]],
            Direction.RIGHT: [[TileType.SPECIAL_BIG_ROOM_MAIN, 0]],
            Direction.DOWN: [[TileType.SPECIAL_BIG_ROOM_CORNER, 3], [TileType.SPECIAL_BIG_ROOM_WALL, 0]],
            Direction.LEFT: list(TileType.get_all_without_connection(Direction.RIGHT))
        },
        allowed_corners=[False, False, False, True]
    )

    template_tile_manager.add_special_tile(
        TileType.SPECIAL_BIG_ROOM_CORNER,
        {
            Direction.UP: list(TileType.get_all_without_connection(Direction.DOWN)),
            Direction.RIGHT: [[TileType.SPECIAL_BIG_ROOM_CORNER, 1], [TileType.SPECIAL_BIG_ROOM_WALL, 1]],
            Direction.DOWN: [[TileType.SPECIAL_BIG_ROOM_CORNER, 3], [TileType.SPECIAL_BIG_ROOM_WALL, 0]],
            Direction.LEFT: list(TileType.get_all_without_connection(Direction.RIGHT))
        },
        allowed_corners=[True, False, False, True]
    )


define_special_tiles()
maze_builder.construct()

template_tile_manager.check_all_tiles_defined()
wfc = WaveFunctionCollapse(template_tile_manager)
maze_finisher = MazeFinisher(wfc)

wfc.get_tile_at(Config.SW // Config.CW // 4, Config.SH // Config.CH // 4).collapse(
    override_type=template_tile_manager.get_template_tile(TileType.SPECIAL_BIG_ROOM_ENTRANCE))
wfc.get_tile_at(Config.SW // Config.CW // 4 * 3, Config.SH // Config.CH // 4).collapse(
    override_type=template_tile_manager.get_template_tile(TileType.SPECIAL_BIG_ROOM_ENTRANCE))
wfc.get_tile_at(Config.SW // Config.CW // 4, Config.SH // Config.CH // 4 * 3).collapse(
    override_type=template_tile_manager.get_template_tile(TileType.SPECIAL_BIG_ROOM_ENTRANCE))
wfc.get_tile_at(Config.SW // Config.CW // 4 * 3, Config.SH // Config.CH // 4 * 3).collapse(
    override_type=template_tile_manager.get_template_tile(TileType.SPECIAL_BIG_ROOM_ENTRANCE))

while True:
    CLOCK.tick(Config.FPS)
    SCREEN.fill((255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    if not wfc.is_finished:
        wfc.update()
    else:
        maze_finisher.update()
        maze_finisher.draw(SCREEN)

    wfc.draw(SCREEN)

    pygame.display.flip()
