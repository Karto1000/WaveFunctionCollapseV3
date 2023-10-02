from __future__ import annotations

import abc
import typing

import pygame

from Config import Config
from TemplateTile import TileType

if typing.TYPE_CHECKING:
    from Tile import Tile


class TileRepresenter:
    def __init__(self, tile: Tile):
        self.tile = tile

    @abc.abstractmethod
    def draw(self, screen: pygame.Surface):
        raise NotImplemented()


class UpDownRepresenter(TileRepresenter):
    def draw(self, screen: pygame.Surface):
        actual_x = self.tile.x * Config.CW
        actual_y = self.tile.y * Config.CH

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (actual_x + Config.CW // 4, actual_y, Config.CW // 2, Config.CH)
        )


class RightLeftRepresenter(TileRepresenter):
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
        )


class UpRightRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                Config.CW // 2,
                Config.CH // 2 + Config.CH // 4
            )
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW // 2 + Config.CW // 4 + 1,
                Config.CH // 2
            )
        )


class UpLeftRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                Config.CW // 2,
                Config.CH // 2 + Config.CH // 4
            )
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW // 2 + Config.CW // 4,
                Config.CH // 2
            )
        )


class DownRightRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH,
                Config.CW // 2,
                Config.CH // 2
            )
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW - Config.CW // 4,
                Config.CH // 2
            )
        )


class DownLeftRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH,
                Config.CW // 2,
                Config.CH // 2
            )
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW - 1,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW - Config.CW // 4,
                Config.CH // 2
            )
        )


class CrossRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW + Config.CW // 4, self.tile.y * Config.CH, Config.CW // 2, Config.CH)
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
        )


class ForkRightUpRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH,
                Config.CW // 2,
                Config.CH // 2
            )
        )


class ForkRightDownRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH + Config.CH // 4, Config.CW, Config.CH // 2)
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                Config.CW // 2,
                Config.CH // 2 + Config.CH // 4
            )
        )


class ForkUpRightRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW + Config.CW // 4, self.tile.y * Config.CH, Config.CW // 2, Config.CH)
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW - Config.CW // 4,
                Config.CH // 2
            )
        )


class ForkUpLeftRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.tile.x * Config.CW + Config.CW // 4, self.tile.y * Config.CH, Config.CW // 2, Config.CH)
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW - 1,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW - Config.CW // 4,
                Config.CH // 2
            )
        )


class UpDeadEndRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH - Config.CH // 2 - Config.CH // 4,
                Config.CW // 2,
                Config.CH // 2 + Config.CH // 4
            )
        )


class DownDeadEndRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH,
                Config.CW // 2,
                Config.CH // 2
            )
        )


class RightDeadEndRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW - 1,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW - Config.CW // 4,
                Config.CH // 2
            )
        )


class LeftDeadEndRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                self.tile.x * Config.CW + Config.CW // 4,
                self.tile.y * Config.CH + Config.CH // 4,
                Config.CW - Config.CW // 4,
                Config.CH // 2
            )
        )


class EmptyRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pass


class BigRoomEntranceRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH, Config.CW, Config.CH)
        )


class BigRoomMainRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH, Config.CW, Config.CH)
        )


class BigRoomWallRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (0, 100, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH, Config.CW, Config.CH)
        )


class SingleRoomRepresenter(TileRepresenter):

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.tile.x * Config.CW, self.tile.y * Config.CH, Config.CW, Config.CH)
        )


class TileRepresenterBuilder:
    representer_mapping = {
        TileType.UP_DOWN: UpDownRepresenter,
        TileType.RIGHT_LEFT: RightLeftRepresenter,
        TileType.UP_RIGHT: UpRightRepresenter,
        TileType.UP_LEFT: UpLeftRepresenter,
        TileType.DOWN_RIGHT: DownRightRepresenter,
        TileType.DOWN_LEFT: DownLeftRepresenter,
        TileType.FORK_UP_RIGHT: ForkUpRightRepresenter,
        TileType.FORK_UP_LEFT: ForkUpLeftRepresenter,
        TileType.FORK_RIGHT_DOWN: ForkRightDownRepresenter,
        TileType.FORK_RIGHT_UP: ForkRightUpRepresenter,
        TileType.CROSS: CrossRepresenter,
        TileType.UP_DEAD_END: UpDeadEndRepresenter,
        TileType.RIGHT_DEAD_END: RightDeadEndRepresenter,
        TileType.DOWN_DEAD_END: DownDeadEndRepresenter,
        TileType.LEFT_DEAD_END: LeftDeadEndRepresenter,
        TileType.EMPTY: EmptyRepresenter,
        TileType.SINGLE_ROOM: SingleRoomRepresenter
    }

    @classmethod
    def from_tile(cls, tile: Tile) -> TileRepresenter:
        return cls.representer_mapping[tile.template_tile.tile_type](tile)
